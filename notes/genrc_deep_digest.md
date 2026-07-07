# GenRC: Generative 3D Room Completion from Sparse Image Collections

优先级：**P0** | 阅读深度：**deep** | 类别：**room-scale RGB-D mesh completion** | 综合分：**3.55/5**

## 资料状态
- 类型：paper
- 本地 PDF：ref/genrc_eccv2024.pdf
- 本地 repo：无
- commit：N/A
- license 文件：未在 repo 根目录确认
- Sources:
- https://minfenli.github.io/GenRC/
- https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/5406_ECCV_2024_paper.php

## 对 directional view coverage gap 的定位
作为 mid-term 主线：补视觉后，GenRC/SceneCompleter/Seen2Scene 负责把低覆盖区域转成物理几何假设。

## Inputs / Outputs
- Inputs：sparse RGB-D images / sparse image collections。
- Outputs：room-scale completed 3D mesh with texture。

## Method Pipeline
- 把 sparse RGB-D 投影为 highly incomplete 3D mesh。
- 用 E-Diffusion 生成 view-consistent panoramic RGB-D，保证 global geometry/appearance consistency。
- 把补全后的 panoramic RGB-D 融合为完整 room mesh。

## Objectives / Losses
training-free pipeline，核心依赖 diffusion prior 和 RGB-D consistency；不是 end-to-end supervised scene completion。

## Assumptions
非常贴合室内/走廊，且输出 mesh；但本轮未确认官方代码完整可用。

## Failure Modes
completion 可能补出合理但错误的房间拓扑；门后/转角等 high uncertainty 区域要标注置信度。

## Isaac Sim / 平台迁移判断
adapter needed but strong；mesh 输出最接近 Isaac USD/collision proxy。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | room-scale RGB-D mesh completion |
| camera-pose conditioning | 强 |
| large-angle support | 强 |
| 3D consistency | 4.0/5 |
| Isaac Sim path | adapter needed but strong；mesh 输出最接近 Isaac USD/collision proxy。 |
| code/weights | 1.4/5 |
| priority score | 3.55/5 |
