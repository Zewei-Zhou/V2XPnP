# V2XPnP: Vehicle-to-Everything Spatio-Temporal Fusion for Multi-Agent Perception and Prediction

[![website](https://img.shields.io/badge/Website-Explore%20Now-blueviolet?style=flat&logo=google-chrome)](https://mobility-lab.seas.ucla.edu/v2xpnp/)
[![paper](https://img.shields.io/badge/arXiv-Paper-<COLOR>.svg)](https://arxiv.org/abs/2412.01812)
[![supplement](https://img.shields.io/badge/Supplementary-Material-red)](https://arxiv.org/abs/2412.01812)
[![data sample](https://img.shields.io/badge/Dataset-Sample-F9D371.svg)](https://drive.google.com/drive/folders/1ZjVW-OKu-afIoiqfQJgFYwHOWzWE8_e8?usp=sharing)
<!-- [![License](https://img.shields.io/badge/License-CC_BY_NC_ND_4.0-F9D371)](https://creativecommons.org/licenses/by-nc-nd/4.0/) -->

This is the official implementation of "V2XPnP: Vehicle-to-Everything Spatio-Temporal Fusion for Multi-Agent Perception and Prediction", [Zewei Zhou](https://zewei-zhou.github.io/), [Hao Xiang](https://xhwind.github.io/), [Zhaoliang Zheng](https://scholar.google.com/citations?user=SyR4O7YAAAAJ&hl=en), [Seth Z. Zhao](https://sethzhao506.github.io/), [Mingyue Lei](https://www.linkedin.com/in/%E6%98%8E%E6%9C%88-%E9%9B%B7-9029611a0/), [Yun Zhang](https://handsomeyun.github.io/), [Tianhui Cai](https://scholar.google.com/citations?user=6YqkXM0AAAAJ&hl=zh-CN&oi=ao),
[Xinyi Liu](https://sherryliu3670.github.io/), [Johnson Liu](), [Maheswari Bajji](), [Jacob Pham](), [Xin Xia](https://scholar.google.com/citations?user=vCYqMTIAAAAJ&hl=en), [Zhiyu Huang](https://mczhi.github.io/), [Bolei Zhou](https://boleizhou.github.io/), [Jiaqi Ma](https://mobility-lab.seas.ucla.edu/about/)

![teaser](images/V2XPnP_framework.png)

V2XPnP is the first open-source V2X spatio-temporal fusion framework for cooperative perception and prediction. This framework combines the intermediate fusion strategy and one-step communication and integrates diverse attention fusion modules in the unified Transformer architecture for V2X spatial-temporal information. Our benchmark model zoo includes 11 SOAT models across no fusion, early fusion, late fusion, and intermediate fusion.

<div align="center">
    <img src="images/V2XPnP_seq_dataset.png" alt="teaser" width="80%">
</div>

V2XPnP Sequential Dataset is the first large-scale, real-world V2X sequential dataset featuring multiple agents and all V2X collaboration modes, ie, vehicle-to-vehicle (V2V), infrastructure-to-infrastructure (I2I), vehicle-centric (VC), and infrastructure-centric (IC).

Supported by the [UCLA Mobility Lab](https://mobility-lab.seas.ucla.edu/)

## Overview
- [Codebase Features](#codebase-features)
- [Release Plan](#release-plan)
- [Dataset](#dataset)
- [Acknowledgment](#acknowledgement)
- [Citation](#citation)

## CodeBase Features
- Support both simulation and real-world V2X dataset
    - [x] [V2XPnP [Ours]](https://arxiv.org/abs/2412.01812)
    - [x] [V2X-Real [ECCV2024]](https://github.com/ucla-mobility/V2X-Real)
    - [x] [V2V4Real [CVPR 2023]](https://github.com/ucla-mobility/v2v4real)
    - [x] [OPV2V [ICRA2022]](https://github.com/DerrickXuNu/OpenCOOD)
- Multiple Tasks supported
    - [x] Cooperative perception and prediction
    - [x] Cooperative single-frame perception
    - [x] Cooperative temporal perception
    - [x] Cooperative prediction
- SOTA model supported
    - [x] No Fusion (Decoupled)
    - [x] [FaF [CVPR2018]](https://arxiv.org/abs/2012.12395) (No Fusion-End2end)
    - [x] Early Fusion
    - [x] Late Fusion (Decoupled)
    - [x] [F-Cooper [SEC2019]](https://arxiv.org/abs/1909.06459)
    - [x] [V2VNet [ECCV2020]](https://arxiv.org/abs/2008.07519)
    - [x] [DiscoNet [NeurIPS 2021]](https://arxiv.org/abs/2111.00643)
    - [x] [V2X-ViT [ECCV 2022]](https://arxiv.org/abs/2203.10638)
    - [x] [CoBEVFlow [NeurIPS 2023]](https://arxiv.org/abs/2309.16940)
    - [x] [FFNet [NeurIPs 2023]](https://arxiv.org/abs/2311.01682)
    - [x] [V2XPnP [Ours]](https://arxiv.org/abs/2412.01812)

## Release Plan
- **`2024/06`**: ✅ Sample Data of V2XPnP in [Google Drive](https://drive.google.com/drive/folders/1ZjVW-OKu-afIoiqfQJgFYwHOWzWE8_e8?usp=sharing) 
- **`2025/03`**: ✅ V2XPnP Dataset 1.0 (68 scenarios) 
- **`2025/05`**: V2XPnP Dataset 2.0 (Whole 100 scenarios)
- **`2025/07`**: V2XPnP Codebase - Official Version 1.0


## Dataset
The V2XPnP Dataset 1.0 can be downloaded in [Train]()([P1](https://ucla.box.com/s/zfbeizdrt9pfayf3oc3zi8fc9d1osjsd),[P2](https://ucla.box.com/s/zxwmm5ohx0xw60wafe9b14kw8uzfyvfl), [P3](https://ucla.box.com/s/pcus09ic7xm87smz2ndjnr27sl67hymf), [P4](https://ucla.box.com/s/b4m4mi2ulls2l5dl3wd5f0ikabn010zs)), [Val](https://ucla.box.com/s/0p1asmx3ueh06hxg6ndzubhk695gbge9), [Test](https://ucla.box.com/s/9ef9sl5hfp64hqypkmx0pub9ega5u37n), and [Map](https://ucla.box.com/s/eapz852kkjzov95gxoxl6p613u63j14s). The sample data of V2XPnP Sequential Dataset can be accessed in [Google Drive](https://drive.google.com/drive/folders/1ZjVW-OKu-afIoiqfQJgFYwHOWzWE8_e8?usp=sharing), and we will release the v2.0 dataset later. The sequential perceptions data format follows the [OpenCOOD](https://opencood.readthedocs.io/en/latest/md_files/data_annotation_tutorial.html), and the trajectory dataset records the whole trajectory of each agent in each scenario.


<!-- ## Benchmark Tasks
- Cooperative perception and prediction
- Cooperative temporal perception
- Cooperative prediction
- **`To be added`** -->

<!-- ## License
All assets and code are under the [CC BY-NC-ND](https://creativecommons.org/licenses/by-nc-nd/4.0/) license unless specified otherwise. -->

## Acknowledgement
V2XPnP belongs to the [OpenCDA ecosystem](https://arxiv.org/abs/2301.07325) family. The codebase is built upon [OpenCOOD](https://github.com/DerrickXuNu/OpenCOOD) in the OpenCDA ecosystem family, and the [V2X-Real](https://arxiv.org/abs/2403.16034), another project in OpenCDA, serves as one of the data sources for this project.

## Citation
If you find this repository useful for your research, please consider giving us a star 🌟 and citing our paper.
 ```bibtex
@article{zhou2024v2xpnp,
  title={V2XPnP: Vehicle-to-Everything Spatio-Temporal Fusion for Multi-Agent Perception and Prediction},
  author={Zhou, Zewei and Xiang, Hao and Zheng, Zhaoliang and Zhao, Seth Z. and Lei, Mingyue and Zhang, Yun and Cai, Tianhui and Liu, Xinyi and Liu, Johnson and Bajji, Maheswari and Pham, Jacob and Xia, Xin and Huang, Zhiyu and Zhou, Bolei and Ma, Jiaqi},
  journal={arXiv preprint arXiv:2412.01812},
  year={2024}
}
```
