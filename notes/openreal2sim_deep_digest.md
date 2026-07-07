# OpenReal2Sim: Toolbox for Real-to-Sim Reconstruction and Robotic Simulation

优先级：**P0** | 阅读深度：**deep** | 类别：**sim-ready real2sim toolbox** | 综合分：**4.17/5**

## 资料状态
- 类型：repo
- 本地 PDF：无 / 技术项目
- 本地 repo：repos/OpenReal2Sim
- commit：8f69a19
- license 文件：LICENSE
- Sources:
- https://github.com/PointsCoder/OpenReal2Sim

## 对 directional view coverage gap 的定位
P0 平台主线。把 NVS/scene-completion 模块接在 preprocess/reconstruction 之间，最终走 USD conversion。

## Inputs / Outputs
- Inputs：single image / monocular video / GT depth image；preprocess 得到 metric depth、intrinsics/extrinsics、dynamic point clouds。
- Outputs：background/object meshes, scene.json, GLB/mesh assets, IsaacLab USD conversion, grasp/trajectory demos。

## Method Pipeline
- preprocess: image extraction, metric depth prediction/calibration, camera estimation。
- reconstruction: object segmentation, background pixel/point inpainting, background/object mesh generation, scenario construction, pose/collision optimization。
- simulation: IsaacLab USD conversion, Maniskill/MuJoCo support, trajectory replay and heuristic manipulation。

## Objectives / Losses
系统 pipeline；核心是 mesh/scene construction 和 simulator import，不是 NVS loss。

## Assumptions
非常贴合最终 Isaac Sim 目标，但更多面向 object-centric manipulation；需要改造成走廊/导航场景。

## Failure Modes
background inpainting/point inpainting 可能过于单图/局部；未显式解决 large-angle camera-conditioned view consistency。

## Isaac Sim / 平台迁移判断
direct for IsaacLab/Isaac Sim path；是本项目 mid-term integration anchor。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | sim-ready real2sim toolbox |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 3.6/5 |
| Isaac Sim path | direct for IsaacLab/Isaac Sim path；是本项目 mid-term integration anchor。 |
| code/weights | 4.5/5 |
| priority score | 4.17/5 |
