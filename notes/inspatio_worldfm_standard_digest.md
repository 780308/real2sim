# InSpatio-WorldFM: Open-Source Real-Time Generative Frame Model

优先级：**P1** | 阅读深度：**standard** | 类别：**interactive world/video frame model** | 综合分：**3.16/5**

## 资料状态
- 类型：paper+repo+weights
- 本地 PDF：ref/inspatio_worldfm_2603_11911.pdf
- 本地 repo：repos/inspatio-world
- commit：fef9706
- license 文件：LICENSE
- Sources:
- https://inspatio.github.io/inspatio-world/
- https://github.com/inspatio/inspatio-world
- https://huggingface.co/inspatio/world

## 对 directional view coverage gap 的定位
P1。可调研但不作为 directional view completion 第一优先级。

## Inputs / Outputs
- Inputs：video/image states and controls for real-time frame generation。
- Outputs：interactive/generated frames; not persistent mesh/USD。

## Method Pipeline
- real-time frame model for spatial intelligence。
- 支持 checkpoint 下载和 v2v inference。
- 更像 interactive visual simulator，而非 metric reconstruction。

## Objectives / Losses
world/frame generation objective。

## Assumptions
开放且可运行，但输出仍偏 video/frame，不直接适合 collision。

## Failure Modes
缺少 metric 3D anchoring；可能对走廊几何漂移。

## Isaac Sim / 平台迁移判断
visual-only；可作为 long-term policy/world-model data generator。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | interactive world/video frame model |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 3.2/5 |
| Isaac Sim path | visual-only；可作为 long-term policy/world-model data generator。 |
| code/weights | 4.0/5 |
| priority score | 3.16/5 |
