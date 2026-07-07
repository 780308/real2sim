# Gaussian Grouping: Segment and Edit Anything in 3D Scenes

## 定位
可作为 ObjectGS 之前的稳健 baseline，用于快速 object grouping 和局部编辑。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.41/5 |
| family | 3DGS instance grouping / object editing |
| sources | https://github.com/lkeab/gaussian-grouping<br>https://arxiv.org/abs/2312.00732 |
| local_pdf | ref/gaussian_grouping_2312_00732.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/gaussian-grouping |
| commit / license | 0ab60af / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: posed RGB images, SAM masks, DEVA/consistent 2D masks.
- Outputs: grouped Gaussians with Identity Encoding; object removal/inpainting/editing.

## Full Method Pipeline
- Train 3DGS while augmenting each Gaussian with Identity Encoding.
- Supervise identity features through differentiable rendering using 2D masks.
- Apply 3D spatial consistency regularization.
- Use grouped Gaussians for object removal, inpainting, colorization or recomposition.

## Losses / Objectives
photometric reconstruction, identity classification, 3D spatial consistency regularization.

## Assumptions
需要稳定多视角 masks；编辑/inpainting 更偏视觉，不保证物理几何正确。

## Failure Modes
物体边界粘连、mask ID 不一致、编辑后几何不可碰撞。

## 对 Directional View Gap 的关系
object inpainting 可补视觉空洞，但不是 metric backside completion。

## Isaac Sim Transfer
visual-only / adapter needed: grouped Gaussians可分离 object visual layer，mesh/collision 需 SuGaR/2DGS。

## 可迁移模块
- scene/object representation: 3DGS instance grouping / object editing
- view/object completion: object inpainting 可补视觉空洞，但不是 metric backside completion。
- geometry/collision: grouped Gaussians with Identity Encoding; object removal/inpainting/editing.
- simulator integration: visual-only / adapter needed: grouped Gaussians可分离 object visual layer，mesh/collision 需 SuGaR/2DGS。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 object grouping baseline；若 ObjectGS 环境难装，可先用它分离物体。

## Next Experiment
在当前场景上训练 grouped 3DGS，测试目标门/桌椅是否能独立 render/remove/export。
