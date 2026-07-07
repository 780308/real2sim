# Splat-MOVER: Robotic Manipulation via Editable Gaussian Splatting

## 定位
不是资产导出主线，但给出 object asset 是否支持 semantic/affordance/manipulation 的评价维度。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.08/5 |
| family | editable semantic/affordance GS for manipulation |
| sources | https://github.com/StanfordMSL/Splat-MOVER<br>https://splatmover.github.io/<br>https://arxiv.org/abs/2405.04378 |
| local_pdf | ref/splat_mover_2405_04378.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/Splat-MOVER |
| commit / license | 1bb64bc / LICENSE.txt (cloned) |

## Inputs / Outputs
- Inputs: brief pre-scan RGB images, language prompt, pretrained semantic/grasp affordance features.
- Outputs: ASK-Splat semantic/affordance Gaussians, SEE-Splat scene edits, Grasp-Splat grasp proposals.

## Full Method Pipeline
- Train ASK-Splat from posed RGB images with CLIP and grasp affordance features.
- Localize objects from open-vocabulary prompt.
- SEE-Splat edits object pose/scene state after manipulation.
- Grasp-Splat proposes affordance-aligned grasps.

## Losses / Objectives
Gaussian reconstruction losses plus feature/affordance distillation; grasp ranking uses affordance scores.

## Assumptions
workspace小、预扫描短、动作后对象可通过编辑更新；不追求 Isaac asset fidelity。

## Failure Modes
视觉编辑不等于物理仿真；collision/mesh/physics 参数缺失。

## 对 Directional View Gap 的关系
局部 object infilling 仅视觉。

## Isaac Sim Transfer
not direct; 可迁移 semantic/affordance features 到 Isaac asset metadata。

## 可迁移模块
- scene/object representation: editable semantic/affordance GS for manipulation
- view/object completion: 局部 object infilling 仅视觉。
- geometry/collision: ASK-Splat semantic/affordance Gaussians, SEE-Splat scene edits, Grasp-Splat grasp proposals.
- simulator integration: not direct; 可迁移 semantic/affordance features 到 Isaac asset metadata。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 interaction evaluation reference。

## Next Experiment
把 ObjectGS 生成的 object Gaussians 加上语言/affordance tags，测试是否能服务 grasp planning。
