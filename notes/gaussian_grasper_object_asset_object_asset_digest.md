# GaussianGrasper: 3D Language Gaussian Splatting for Open-vocabulary Robotic Grasping

## 定位
交互层参考：object asset 不仅要能看，还应提供 language query 和 grasp geometry。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 2.89/5 |
| family | language Gaussian field + grasping |
| sources | https://github.com/MrSecant/GaussianGrasper<br>https://arxiv.org/abs/2403.09637 |
| local_pdf | ref/gaussiangrasper_2403_09637.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/GaussianGrasper |
| commit / license | 2ac23c2 / n/a (cloned) |

## Inputs / Outputs
- Inputs: limited RGB-D views, SAM/CLIP features, pretrained grasping model.
- Outputs: language-embedded Gaussian feature field, rendered depth/normal, collision-free grasp pose candidates.

## Full Method Pipeline
- Initialize 3DGS from RGB-D scans.
- Distill dense language features using SAM and CLIP with contrastive learning.
- Locate target from open-vocabulary query.
- Use rendered normals and geometry to filter grasp candidates, then update scene after manipulation.

## Losses / Objectives
contrastive feature distillation, photometric/geometric reconstruction, normal-guided grasp filtering.

## Assumptions
RGB-D 质量可靠；open-vocabulary features定位足够精准。

## Failure Modes
feature 边界和 grasp 质量受 3DGS geometry 影响；不生成完整 mesh/collision asset。

## 对 Directional View Gap 的关系
不补视角。

## Isaac Sim Transfer
not direct; metadata/affordance path only。

## 可迁移模块
- scene/object representation: language Gaussian field + grasping
- view/object completion: 不补视角。
- geometry/collision: language-embedded Gaussian feature field, rendered depth/normal, collision-free grasp pose candidates.
- simulator integration: not direct; metadata/affordance path only。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 interaction evaluation baseline。

## Next Experiment
用它的 language feature field 检查重建资产是否能定位“door handle/table leg/chair back”。
