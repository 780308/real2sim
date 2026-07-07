# GaussGym: An Open-Source Real-to-Sim Framework for Learning Locomotion from Pixels

优先级：**P0** | 阅读深度：**deep** | 类别：**real-to-sim 3DGS locomotion framework** | 综合分：**3.41/5**

## 资料状态
- 类型：paper
- 本地 PDF：ref/gaussgym_2510_15352.pdf
- 本地 repo：无
- commit：N/A
- license 文件：未在 repo 根目录确认
- Sources:
- https://arxiv.org/abs/2510.15352

## 对 directional view coverage gap 的定位
P0 概念参考，工程优先级低于 OpenReal2Sim/GS-Playground，因为代码证据较弱。

## Inputs / Outputs
- Inputs：phone scan/video or generative video model outputs + 3DGS rendering integrated with IsaacGym-style pipeline。
- Outputs：photorealistic high-throughput robot learning environment。

## Method Pipeline
- 把 3D Gaussian renderer 集成到 GPU robot simulation。
- 支持从手机扫描/视频模型构建真实感世界。
- 用于 pixel-based locomotion policy training。

## Objectives / Losses
系统框架与 RL performance；不是 view completion loss。

## Assumptions
paper 可得，但本轮未确认官方 repo 完整可用。

## Failure Modes
它是整合路径，不解决反向视角观测缺失；对 geometry/collision 细节需继续核验。

## Isaac Sim / 平台迁移判断
adapter needed / possibly direct if IsaacGym branch available。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | real-to-sim 3DGS locomotion framework |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 3.5/5 |
| Isaac Sim path | adapter needed / possibly direct if IsaacGym branch available。 |
| code/weights | 2.0/5 |
| priority score | 3.41/5 |
