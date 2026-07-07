# PGSR: Planar-based Gaussian Splatting for Efficient and High-Fidelity Surface Reconstruction

## 定位
适合室内门、墙、桌面等 planar objects 的 geometry layer；对 collision proxy 很实用。

| 字段 | 内容 |
| --- | --- |
| priority / score | P0 / 3.83/5 |
| family | surface-aware 3DGS / mesh reconstruction |
| sources | https://github.com/zju3dv/PGSR<br>https://arxiv.org/abs/2406.06521 |
| local_pdf | ref/pgsr_2406_06521.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/PGSR |
| commit / license | de24f1a / LICENSE.md (cloned) |

## Inputs / Outputs
- Inputs: multi-view RGB / SfM poses; no pretrained depth/normal prior required.
- Outputs: planar-regularized 3DGS and mesh/surface reconstruction.

## Full Method Pipeline
- Train 3DGS with planar-based constraints.
- Use geometry regularization to improve surface fidelity.
- Extract mesh/surface for downstream use.
- Combine with pseudo/completed views to reduce holes.

## Losses / Objectives
photometric loss plus planar/surface regularization losses.

## Assumptions
目标表面具有平面/局部平滑结构；缺失背面仍需补齐。

## Failure Modes
错误 pseudo views 会被几何正则固化；非平面复杂物体优势下降。

## 对 Directional View Gap 的关系
后端修复，不直接补视角。

## Isaac Sim Transfer
adapter needed: mesh output可转 USD/collision。

## 可迁移模块
- scene/object representation: surface-aware 3DGS / mesh reconstruction
- view/object completion: 后端修复，不直接补视角。
- geometry/collision: planar-regularized 3DGS and mesh/surface reconstruction.
- simulator integration: adapter needed: mesh output可转 USD/collision。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P0 几何后端，尤其针对门/桌面/墙体。

## Next Experiment
对门和桌面对象跑 PGSR，与 SuGaR/2DGS 输出 mesh 做 collision proxy 对比。
