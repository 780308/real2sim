# SAGA: Segment Any 3D Gaussians

## 定位
适合作为交互式选择指定物体/部件的工具，不负责重建/补全。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.15/5 |
| family | promptable 3D Gaussian segmentation |
| sources | https://github.com/Jumpat/SegAnyGAussians<br>https://arxiv.org/abs/2312.00860 |
| local_pdf | ref/saga_2312_00860.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/SegAnyGAussians |
| commit / license | 4acdaa6 / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: trained 3DGS, SAM-generated masks/features, 2D visual prompts, optional physical scale prompt.
- Outputs: prompted 3D Gaussian object/part segmentation in milliseconds.

## Full Method Pipeline
- Attach scale-gated affinity features to Gaussians.
- Distill SAM masks into 3D features with scale-aware contrastive learning.
- At inference, map 2D prompts to 3D queries and segment corresponding Gaussians.
- Use scale gate to handle multi-granularity ambiguity.

## Losses / Objectives
scale-aware contrastive loss over rendered affinity features and SAM-derived mask correspondences.

## Assumptions
已有较好 3DGS；prompt/mask质量足够；scale选择影响结果。

## Failure Modes
多粒度部件边界不稳定；不输出 mesh/collision。

## 对 Directional View Gap 的关系
不补视角；用于指定补齐对象的 selection layer。

## Isaac Sim Transfer
adapter needed: segmented Gaussians 经 mesh extraction 后才可进入 Isaac。

## 可迁移模块
- scene/object representation: promptable 3D Gaussian segmentation
- view/object completion: 不补视角；用于指定补齐对象的 selection layer。
- geometry/collision: prompted 3D Gaussian object/part segmentation in milliseconds.
- simulator integration: adapter needed: segmented Gaussians 经 mesh extraction 后才可进入 Isaac。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 interactive object/part picking utility。

## Next Experiment
用 2D prompt 选门把手/椅腿等细部，测试后续 mesh extraction 是否保持部件边界。
