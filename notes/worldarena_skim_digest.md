# WorldArena: Benchmark for Embodied World Models

优先级：**P2** | 阅读深度：**skim** | 类别：**world model benchmark** | 综合分：**2.52/5**

## 资料状态
- 类型：repo
- 本地 PDF：无 / 技术项目
- 本地 repo：repos/WorldArena
- commit：329f6c7
- license 文件：未在 repo 根目录确认
- Sources:
- https://github.com/tsinghua-fib-lab/WorldArena
- https://world-arena.ai/

## 对 directional view coverage gap 的定位
P2。用来构造 world model 对照实验，而非主线。

## Inputs / Outputs
- Inputs：world model generated videos and evaluation tasks。
- Outputs：benchmark scores / human and automated evaluation protocols。

## Method Pipeline
- 用于比较 embodied world model 的感知和 functional utility。

## Objectives / Losses
benchmark not method。

## Assumptions
对本项目可提供 evaluation inspiration，不提供补全模块。

## Failure Modes
不能直接修复 Go2 3DGS。

## Isaac Sim / 平台迁移判断
evaluation-only。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | world model benchmark |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 2.5/5 |
| Isaac Sim path | evaluation-only。 |
| code/weights | 3.5/5 |
| priority score | 2.52/5 |
