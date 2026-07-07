# LingBot-World: Open-Source World Simulator from Video Generation

优先级：**P1** | 阅读深度：**standard** | 类别：**camera/action-conditioned video world model** | 综合分：**3.31/5**

## 资料状态
- 类型：paper+repo+weights
- 本地 PDF：ref/lingbot_world_2601_20540.pdf
- 本地 repo：repos/lingbot-world
- commit：7ee84e1
- license 文件：LICENSE.txt
- Sources:
- https://github.com/robbyant/lingbot-world
- https://huggingface.co/collections/robbyant/lingbot-world
- https://arxiv.org/abs/2601.20540

## 对 directional view coverage gap 的定位
P1。作为开放 world model 对照组，比较它和 SEVA/GEN3C 在反向 yaw pseudo views 的漂移差异。

## Inputs / Outputs
- Inputs：initial frames + camera poses or actions；README 使用 poses.npy [num_frames,4,4] OpenCV transforms。
- Outputs：long-horizon camera/action-conditioned videos。

## Method Pipeline
- Base(Cam) / Base(Act) / Fast 模型支持 camera poses 或 actions。
- 用 run scripts 生成长时域视频。
- 可用于模拟反向 camera motion，但不产生 3D assets。

## Objectives / Losses
video world model generation objective。

## Assumptions
camera-conditioned 是亮点；但 geometry anchoring 比 SEVA/GEN3C 弱。

## Failure Modes
长视频可能保持视觉连续但不保持 metric scene structure；不可直接用于 Isaac collision。

## Isaac Sim / 平台迁移判断
visual-only。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | camera/action-conditioned video world model |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 3.4/5 |
| Isaac Sim path | visual-only。 |
| code/weights | 4.2/5 |
| priority score | 3.31/5 |
