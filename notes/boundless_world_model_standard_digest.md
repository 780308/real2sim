# Boundless World Model (BWM)

优先级：**P1** | 阅读深度：**standard** | 类别：**action-conditioned robot video world model** | 综合分：**2.69/5**

## 资料状态
- 类型：repo+weights
- 本地 PDF：无 / 技术项目
- 本地 repo：repos/boundless-world-model
- commit：2c1a83b
- license 文件：LICENSE
- Sources:
- https://github.com/boundless-large-model/boundless-world-model
- https://huggingface.co/BLM-Lab/Boundless-World-Model

## 对 directional view coverage gap 的定位
P1/P2 边界。保留在开放 world model 对照组，不投入主线工程。

## Inputs / Outputs
- Inputs：initial frames + robot action sequences。
- Outputs：action-conditioned robot manipulation videos。

## Method Pipeline
- 基于 Wan2.2-TI2V-5B；已释放 inference code/model definition/weights。
- 训练代码和 technical report 仍 TODO。
- WorldArena 机器人 manipulation videos 表现强。

## Objectives / Losses
action-conditioned video generation。

## Assumptions
主要用于 manipulation，不是 room-scale static geometry completion。

## Failure Modes
无法输出 mesh/USD；对 Go2 走廊反向 yaw 只是视觉预测参考。

## Isaac Sim / 平台迁移判断
visual-only / not suitable for geometry。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | action-conditioned robot video world model |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 3.0/5 |
| Isaac Sim path | visual-only / not suitable for geometry。 |
| code/weights | 3.5/5 |
| priority score | 2.69/5 |
