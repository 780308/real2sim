# CRM: Single Image to 3D Textured Mesh with Convolutional Reconstruction Model

## 定位
和 InstantMesh 同类，但直接 textured mesh，适合作为 asset generation baseline。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.42/5 |
| family | single-image textured mesh generation |
| sources | https://github.com/thu-ml/CRM<br>https://arxiv.org/abs/2403.05034 |
| local_pdf | ref/crm_2403_05034.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/CRM |
| commit / license | 4964e36 / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: single image; foreground preprocessing/grey background recommended.
- Outputs: textured OBJ mesh, multi-view generated images, canonical coordinate maps.

## Full Method Pipeline
- Generate six orthographic views with multi-view diffusion.
- Generate canonical coordinate maps.
- Feed views and CCMs into convolutional reconstruction model.
- Optimize/export textured mesh with UV texture.

## Losses / Objectives
multi-view diffusion and mesh reconstruction objectives with FlexiCubes.

## Assumptions
clean object crop; no real metric scale。

## Failure Modes
background preprocessing敏感；背面 hallucination；collision需重建。

## 对 Directional View Gap 的关系
可补单物体未见面但须验证。

## Isaac Sim Transfer
adapter needed。

## 可迁移模块
- scene/object representation: single-image textured mesh generation
- view/object completion: 可补单物体未见面但须验证。
- geometry/collision: textured OBJ mesh, multi-view generated images, canonical coordinate maps.
- simulator integration: adapter needed。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 generative mesh baseline。

## Next Experiment
对 Hunyuan3D/InstantMesh/CRM 输出进行 ICP+collision proxy 比较。
