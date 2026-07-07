# 2D Gaussian Splatting for Geometrically Accurate Radiance Fields

## 定位
把视觉层从 volumetric blobs 推向 surface-like representation，对碰撞层更友好。

| 字段 | 内容 |
| --- | --- |
| priority / score | P0 / 3.83/5 |
| family | surfel Gaussian representation / mesh extraction |
| sources | https://github.com/hbb1/2d-gaussian-splatting<br>https://arxiv.org/abs/2403.17888 |
| local_pdf | ref/2d_gaussian_splatting_2403_17888.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/2d-gaussian-splatting |
| commit / license | 335ad61 / LICENSE.md (cloned) |

## Inputs / Outputs
- Inputs: posed images / COLMAP dataset.
- Outputs: 2D surfel Gaussians, rendered RGB/depth, mesh extraction.

## Full Method Pipeline
- Represent scene/object with 2D surfel-like Gaussians.
- Optimize photometric rendering with geometry-aware representation.
- Render depth and extract mesh.
- Use mesh as Isaac geometry candidate.

## Losses / Objectives
photometric reconstruction plus geometry/depth/surface regularizers depending implementation.

## Assumptions
多视角覆盖足够；thin objects 和 unseen surfaces 仍需补齐。

## Failure Modes
input sparse 时会过拟合已见面；mesh may have holes。

## 对 Directional View Gap 的关系
后端，不生成 unseen content。

## Isaac Sim Transfer
adapter needed: mesh/depth output利于 USD/collision proxy。

## 可迁移模块
- scene/object representation: surfel Gaussian representation / mesh extraction
- view/object completion: 后端，不生成 unseen content。
- geometry/collision: 2D surfel Gaussians, rendered RGB/depth, mesh extraction.
- simulator integration: adapter needed: mesh/depth output利于 USD/collision proxy。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P0 几何后端，与 SuGaR/PGSR 并列比较。

## Next Experiment
用同一 object crop 对比 3DGS+SuGaR、PGSR、2DGS 三条 mesh extraction 的 holes/collision 质量。
