# LGM: Large Multi-View Gaussian Model for High-Resolution 3D Content Creation

## 定位
少数直接生成 3D Gaussians 的 object content model，可补 visual layer；mesh/collision仍需后处理。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.43/5 |
| family | single/text-to-3D Gaussian generation + mesh conversion |
| sources | https://github.com/3DTopia/LGM<br>https://arxiv.org/abs/2402.05054 |
| local_pdf | ref/lgm_2402_05054.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/LGM |
| commit / license | fe8d12c / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: text prompt or single-view image; multi-view diffusion generated views.
- Outputs: high-resolution 3D Gaussians, optional smooth textured mesh.

## Full Method Pipeline
- Generate multi-view images from image/text.
- Use asymmetric U-Net to predict multi-view Gaussian features.
- Fuse features into 3D Gaussians.
- Convert generated Gaussians to textured mesh if needed.

## Losses / Objectives
regression objectives on multi-view Gaussian reconstruction and rendering supervision.

## Assumptions
generated object prior may not match real object; scale/pose unknown。

## Failure Modes
mesh conversion耗时且可能不稳定；背面细节 hallucination。

## 对 Directional View Gap 的关系
可作为 object backside/visual layer prior。

## Isaac Sim Transfer
adapter needed: Gaussian visual + mesh conversion。

## 可迁移模块
- scene/object representation: single/text-to-3D Gaussian generation + mesh conversion
- view/object completion: 可作为 object backside/visual layer prior。
- geometry/collision: high-resolution 3D Gaussians, optional smooth textured mesh.
- simulator integration: adapter needed: Gaussian visual + mesh conversion。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 3DGS object generation baseline。

## Next Experiment
比较 LGM 直接生成 Gaussians 与 Hunyuan3D mesh+PBR 的 visual fidelity/mesh usability。
