# GraspSplats: Efficient Manipulation with 3D Feature Splatting

## 定位
给出 part-level interaction/grasp 的下游验证方式；适合评价生成的门把手/椅子部件是否能被定位和操作。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.01/5 |
| family | feature-enhanced 3DGS for part-level grasping |
| sources | https://github.com/jimazeyu/GraspSplats<br>https://graspsplats.github.io/<br>https://arxiv.org/abs/2409.02084 |
| local_pdf | ref/graspsplats_2409_02084.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/GraspSplats |
| commit / license | e6b837e / n/a (cloned) |

## Inputs / Outputs
- Inputs: posed RGB-D frames from calibrated camera, MobileSAM/MaskCLIP features.
- Outputs: feature-enhanced explicit Gaussians, part-level affordance, grasp proposals, dynamic object updates.

## Full Method Pipeline
- Initialize Gaussians from depth frames.
- Compute 2D reference features and optimize geometry/texture/semantics by differentiable rasterization.
- Use object/part language queries to predict affordance.
- Generate grasp proposals from explicit Gaussian primitives and update under object motion.

## Losses / Objectives
depth/photometric/feature supervision and grasp proposal scoring.

## Assumptions
有 RGB-D 且目标工作空间较小；任务是抓取而非完整 digital twin export。

## Failure Modes
不输出 collision/physical parameters；动态更新依赖 tracking。

## 对 Directional View Gap 的关系
不补视角。

## Isaac Sim Transfer
not direct; 可作为 Isaac asset 的 affordance metadata generator。

## 可迁移模块
- scene/object representation: feature-enhanced 3DGS for part-level grasping
- view/object completion: 不补视角。
- geometry/collision: feature-enhanced explicit Gaussians, part-level affordance, grasp proposals, dynamic object updates.
- simulator integration: not direct; 可作为 Isaac asset 的 affordance metadata generator。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 manipulation evaluation tool。

## Next Experiment
对生成/重建的桌椅部件跑 GraspSplats-style feature distillation，测试 part query localization。
