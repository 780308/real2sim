# Geometric Latent Diffusion (GLD): Multi-view Diffusion with Geometric Foundation Models

优先级：**P1** | 阅读深度：**standard** | 类别：**geometry-latent multi-view diffusion** | 综合分：**3.62/5**

## 资料状态
- 类型：repo+weights
- 本地 PDF：无 / 技术项目
- 本地 repo：repos/GLD
- commit：af5abb8
- license 文件：LICENSE
- Sources:
- https://github.com/cvlab-kaist/GLD
- https://arxiv.org/abs/2603.22275
- https://huggingface.co/SeonghuJeon/GLD

## 对 directional view coverage gap 的定位
P1+。作为 MVGD/SEVA 的几何增强替代，若硬件可用值得验证。

## Inputs / Outputs
- Inputs：multi-view inputs and cameras；使用 Depth Anything 3 / VGGT feature space。
- Outputs：NVS outputs；demo 还能生成 GLB + COLMAP 3D reconstructions。

## Method Pipeline
- 在 geometric foundation model latent space 中做 multi-view diffusion。
- 用 depth/geometry backbone 约束 zero-shot geometry。
- demo 输出可用于后续 mesh/GLB 实验。

## Objectives / Losses
multi-view diffusion objective in geometric latent space。

## Assumptions
需要 48GB+ VRAM，工程成本高；2026 新项目，需复现实测。

## Failure Modes
高资源门槛；foundation geometry 可能不适配低纹理走廊。

## Isaac Sim / 平台迁移判断
adapter needed；GLB 输出使其比普通 NVS 更接近 sim asset。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | geometry-latent multi-view diffusion |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 4.2/5 |
| Isaac Sim path | adapter needed；GLB 输出使其比普通 NVS 更接近 sim asset。 |
| code/weights | 4.0/5 |
| priority score | 3.62/5 |
