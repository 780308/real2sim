# HY-World 2.0: Multi-Modal World Model for 3D World Generation and Reconstruction

优先级：**P1** | 阅读深度：**standard** | 类别：**open 3D world model** | 综合分：**3.69/5**

## 资料状态
- 类型：tech report+repo+weights
- 本地 PDF：ref/hy_world_2_0_tech_report.pdf
- 本地 repo：repos/HY-World-2.0
- commit：7f668e6
- license 文件：License.txt
- Sources:
- https://3d.hunyuan.tencent.com/sceneTo3D
- https://github.com/Tencent-Hunyuan/HY-World-2.0

## 对 directional view coverage gap 的定位
P1 强候选：作为 semantic/geometry prior，不作为第一主线。

## Inputs / Outputs
- Inputs：text, single-view image, multi-view images, video。
- Outputs：3D world representations: meshes / 3DGS / point cloud / depth / normals / camera parameters。

## Method Pipeline
- World Generation: HY-Pano 2.0 -> WorldNav -> WorldStereo 2.0 -> WorldMirror 2.0 + 3DGS learning。
- World Reconstruction: WorldMirror 2.0 feed-forward predicts depth, normals, camera, point cloud, 3DGS attributes。
- README 明确可导入 Blender/Unity/Unreal/Isaac 类引擎。

## Objectives / Losses
多模型组合 world generation/reconstruction；报告重在系统能力而非单一 loss。

## Assumptions
世界模型会生成 plausible 3D world，但未必 metric-align 到 Go2 真实走廊；需要真实几何约束和局部锁定。

## Failure Modes
可能改变拓扑/物体布局；如果无约束替换原场景，会损害 real2sim fidelity。

## Isaac Sim / 平台迁移判断
adapter needed but promising；mesh/3DGS 输出和 Isaac 兼容表述使其比纯 video world model 更有用。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | open 3D world model |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 3.5/5 |
| Isaac Sim path | adapter needed but promising；mesh/3DGS 输出和 Isaac 兼容表述使其比纯 video world model 更有用。 |
| code/weights | 4.2/5 |
| priority score | 3.69/5 |
