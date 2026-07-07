# GSDF: 3DGS Meets SDF for Improved Neural Rendering and Reconstruction

## 定位
和 SuGaR/PGSR/2DGS 同属 geometry repair 后端，可作为 SDF-based 对照。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.56/5 |
| family | 3DGS + SDF surface constraint |
| sources | https://github.com/city-super/GSDF<br>https://arxiv.org/abs/2403.16964 |
| local_pdf | ref/gsdf_2403_16964.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/GSDF |
| commit / license | fba285f / LICENSE.md (cloned) |

## Inputs / Outputs
- Inputs: posed RGB images, 3DGS/SDF reconstruction setup.
- Outputs: SDF-improved neural rendering/reconstruction with better surfaces.

## Full Method Pipeline
- Combine Gaussian representation with SDF-inspired geometry constraints.
- Optimize radiance and surface fields jointly.
- Use SDF signal to improve surface reconstruction.
- Extract geometry for mesh-like downstream use.

## Losses / Objectives
photometric rendering losses plus SDF/eikonal/surface related constraints.

## Assumptions
适合表面可由 SDF 表达的对象；训练复杂度高于纯 3DGS。

## Failure Modes
对透明/薄结构和未观测面仍有限；代码集成成本较高。

## 对 Directional View Gap 的关系
不补视角。

## Isaac Sim Transfer
adapter needed: SDF/mesh extraction 后用于 collision proxy。

## 可迁移模块
- scene/object representation: 3DGS + SDF surface constraint
- view/object completion: 不补视角。
- geometry/collision: SDF-improved neural rendering/reconstruction with better surfaces.
- simulator integration: adapter needed: SDF/mesh extraction 后用于 collision proxy。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 SDF geometry baseline。

## Next Experiment
若 SuGaR/PGSR mesh 对门边/桌腿不稳定，再测试 GSDF surface extraction。
