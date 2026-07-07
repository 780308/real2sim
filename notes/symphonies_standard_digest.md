# Symphonies: 3D Semantic Scene Completion with Contextual Instance Queries

优先级：**P1** | 阅读深度：**standard** | 类别：**semantic scene completion** | 综合分：**3.16/5**

## 资料状态
- 类型：paper+repo+weights
- 本地 PDF：ref/symphonies_2306_15670.pdf
- 本地 repo：repos/Symphonies
- commit：4ca4ff2
- license 文件：LICENSE
- Sources:
- https://github.com/hustvl/Symphonies
- https://arxiv.org/abs/2306.15670

## 对 directional view coverage gap 的定位
P1 低位，作为 occupancy prior 代表，不建议优先实现。

## Inputs / Outputs
- Inputs：camera images/depth predictions on SemanticKITTI/KITTI-360 style data。
- Outputs：3D semantic occupancy/voxels。

## Method Pipeline
- contextual instance queries 建模场景实例与上下文。
- 输出 semantic scene completion。

## Objectives / Losses
semantic voxel completion losses。

## Assumptions
自动驾驶数据域，室内/Isaac asset 需要转换。

## Failure Modes
不生成 texture / photorealistic novel view；仅作为语义/occupancy prior。

## Isaac Sim / 平台迁移判断
adapter needed。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | semantic scene completion |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 3.7/5 |
| Isaac Sim path | adapter needed。 |
| code/weights | 3.8/5 |
| priority score | 3.16/5 |
