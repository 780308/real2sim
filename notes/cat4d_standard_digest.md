# CAT4D: Create Anything in 4D with Multi-View Video Diffusion Models

优先级：**P1** | 阅读深度：**standard** | 类别：**dynamic multi-view video diffusion** | 综合分：**2.77/5**

## 资料状态
- 类型：paper
- 本地 PDF：ref/cat4d_cvpr2025.pdf
- 本地 repo：无
- commit：N/A
- license 文件：未在 repo 根目录确认
- Sources:
- https://cat-4d.github.io
- https://openaccess.thecvf.com/content/CVPR2025/html/Wu_CAT4D_Create_Anything_in_4D_with_Multi-View_Video_Diffusion_Models_CVPR_2025_paper.html

## 对 directional view coverage gap 的定位
P1。先不投入工程验证，等静态方向补全闭环成立后再回看。

## Inputs / Outputs
- Inputs：monocular video + specified camera poses/timestamps。
- Outputs：multi-view video for dynamic 4D scenes。

## Method Pipeline
- 从单目视频生成指定 camera/time 的多视角视频。
- 可扩展 ReaDy-Go 式 dynamic actor/obstacle，但当前问题先聚焦静态走廊。

## Objectives / Losses
multi-view video diffusion objective。

## Assumptions
动态能力强，但静态 directional gap 不是它最直接的目标。

## Failure Modes
可能过度关注时间变化；无直接 Isaac geometry/collision 输出。

## Isaac Sim / 平台迁移判断
visual-only；作为长期 dynamic extension。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | dynamic multi-view video diffusion |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 4.1/5 |
| Isaac Sim path | visual-only；作为长期 dynamic extension。 |
| code/weights | 1.2/5 |
| priority score | 2.77/5 |
