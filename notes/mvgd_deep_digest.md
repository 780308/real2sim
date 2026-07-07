# MVGD: Zero-Shot Novel View and Depth Synthesis with Multi-View Geometric Diffusion

优先级：**P0** | 阅读深度：**deep** | 类别：**novel view + scale-consistent depth synthesis** | 综合分：**3.56/5**

## 资料状态
- 类型：paper
- 本地 PDF：ref/mvgd_cvpr2025.pdf
- 本地 repo：无
- commit：N/A
- license 文件：未在 repo 根目录确认
- Sources:
- https://openaccess.thecvf.com/content/CVPR2025/html/Guizilini_Zero-Shot_Novel_View_and_Depth_Synthesis_with_Multi-View_Geometric_Diffusion_CVPR_2025_paper.html

## 对 directional view coverage gap 的定位
若官方或第三方实现可用，应升级为 SEVA/GEN3C 后的第二个验证模块。

## Inputs / Outputs
- Inputs：sparse posed images / target viewpoints。
- Outputs：novel RGB + scale-consistent depth maps。

## Method Pipeline
- 用 geometric diffusion 直接生成目标视角 RGB 和 depth，而不是先建完整 radiance field。
- 输出 depth 使 pseudo-view 不只停留在 RGB，可以参与 TSDF、mesh、PGSR 或 Isaac collision proxy。
- zero-shot 设定降低重新训练成本，但工程可复现性取决于代码/权重公开状态。

## Objectives / Losses
diffusion generation objective + multi-view geometric/depth consistency 约束。

## Assumptions
论文路线很适合本问题，但本轮未找到完整官方 repo；只能作为方法强参考。

## Failure Modes
若代码不可用，短期落地弱；depth 虽 scale-consistent，仍需和 Go2 metric scale / point cloud 校准。

## Isaac Sim / 平台迁移判断
adapter needed；比纯 RGB NVS 更接近 Isaac，因为 depth 可参与 mesh/collision。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | novel view + scale-consistent depth synthesis |
| camera-pose conditioning | 强 |
| large-angle support | 强 |
| 3D consistency | 4.7/5 |
| Isaac Sim path | adapter needed；比纯 RGB NVS 更接近 Isaac，因为 depth 可参与 mesh/collision。 |
| code/weights | 1.5/5 |
| priority score | 3.56/5 |
