# GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning

优先级：**P0** | 阅读深度：**deep** | 类别：**3DGS simulator / real2sim framework** | 综合分：**4.01/5**

## 资料状态
- 类型：paper+repo
- 本地 PDF：ref/gs_playground_2604_25459.pdf
- 本地 repo：repos/gs_playground
- commit：33127ca
- license 文件：LICENSE
- Sources:
- https://gsplayground.github.io
- https://github.com/discoverse-dev/gs_playground
- https://arxiv.org/abs/2604.25459

## 对 directional view coverage gap 的定位
P0 平台参考。吸收 batch 3DGS observation + physics separation，但 directional completion 仍靠 NVS/completion 模块。

## Inputs / Outputs
- Inputs：3DGS assets + robot/physics assets；Real2Sim workflow via GS-Real2Sim。
- Outputs：batched RGB/depth observations, contact/physics integration, sim-ready assets。

## Method Pipeline
- 把 parallel physics engine 与 batch 3DGS rendering 耦合。
- Rigid-Link Gaussian Kinematics 将 Gaussian clusters 绑定刚体。
- 支持 navigation/manipulation/locomotion 视觉 RL。

## Objectives / Losses
系统框架，不是单个 learning loss；重点是 throughput、synchronized visuals、asset packaging。

## Assumptions
README 标注 full Real2Sim asset packaging/collision sync 仍在 release plan；Isaac 不是主后端。

## Failure Modes
它不主动补 unseen yaw；坏 3DGS 进来仍会坏。

## Isaac Sim / 平台迁移判断
adapter needed；是 Isaac 之外最重要的 sim architecture reference。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | 3DGS simulator / real2sim framework |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 3.8/5 |
| Isaac Sim path | adapter needed；是 Isaac 之外最重要的 sim architecture reference。 |
| code/weights | 4.0/5 |
| priority score | 4.01/5 |
