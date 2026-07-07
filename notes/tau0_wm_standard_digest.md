# τ0-WM: A Unified Video-Action World Model for Robotic Manipulation

优先级：**P1** | 阅读深度：**standard** | 类别：**video-action manipulation world model** | 综合分：**2.19/5**

## 资料状态
- 类型：paper
- 本地 PDF：ref/tau0_wm_2606_01027.pdf
- 本地 repo：无
- commit：N/A
- license 文件：未在 repo 根目录确认
- Sources:
- https://arxiv.org/abs/2606.01027

## 对 directional view coverage gap 的定位
P1 低位，仅在最终报告中作为 world-model 辅助方向。

## Inputs / Outputs
- Inputs：robot observation/action sequences。
- Outputs：future video prediction, action evaluation, policy-related outputs。

## Method Pipeline
- 共享未来预测框架同时服务 policy learning、video prediction、action evaluation。
- 目标是 manipulation action grounding。

## Objectives / Losses
video-action prediction/evaluation objectives。

## Assumptions
方向与 embodied world model 有关，但与静态走廊 large-angle view completion 间接。

## Failure Modes
无 geometry/collision asset；没有直接补 3DGS 黑洞路线。

## Isaac Sim / 平台迁移判断
not suitable for current visual asset completion。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | video-action manipulation world model |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 3.0/5 |
| Isaac Sim path | not suitable for current visual asset completion。 |
| code/weights | 1.2/5 |
| priority score | 2.19/5 |
