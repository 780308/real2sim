# Object-Aware Gaussian Splatting for Robotic Manipulation

## 定位
强调 objectness 对实时交互的重要性，可启发资产运行时更新模块。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 2.56/5 |
| family | dynamic object-aware Gaussians for manipulation |
| sources | https://object-aware-gaussian.github.io/<br>https://openreview.net/forum?id=t46z5MslkU |
| local_pdf | ref/object_aware_gaussian_splatting_robotic_manipulation_2024_openreview.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | 无 |
| commit / license | n/a / n/a (no-repo) |

## Inputs / Outputs
- Inputs: three RGB-D camera views, object-wise segmentation, pretrained foundation model semantics.
- Outputs: dynamic object-aware Gaussian representation updated at about 30 Hz; language-conditioned dynamic grasping.

## Full Method Pipeline
- Initialize dense point cloud and object-wise Gaussians from few RGB-D cameras.
- Inject objectness/semantic labels at initialization.
- Update Gaussians object-wise rather than per-Gaussian for speed.
- Use representation for dynamic language-conditioned grasping and visuomotor policy training.

## Losses / Objectives
dynamic 3DGS reconstruction/update objectives; policy imitation/behavior cloning in downstream usage.

## Assumptions
多 RGB-D 相机固定覆盖 workspace；不是离线高保真 Isaac asset pipeline。

## Failure Modes
无开源代码；碰撞/mesh/physical parameters 缺失。

## 对 Directional View Gap 的关系
通过多 RGB-D 视角减少缺失，但不是生成式补齐。

## Isaac Sim Transfer
not direct。

## 可迁移模块
- scene/object representation: dynamic object-aware Gaussians for manipulation
- view/object completion: 通过多 RGB-D 视角减少缺失，但不是生成式补齐。
- geometry/collision: dynamic object-aware Gaussian representation updated at about 30 Hz; language-conditioned dynamic grasping.
- simulator integration: not direct。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 runtime object update idea，不作为短期复现。

## Next Experiment
借鉴 object-wise update 思路，为 Isaac 中可移动物体维护 object ID 和 visual layer transform。
