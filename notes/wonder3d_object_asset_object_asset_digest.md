# Wonder3D: Single Image to 3D using Cross-Domain Diffusion

## 定位
normal maps对几何补全有帮助，可作为 object mesh generation baseline。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.37/5 |
| family | multi-view normal/color generation + mesh reconstruction |
| sources | https://github.com/xxlong0/Wonder3D<br>https://arxiv.org/abs/2310.15008 |
| local_pdf | ref/wonder3d_2310_15008.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/Wonder3D |
| commit / license | d894f82 / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: single object image.
- Outputs: consistent multi-view normal maps/color images and textured mesh.

## Full Method Pipeline
- Generate multi-view normals and colors with cross-domain diffusion.
- Use cross-domain attention for view/modality consistency.
- Fuse normals geometry-aware to extract surface.
- Texture reconstructed mesh.

## Losses / Objectives
diffusion losses over normal/color domains; surface fusion postprocess。

## Assumptions
single clean object image; generated normals may diverge from真实测量。

## Failure Modes
thin/reflective objects难；scale/collision absent。

## 对 Directional View Gap 的关系
背面 normal/color prior。

## Isaac Sim Transfer
adapter needed。

## 可迁移模块
- scene/object representation: multi-view normal/color generation + mesh reconstruction
- view/object completion: 背面 normal/color prior。
- geometry/collision: consistent multi-view normal maps/color images and textured mesh.
- simulator integration: adapter needed。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 mesh generation baseline，优先级低于 Hunyuan3D/InstantMesh。

## Next Experiment
仅在 Hunyuan3D/InstantMesh 失败时做替补测试。
