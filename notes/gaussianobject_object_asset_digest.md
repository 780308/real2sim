# GaussianObject: High-Quality 3D Object Reconstruction from Four Views with Gaussian Splatting

## 定位
直接对应“单/少视角指定物体背面缺失”的补齐问题，是 object-level directional gap 的首选方法参考。

| 字段 | 内容 |
| --- | --- |
| priority / score | P0 / 3.91/5 |
| family | sparse-view object 3DGS / diffusion repair |
| sources | https://github.com/chensjtu/GaussianObject<br>https://gaussianobject.github.io/<br>https://arxiv.org/abs/2402.10259 |
| local_pdf | ref/gaussianobject_2402_10259.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/GaussianObject |
| commit / license | 91048a5 / n/a (cloned) |

## Inputs / Outputs
- Inputs: as few as 4 object images, masks, optional camera parameters / COLMAP-free path, monocular depth.
- Outputs: object-level 3D Gaussian representation and repaired novel-view renderings; mesh requires downstream extraction.

## Full Method Pipeline
- Build a visual hull from masked sparse views and camera parameters.
- Initialize and optimize 3D Gaussians with reference photometric loss plus floater elimination.
- Train a Gaussian repair model with leave-one-out corrupted renderings and 3D Gaussian noise pairs.
- Use repaired images to refine missing/compressed object information.

## Losses / Objectives
L_gs photometric/ref reconstruction, L_tune for diffusion repair tuning, L_rep for repaired-view refinement.

## Assumptions
需要目标物体 mask；物体基本封闭且视觉 hull 有意义；diffusion repair 可能生成 plausible 但非真实背面。

## Failure Modes
薄结构、透明/反光、强遮挡会破坏 visual hull；修复模型可能改变真实几何；不输出物理参数。

## 对 Directional View Gap 的关系
强相关：把 scene-level 反向 yaw 问题收束为 object backside / missing surface completion。

## Isaac Sim Transfer
adapter needed: 先用 SuGaR/2DGS/PGSR 或 mesh extraction 转 geometry，再做 collision proxy。

## 可迁移模块
- scene/object representation: sparse-view object 3DGS / diffusion repair
- view/object completion: 强相关：把 scene-level 反向 yaw 问题收束为 object backside / missing surface completion。
- geometry/collision: object-level 3D Gaussian representation and repaired novel-view renderings; mesh requires downstream extraction.
- simulator integration: adapter needed: 先用 SuGaR/2DGS/PGSR 或 mesh extraction 转 geometry，再做 collision proxy。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P0 object backside completion baseline；和 ObjectGS 输出的 object crop/mask 串联。

## Next Experiment
从 Go2 场景截取指定物体 4-8 个视角，跑 GaussianObject，比较背面 novel view 与 SuGaR mesh 是否优于普通 3DGS。
