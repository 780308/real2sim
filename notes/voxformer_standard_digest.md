# VoxFormer: Sparse Voxel Transformer for Camera-based 3D Semantic Scene Completion

优先级：**P1** | 阅读深度：**standard** | 类别：**semantic scene completion** | 综合分：**3.17/5**

## 资料状态
- 类型：paper+repo+weights
- 本地 PDF：ref/voxformer_2302_12251.pdf
- 本地 repo：repos/VoxFormer
- commit：63da924
- license 文件：LICENSE
- Sources:
- https://github.com/NVlabs/VoxFormer
- https://arxiv.org/abs/2302.12251

## 对 directional view coverage gap 的定位
P1 baseline，用于生成 occupancy prior，不作为视觉补帧主线。

## Inputs / Outputs
- Inputs：single/multiple camera images; depth-estimated sparse visible voxels。
- Outputs：dense 3D semantic voxels。

## Method Pipeline
- stage 1 query proposal from depth-estimated visible structures。
- stage 2 masked autoencoder propagates information to full voxel volume。

## Objectives / Losses
semantic occupancy completion losses。

## Assumptions
户外自动驾驶语境强；室内 Go2 走廊需 domain adaptation。

## Failure Modes
语义 voxel 不等于 textured mesh/NVS；不补 RGB 画面。

## Isaac Sim / 平台迁移判断
adapter needed; useful as uncertainty/occupancy prior。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | semantic scene completion |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 3.5/5 |
| Isaac Sim path | adapter needed; useful as uncertainty/occupancy prior。 |
| code/weights | 3.6/5 |
| priority score | 3.17/5 |
