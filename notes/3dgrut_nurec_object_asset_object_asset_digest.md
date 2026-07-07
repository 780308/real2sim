# 3DGRT/3DGUT/3DGRUT and NVIDIA NuRec-oriented Gaussian Rendering

## 定位
不解决 object geometry/collision，但非常重要：Isaac Sim 5.0/Omniverse 的 Gaussian visual layer 可能走 NuRec/USDZ/3DGRUT 生态。

| 字段 | 内容 |
| --- | --- |
| priority / score | P0 / 3.63/5 |
| family | production-ready Gaussian rendering / USD export / distorted cameras |
| sources | https://github.com/nv-tlabs/3DGRUT<br>https://research.nvidia.com/labs/toronto-ai/3DGUT<br>https://developer.nvidia.com/omniverse/nurec |
| local_pdf | ref/3dgrut_2412_12507.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/3DGRUT |
| commit / license | 21bd44d / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: 3DGS/3DGRT/3DGUT scenes, COLMAP/NCore datasets, masks, complex camera models.
- Outputs: trained Gaussian scenes, USD/PLY/NuRec export, rendering with distorted cameras, rolling shutter, secondary rays.

## Full Method Pipeline
- Replace 3DGS projection linearization with Unscented Transform to support nonlinear camera projection.
- Unify rasterization and ray tracing formulation for primary/secondary rays.
- Train/export scenes in a production-oriented pipeline.
- Use USD/NuRec path for Omniverse/Isaac rendering integration.

## Losses / Objectives
standard 3DGS reconstruction losses with 3DGUT projection/rendering changes.

## Assumptions
主要关心渲染而非物理；collision 仍需 mesh。

## Failure Modes
视觉层接入成功不代表可交互；复杂 camera 支持不补 missing geometry。

## 对 Directional View Gap 的关系
可更准确支持 Go2/广角/畸变相机训练与渲染，但不生成 unseen view。

## Isaac Sim Transfer
direct for visual layer: USD/NuRec/Omniverse 方向最值得关注。

## 可迁移模块
- scene/object representation: production-ready Gaussian rendering / USD export / distorted cameras
- view/object completion: 可更准确支持 Go2/广角/畸变相机训练与渲染，但不生成 unseen view。
- geometry/collision: trained Gaussian scenes, USD/PLY/NuRec export, rendering with distorted cameras, rolling shutter, secondary rays.
- simulator integration: direct for visual layer: USD/NuRec/Omniverse 方向最值得关注。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P0 visual layer integration path；和 SuGaR/OpenReal2Sim 的 geometry layer 并行。

## Next Experiment
把现有 3DGS/3DGRUT 输出转 NuRec/USDZ，在 Isaac Sim 5.0 中测试 RGB camera rendering 与 mesh collision 同步。
