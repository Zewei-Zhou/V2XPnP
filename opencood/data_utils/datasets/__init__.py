from opencood.data_utils.datasets.late_fusion_dataset import LateFusionDataset
from opencood.data_utils.datasets.early_fusion_dataset import EarlyFusionDataset
from opencood.data_utils.datasets.intermediate_fusion_dataset import IntermediateFusionDataset
from opencood.data_utils.datasets.intermediate_fusion_dataset_v2 import IntermediateFusionDatasetV2
from opencood.data_utils.datasets.e2e_early_fusion_dataset import E2EEarlyFusionDataset

__all__ = {
    'LateFusionDataset': LateFusionDataset,
    'EarlyFusionDataset': EarlyFusionDataset,
    'E2EEarlyFusionDataset': E2EEarlyFusionDataset,
    'IntermediateFusionDataset': IntermediateFusionDataset,
    'IntermediateFusionDatasetV2': IntermediateFusionDatasetV2,
}

# the final range for evaluation
GT_RANGE = [-70.4, -40, -15, 70.4, 40, 15]
# The communication range for cavs
COM_RANGE = 50
# Data record Hz
DATA_Hz = 10


def build_dataset(dataset_cfg, visualize=False, train=True):
    dataset_name = dataset_cfg['fusion']['core_method']
    error_message = f"{dataset_name} is not found. " \
                    f"Please add your processor file's name in opencood/" \
                    f"data_utils/datasets/init.py"
    assert dataset_name in __all__.keys(), error_message

    dataset = __all__[dataset_name](
        params=dataset_cfg,
        visualize=visualize,
        train=train
    )

    return dataset
