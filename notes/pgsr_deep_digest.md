# PGSR: Planar-based Gaussian Splatting for Efficient and High-Fidelity Surface Reconstruction

优先级：**P0** | 阅读深度：**deep** | 类别：**3DGS geometry regularization / mesh extraction** | 综合分：**3.81/5**

## 资料状态
- 类型：paper+repo
- 本地 PDF：ref/pgsr_2406_06521.pdf
- 本地 repo：repos/PGSR
- commit：de24f1a
- license 文件：LICENSE.md
- Sources:
- https://zju3dv.github.io/pgsr/
- https://github.com/zju3dv/PGSR
- https://arxiv.org/abs/2406.06521

## 对 directional view coverage gap 的定位
P0 工程后端：SEVA/GEN3C 生成反向视角后，用 PGSR 验证重训是否减少黑洞并改善 mesh。

## Inputs / Outputs
- Inputs：multi-view RGB / SfM poses；无需预训练 depth/normal prior。
- Outputs：planar-constrained 3DGS and surface reconstruction / mesh。

## Method Pipeline
- 用 planar-based Gaussian 表达增强 surface alignment。
- 通过 multi-view constraints 提高 geometry accuracy。
- 用于把 pseudo views + 原始 views 重训成更适合 mesh/Isaac 的表示。

## Objectives / Losses
RGB reconstruction + planar/geometric regularization；目标是高保真 surface reconstruction。

## Assumptions
不能凭空补未观测反向内容；必须与 NVS 或补采集结合。

## Failure Modes
若 pseudo views 错误，PGSR 会把错误几何固化；需要 confidence weighting。

## Isaac Sim / 平台迁移判断
adapter needed but strong；可作为 GS-to-surface bridge。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | 3DGS geometry regularization / mesh extraction |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 4.3/5 |
| Isaac Sim path | adapter needed but strong；可作为 GS-to-surface bridge。 |
| code/weights | 4.0/5 |
| priority score | 3.81/5 |
