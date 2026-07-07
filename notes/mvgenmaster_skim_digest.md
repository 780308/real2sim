# MvGenMaster: Scaling Multi-View Consistent Image Generation

优先级：**P2** | 阅读深度：**skim** | 类别：**multi-view image generation** | 综合分：**2.91/5**

## 资料状态
- 类型：repo
- 本地 PDF：无 / 技术项目
- 本地 repo：repos/mvgenmaster
- commit：23ea32e
- license 文件：LICENSE
- Sources:
- https://github.com/ewrfcas/mvgenmaster

## 对 directional view coverage gap 的定位
P2。作为 CAT3D/SEVA 的替补线。

## Inputs / Outputs
- Inputs：multi-view generation conditions。
- Outputs：multi-view consistent images。

## Method Pipeline
- multi-view consistent image generation 方向的补充项目。

## Objectives / Losses
generation consistency objective。

## Assumptions
不是专门 real2sim/Isaac pipeline。

## Failure Modes
3D geometry/collision 输出弱。

## Isaac Sim / 平台迁移判断
visual-only。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | multi-view image generation |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 3.4/5 |
| Isaac Sim path | visual-only。 |
| code/weights | 3.5/5 |
| priority score | 2.91/5 |
