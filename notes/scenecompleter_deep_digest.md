# SceneCompleter: Dense 3D Scene Completion for Generative Novel View Synthesis

优先级：**P0** | 阅读深度：**deep** | 类别：**dense 3D completion for generative NVS** | 综合分：**3.55/5**

## 资料状态
- 类型：paper
- 本地 PDF：ref/scenecompleter_2506_10981.pdf
- 本地 repo：无
- commit：N/A
- license 文件：未在 repo 根目录确认
- Sources:
- https://arxiv.org/abs/2506.10981

## 对 directional view coverage gap 的定位
P0 方法参考，工程上排在有代码的 SEVA/GEN3C/PGSR/OpenReal2Sim 之后。

## Inputs / Outputs
- Inputs：partial 3D / generated novel-view context；关注 2D inpainting 导致 geometry distortion 的问题。
- Outputs：dense completed 3D scene representation for NVS。

## Method Pipeline
- 先补 dense 3D scene，而不是逐帧 2D inpainting。
- 用完整 3D 表示约束 generative novel view synthesis，降低 appearance drift。
- 更适合在 3DGS 黑洞处生成结构先验，再渲染多视角。

## Objectives / Losses
3D completion + generative NVS consistency；论文强调避免 2D inpainting paradigm 的几何漂移。

## Assumptions
代码状态不明；需要验证输入格式是否能接 Go2 3DGS/point cloud。

## Failure Modes
若场景拓扑先验错误，所有补视角会一致地错；需 uncertainty map 和 active re-capture 对照。

## Isaac Sim / 平台迁移判断
adapter needed；比纯 world model 更适合 Isaac 的几何中间层。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | dense 3D completion for generative NVS |
| camera-pose conditioning | 强 |
| large-angle support | 强 |
| 3D consistency | 4.5/5 |
| Isaac Sim path | adapter needed；比纯 world model 更适合 Isaac 的几何中间层。 |
| code/weights | 1.2/5 |
| priority score | 3.55/5 |
