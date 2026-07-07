# CAT3D: Create Anything in 3D with Multi-View Diffusion Models

优先级：**P0** | 阅读深度：**deep** | 类别：**multi-view diffusion for reconstruction input synthesis** | 综合分：**3.24/5**

## 资料状态
- 类型：paper
- 本地 PDF：ref/cat3d_2405_10314.pdf
- 本地 repo：无
- commit：N/A
- license 文件：未在 repo 根目录确认
- Sources:
- https://cat3d.github.io
- https://arxiv.org/abs/2405.10314

## 对 directional view coverage gap 的定位
保留为强方法参考，短期优先使用有代码/权重的 SEVA/GEN3C 替代。

## Inputs / Outputs
- Inputs：任意数量 input images + target novel viewpoints。
- Outputs：multi-view consistent generated views，可送入 3D reconstruction。

## Method Pipeline
- 模拟真实 capture process：从少量输入合成一批目标相机视角。
- 把生成视图交给已有 3D reconstruction 技术产出 3D representation。
- 适合补齐 Go2 未覆盖 yaw 后再训练 3DGS/mesh。

## Objectives / Losses
multi-view diffusion generation objective；不直接估计物理属性。

## Assumptions
公开资料以论文/项目页为主，代码可用性不足；更适合作为策略范式而非第一工程依赖。

## Failure Modes
可能生成与真实局部不完全一致的 backside content；无显式 collision guarantee。

## Isaac Sim / 平台迁移判断
adapter needed；作为 pseudo-view synthesis 前端。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | multi-view diffusion for reconstruction input synthesis |
| camera-pose conditioning | 强 |
| large-angle support | 强 |
| 3D consistency | 4.4/5 |
| Isaac Sim path | adapter needed；作为 pseudo-view synthesis 前端。 |
| code/weights | 1.2/5 |
| priority score | 3.24/5 |
