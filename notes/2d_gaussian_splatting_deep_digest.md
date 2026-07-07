# 2D Gaussian Splatting for Geometrically Accurate Radiance Fields

优先级：**P0** | 阅读深度：**deep** | 类别：**surfel Gaussian representation / mesh extraction** | 综合分：**3.86/5**

## 资料状态
- 类型：paper+repo
- 本地 PDF：ref/2d_gaussian_splatting_2403_17888.pdf
- 本地 repo：repos/2d-gaussian-splatting
- commit：335ad61
- license 文件：LICENSE.md
- Sources:
- https://surfsplatting.github.io/
- https://github.com/hbb1/2d-gaussian-splatting
- https://arxiv.org/abs/2403.17888

## 对 directional view coverage gap 的定位
P0 后处理候选，与 PGSR/SuGaR 共同组成 GS repair baseline。

## Inputs / Outputs
- Inputs：COLMAP/NeRF-style posed images。
- Outputs：2D surfel Gaussians, rendered RGB/depth, mesh extraction including unbounded scenes。

## Method Pipeline
- 用 2D oriented disks/surfels 取代无结构 3D Gaussian ellipsoids。
- normal consistency / depth distortion regularization。
- TSDF/adaptive meshing 输出 mesh。

## Objectives / Losses
RGB rendering loss + normal/depth/distortion regularization。

## Assumptions
同样不能无中生有补 unseen yaw，但在有 pseudo views 后更适合 surface geometry。

## Failure Modes
输入视角不足时会过拟合已见表面；走廊反向墙面需额外 NVS/采集。

## Isaac Sim / 平台迁移判断
adapter needed；mesh extraction 对 Isaac 有价值。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | surfel Gaussian representation / mesh extraction |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 4.2/5 |
| Isaac Sim path | adapter needed；mesh extraction 对 Isaac 有价值。 |
| code/weights | 4.2/5 |
| priority score | 3.86/5 |
