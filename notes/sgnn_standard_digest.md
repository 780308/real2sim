# SG-NN: Sparse Generative Neural Networks for Self-Supervised Scene Completion of RGB-D Scans

优先级：**P1** | 阅读深度：**standard** | 类别：**RGB-D scan geometry completion** | 综合分：**3.63/5**

## 资料状态
- 类型：paper+repo+weights
- 本地 PDF：ref/sgnn_cvpr2020.pdf
- 本地 repo：repos/sgnn
- commit：1af2193
- license 文件：LICENSE
- Sources:
- https://github.com/angeladai/sgnn
- https://arxiv.org/abs/1912.00036

## 对 directional view coverage gap 的定位
P1。方法理念值得借鉴，直接复现优先级低于 Seen2Scene/GenRC。

## Inputs / Outputs
- Inputs：partial/noisy RGB-D scans。
- Outputs：completed high-resolution 3D reconstruction / unseen geometry。

## Method Pipeline
- self-supervised: 从 incomplete scan 中移除 frames 构造更不完整输入。
- sparse generative network 预测 missing geometry。
- marching cubes 可视化 surface。

## Objectives / Losses
self-supervised scene completion losses。

## Assumptions
老项目依赖 Python 2.7 / PyTorch 1.1 / SparseConvNet，工程成本较高。

## Failure Modes
几何补全不处理 photorealistic texture；需另接 NVS/texture pipeline。

## Isaac Sim / 平台迁移判断
adapter needed；可作为 geometry-only baseline。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | RGB-D scan geometry completion |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 3.6/5 |
| Isaac Sim path | adapter needed；可作为 geometry-only baseline。 |
| code/weights | 3.5/5 |
| priority score | 3.63/5 |
