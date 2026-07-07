# Stable Virtual Camera (SEVA): Generative View Synthesis with Diffusion Models

优先级：**P0** | 阅读深度：**deep** | 类别：**pose-conditioned large-angle NVS** | 综合分：**3.8/5**

## 资料状态
- 类型：paper+repo+weights
- 本地 PDF：ref/seva_stable_virtual_camera_iccv2025.pdf
- 本地 repo：repos/stable-virtual-camera
- commit：fe19948
- license 文件：LICENSE
- Sources:
- https://stable-virtual-camera.github.io
- https://github.com/Stability-AI/stable-virtual-camera
- https://huggingface.co/stabilityai/stable-virtual-camera
- https://openaccess.thecvf.com/content/ICCV2025/html/Zhou_Stable_Virtual_Camera_Generative_View_Synthesis_with_Diffusion_Models_ICCV_2025_paper.html

## 对 directional view coverage gap 的定位
第一优先级试验：在 A* 黑帧相机中心上指定反向 yaw target cameras，生成 pseudo views，再用 3DGS/PGSR 重训并检测 dark-frame ratio。

## Inputs / Outputs
- Inputs：任意数量 input views + target cameras/trajectory；可从 Go2 training poses 选定目标反向 yaw。
- Outputs：目标相机序列下的 RGB / multi-view video；不是 mesh 或 USD。

## Method Pipeline
- 把 input images 编码为条件，显式输入 target camera path。
- diffusion model 生成目标视角序列；sampling strategy 支持不同 view synthesis tasks。
- 输出结果可作为 pseudo observations 回灌到 3DGS/2DGS/PGSR 训练，或作为 novel-view data augmentation。

## Objectives / Losses
论文核心是 diffusion denoising objective + view/camera-conditioned training recipe；不直接优化 sim geometry 或 collision。

## Assumptions
输入视图与目标视角仍属于同一真实场景；模型允许 hallucination，因此需要 depth/pose/3DGS 重建做二次约束。

## Failure Modes
大角度下可能生成 plausible 但不 metric-correct 的内容；对细窄走廊的门、墙面、可通行边界可能产生语义漂移。

## Isaac Sim / 平台迁移判断
visual-only；最适合作为 short-term view completion generator，不适合作为 Isaac asset 直接来源。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | pose-conditioned large-angle NVS |
| camera-pose conditioning | 强 |
| large-angle support | 强 |
| 3D consistency | 4.1/5 |
| Isaac Sim path | visual-only；最适合作为 short-term view completion generator，不适合作为 Isaac asset 直接来源。 |
| code/weights | 4.2/5 |
| priority score | 3.8/5 |
