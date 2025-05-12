import numpy as np
import torch
import matplotlib.pyplot as plt
from sklearn.neighbors import KDTree
from opencood.data_utils.datasets.map.map_types import *
from opencood.utils.common_utils import rotate_points_along_z_2d

src_polylines_num = 5
points_per_segment = 10  # Notice: add yaml
boundary_type = 5  # Notice: be consistent with lane type in map type


def get_polyline_heading(polyline):
    """
    Calculate the heading of each segment in the given polyline.

    Parameters
    ----------
    polyline: np | (N,3) x, y, z

    """
    polyline_pre = np.roll(polyline, shift=1, axis=0)
    # keep the start point
    polyline_pre[0] = polyline[0]
    # calculate the diff
    diff = polyline - polyline_pre
    polyline_heading = diff / np.clip(np.linalg.norm(diff, axis=-1)[:, np.newaxis],
                                      a_min=1e-6, a_max=1000000000)  # normalization
    # update the first value with the second step
    polyline_heading[0] = polyline_heading[1]
    return polyline_heading


def normalize_angle(theta_list):
    for i in range(len(theta_list)):
        while theta_list[i] > np.pi:
            theta_list[i] -= 2 * np.pi
        while theta_list[i] < -np.pi:
            theta_list[i] += 2 * np.pi
    return theta_list


def decode_map_features_from_proto(map_features):
    """
    Decode map features from the input protobuf data and generate processed polyline segments.

    Parameters
    ----------
    map_features: list
        List of map feature data

    Returns
    ----------
    map_infos: dict
        'polylines': np, (N, points_per_segment, 7) | [x, y, z, dir_x, dir_y, dir_z, global_type]
        'polylines_mask': np, (N, points_per_segment)
    """
    polylines = []
    polylines_mask = []

    def process_polyline(cur_polyline):
        cur_polyline = np.concatenate((cur_polyline[:, :3],
                                       get_polyline_heading(cur_polyline[:, :3]),
                                       cur_polyline[:, 3:]), axis=-1)
        for i in range(0, cur_polyline.shape[0], points_per_segment):
            cur_polyline_segment = cur_polyline[i:i + points_per_segment]
            # d = np.linalg.norm(cur_polyline_segment[:, 0:2], axis=-1)
            # if np.max(d) > 50:
            #     continues
            if cur_polyline_segment.shape[0] < points_per_segment / 2:
                continue

            cur_polyline_segment_mask = np.zeros(points_per_segment)
            cur_polyline_segment_mask[:cur_polyline_segment.shape[0]] = 1

            if cur_polyline_segment.shape[0] < points_per_segment:
                padding = np.zeros((points_per_segment - cur_polyline_segment.shape[0],
                                    cur_polyline_segment.shape[1]))
                cur_polyline_segment = np.concatenate((cur_polyline_segment, padding), axis=0)

            polylines.append(cur_polyline_segment)
            polylines_mask.append(cur_polyline_segment_mask)

    for cur_data in map_features:
        if isinstance(cur_data, Lane):
            # center line
            polyline = np.array([[map_point.x, map_point.y, map_point.z, cur_data.type]
                                 for map_point in cur_data.polyline])
            if polyline.shape[0] > points_per_segment / 2:
                process_polyline(polyline)

            # boundary for driving lanes
            if cur_data.type == 1:
                boundary = np.array([[map_point.x, map_point.y, map_point.z, boundary_type]
                                     for map_point in cur_data.boundary])
                if boundary.shape[0] > points_per_segment / 2:
                    process_polyline(boundary)

    # (num_polylines, points_per_segment, 7), (num_polylines, points_per_segment)
    map_infos = {'polylines': np.array(polylines, dtype=np.float32),
                 'polylines_mask': np.array(polylines_mask, dtype=np.int32)}

    return map_infos


def generate_center_map(map_infos, local_centers, object_local_poses=None):
    """
    Generate center map based on map_infos and centers.
    1. select closest map elements
    2. map coordinates transformation
    
    Parameters
    ----------
    map_infos: dict
        Dictionary containing polylines and their masks.
    local_centers: np
        Array of object center coordinates, shape (N, 6) | [x, y, z, roll, yaw (degree), pitch]
    object_local_poses: np
        loacl pos of each object in center coordinate
        shape (N, 7) | [x, y, z, l, w, h, yaw(radian)] or shape (N, 3) | [x, y, z]
        if not include the angle list, the map will rotate just based on the local center's angle

    Returns
    -------
    map_polylines: np
        Batch map polyline | (N or (H, M), src_polylines_num, points_per_segment, 7)
        [x, y, dir_x, dir_y, global_type, pre_x, pre_y]
    map_polylines_mask: np
        (N or (H, M), src_polylines_num, points_per_segment)
    map_polylines_center: np
        (N or (H, M), src_polylines_num, 2) [x, y]

    """
    center_num = local_centers.shape[0]
    polylines = map_infos['polylines'].copy()
    polylines_mask = map_infos['polylines_mask'].copy()
    centers = local_centers.copy()

    local_heading = np.radians(centers[:, 4])  # heading of the local coordinate in world coordinate
    if object_local_poses is not None:
        if object_local_poses.shape[1] == 7:
            object_heading = normalize_angle(np.radians(centers[:, 4]) + object_local_poses[:, 6])
        elif object_local_poses.shape[1] == 3:  # force if to avoid the wrong data
            object_heading = np.radians(centers[:, 4])
    else:
        object_heading = np.radians(centers[:, 4])

    # transform object coordinates by center objects
    def transform_to_center_coordinates(neighboring_polylines, neighboring_polyline_valid_mask):
        neighboring_polylines = neighboring_polylines[:, :, :, [0, 1, 3, 4, 6]]
        neighboring_polylines[:, :, :, 0:2] -= map_centers[:, None, None, 0:2]
        neighboring_polylines[:, :, :, 0:2] = rotate_points_along_z_2d(
            points=neighboring_polylines[:, :, :, 0:2].reshape(-1, 2),
            angle=-np.broadcast_to(object_heading[:, None, None],
                                   (center_num, src_polylines_num, points_per_segment)).reshape(-1)
        ).reshape(center_num, src_polylines_num, points_per_segment, 2)
        neighboring_polylines[:, :, :, 2:4] = rotate_points_along_z_2d(
            points=neighboring_polylines[:, :, :, 2:4].reshape(-1, 2),
            angle=-np.broadcast_to(object_heading[:, None, None],
                                   (center_num, src_polylines_num, points_per_segment)).reshape(-1)
        ).reshape(center_num, src_polylines_num, points_per_segment, 2)

        # use pre points to map
        xy_pos_pre = np.roll(neighboring_polylines[:, :, :, 0:2], shift=1, axis=-2)
        xy_pos_pre[:, :, 0, :] = xy_pos_pre[:, :, 1, :]
        neighboring_polylines = np.concatenate((neighboring_polylines, xy_pos_pre), axis=-1)

        neighboring_polylines[neighboring_polyline_valid_mask == 0] = 0
        return neighboring_polylines, neighboring_polyline_valid_mask

    # select the closest map elements
    if len(polylines) > src_polylines_num:
        polyline_center = polylines[:, :, 0:2].sum(axis=1) / np.clip(
            polylines_mask.sum(axis=1, keepdims=True).astype(float), a_min=1.0, a_max=None)

        map_centers = centers[:, 0:2]
        if object_local_poses is not None:
            centers_offset_rot = np.array(object_local_poses[:, :2], dtype=np.float32)
            center_offset_rot = rotate_points_along_z_2d(points=centers_offset_rot, angle=local_heading)
            map_centers += center_offset_rot

        # dist = np.linalg.norm(map_centers[:, None, :] - polyline_center[None, :, :], axis=-1)
        # topk_idxs = np.argsort(dist, axis=-1)[:, :src_polylines_num]

        # Use KDTree for nearest neighbor search
        tree = KDTree(polyline_center)  # Build KDTree based on polyline centers
        dist, topk_idxs = tree.query(map_centers, k=src_polylines_num)  # Query top-k closest
        
        map_polylines = polylines[topk_idxs]
        map_polylines_mask = polylines_mask[topk_idxs]
    else:
        map_polylines = np.tile(polylines[None, :, :, :], (center_num, 1, 1, 1))
        map_polylines_mask = np.tile(polylines_mask[None, :, :], (center_num, 1, 1))

    map_polylines, map_polylines_mask = transform_to_center_coordinates(
        map_polylines, map_polylines_mask)

    temp_sum = (map_polylines[:, :, :, 0:2] * map_polylines_mask[:, :, :, None].astype(np.float32)).sum(axis=-2)
    map_polylines_center = temp_sum / np.clip(
        map_polylines_mask.sum(axis=-1, keepdims=True).astype(np.float32), a_min=1.0, a_max=None)

    # Debug: Visualize original and transformed maps
    visualize_map_and_transformation(
        map_infos['polylines'],
        map_infos['polylines_mask'],
        map_centers,
        object_heading,
        map_polylines,
        map_polylines_mask
    )

    return map_polylines, map_polylines_mask, map_polylines_center


def visualize_map_and_transformation(map_polylines,
                                     map_polylines_mask,
                                     map_centers,
                                     object_heading,
                                     transformed_polylines,
                                     transformed_polylines_mask):
    """
    Visualize the map polylines, map_centers, and transformations.
    """
    map_center_num = map_centers.shape[0]
    map_polylines_bool_mask = map_polylines_mask.astype(bool)
    transformed_polylines_bool_mask = transformed_polylines_mask.astype(bool)

    # Step 1: Visualize in world coordinates (original coordinates)
    plt.figure(figsize=(6, 12))

    # plt.subplot(1, 2, 1)
    plt.title("World Coordinates: Original Map and map_centers")

    # Plot original map polylines with masking
    for c in range(map_polylines.shape[0]):  # iterate over each center
        plt.plot(map_polylines[c, map_polylines_bool_mask[c, :], 0],
                 map_polylines[c, map_polylines_bool_mask[c, :], 1], 'b-', alpha=0.4)

    # Plot the map_centers and their headings (yaw angle) in world coordinates
    for i in range(map_center_num):
        center_x, center_y = map_centers[i, 0], map_centers[i, 1]
        plt.plot(center_x, center_y, 'ro')
        heading = object_heading[i]  # plot the center point
        dx = np.cos(heading) * 20  # Direction arrow scaled
        dy = np.sin(heading) * 20
        plt.arrow(center_x, center_y, dx, dy, head_width=8, head_length=15, fc='r', ec='r',linewidth=3, alpha=1.0)

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis('equal')

    # Step 2: Visualize in ego coordinates
    for c in range(map_center_num):
        plt.figure(figsize=(6, 12))
        plt.title("Center-Transformed Coordinates: Map and Centers")
        for i in range(src_polylines_num):
            plt.plot(transformed_polylines[c, i, transformed_polylines_bool_mask[c, i, :], 0],
                     transformed_polylines[c, i, transformed_polylines_bool_mask[c, i, :], 1], 'g-', alpha=0.5)

        center_x, center_y = 0, 0
        yaw_angle = 0  # Yaw angle should also be zero (aligned with the new X-axis)
        plt.plot(center_x, center_y, 'ro')  # plot the center point with offset

        dx, dy = 5, 0
        plt.arrow(center_x, center_y, dx, dy, head_width=1, head_length=2, fc='r', ec='r')
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.axis('equal')
        plt.show()
