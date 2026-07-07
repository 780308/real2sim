# Seen2Scene: Completing Realistic 3D Scenes with Visibility-Guided Flow

优先级：**P1** | 阅读深度：**standard** | 类别：**real-scan 3D scene completion** | 综合分：**3.45/5**

## 资料状态
- 类型：repo
- 本地 PDF：无 / 技术项目
- 本地 repo：repos/seen2scene
- commit：6618a96
- license 文件：未在 repo 根目录确认
- Sources:
- https://github.com/quan-meng/seen2scene
- https://arxiv.org/abs/2603.28548

## 对 directional view coverage gap 的定位
P1+。作为 GenRC/SceneCompleter 的最新替代线持续关注。

## Inputs / Outputs
- Inputs：incomplete real-world 3D scans, TSDF sparse grids, layout boxes。
- Outputs：completed realistic 3D scenes。

## Method Pipeline
- visibility-guided flow matching mask unknown regions in real scans。
- sparse transformer models complex scene structures。
- layout boxes provide conditioning。

## Objectives / Losses
flow matching objective with visibility masking。

## Assumptions
repo 当前很轻，完整代码/weights 状态需持续跟踪；但问题定义极贴合 partial observation。

## Failure Modes
需要 TSDF/scan preprocessing；与 Go2 3DGS/point cloud 的接口需实现。

## Isaac Sim / 平台迁移判断
adapter needed; strong for Isaac mesh proxy if code matures。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | real-scan 3D scene completion |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 4.0/5 |
| Isaac Sim path | adapter needed; strong for Isaac mesh proxy if code matures。 |
| code/weights | 2.0/5 |
| priority score | 3.45/5 |
