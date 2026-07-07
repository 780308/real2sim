# GEN3C: 3D-Informed World-Consistent Video Generation with Precise Camera Control

优先级：**P0** | 阅读深度：**deep** | 类别：**3D-informed camera-controlled world-consistent video** | 综合分：**3.94/5**

## 资料状态
- 类型：paper+repo+weights
- 本地 PDF：ref/gen3c_3d_informed_world_consistent_video_generation.pdf
- 本地 repo：repos/GEN3C
- commit：db2ffe1
- license 文件：LICENSE
- Sources:
- https://research.nvidia.com/labs/toronto-ai/GEN3C/
- https://github.com/nv-tlabs/GEN3C
- https://huggingface.co/nvidia/GEN3C-Cosmos-7B

## 对 directional view coverage gap 的定位
与 SEVA 并列 P0。若算力允许，优先用 GEN3C 做 camera-controlled 反向 yaw 补帧，因为它的问题表述最贴合 directional view gap。

## Inputs / Outputs
- Inputs：single/multi-view image, camera path, depth/pose informed conditioning；README 支持 interactive GUI author arbitrary camera trajectories。
- Outputs：camera-controlled video / novel views；后续版本还关联 Lyra static/dynamic 3DGS decoder。

## Method Pipeline
- 先用 3D information 帮模型理解已观测结构，而不是只靠 pose token。
- 在推理时给定任意 camera trajectory，模型把生成能力集中到 unobserved regions 和时序推进。
- 可通过 multi-view inference 或 video-to-video pipeline 与真实采集片段对齐。

## Objectives / Losses
视频扩散/生成 objective，强调 temporal 3D consistency 和 precise camera control；不是显式 geometry loss 的重建器。

## Assumptions
需要大模型权重和较高 GPU 资源；license 包括 NVIDIA Open Model License，需要确认项目合规。

## Failure Modes
视频一致性强于普通 video model，但仍可能在 metric scale、障碍物边界和地面可通行区域上不可靠。

## Isaac Sim / 平台迁移判断
visual-only / pseudo-view generator；若结合 Lyra 或 3DGS decoder，可作为中期 3DGS 修复方向。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | 3D-informed camera-controlled world-consistent video |
| camera-pose conditioning | 强 |
| large-angle support | 强 |
| 3D consistency | 4.5/5 |
| Isaac Sim path | visual-only / pseudo-view generator；若结合 Lyra 或 3DGS decoder，可作为中期 3DGS 修复方向。 |
| code/weights | 4.3/5 |
| priority score | 3.94/5 |
