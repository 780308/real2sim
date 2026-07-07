# Real-to-Sim Robot Policy Evaluation with Gaussian Splatting Simulation of Soft-Body Interactions

优先级：**P2** | 阅读深度：**skim** | 类别：**policy evaluation / GS simulator** | 综合分：**2.66/5**

## 资料状态
- 类型：repo
- 本地 PDF：无 / 技术项目
- 本地 repo：repos/real2sim-eval
- commit：8bd7091
- license 文件：LICENSE
- Sources:
- https://github.com/kywind/real2sim-eval

## 对 directional view coverage gap 的定位
P2。最终报告中作为 evaluation 思路参考即可。

## Inputs / Outputs
- Inputs：Gaussian Splatting simulation setup for robot policy evaluation。
- Outputs：policy evaluation environment, soft-body interaction demos。

## Method Pipeline
- 关注 robot policy evaluation rather than scene completion。

## Objectives / Losses
simulation/evaluation pipeline。

## Assumptions
与导航走廊和 Isaac asset 间接相关。

## Failure Modes
不补视角，不输出完整场景几何。

## Isaac Sim / 平台迁移判断
supplementary only。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | policy evaluation / GS simulator |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 2.5/5 |
| Isaac Sim path | supplementary only。 |
| code/weights | 3.0/5 |
| priority score | 2.66/5 |
