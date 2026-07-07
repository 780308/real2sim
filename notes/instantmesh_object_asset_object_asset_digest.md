# InstantMesh: Efficient 3D Mesh Generation from a Single Image with Sparse-view Large Reconstruction Models

## 定位
快速 single-image mesh baseline，适合做 Hunyuan3D 的轻量替代或 ablation。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.71/5 |
| family | single-image mesh generation baseline |
| sources | https://github.com/TencentARC/InstantMesh<br>https://arxiv.org/abs/2404.07191<br>https://huggingface.co/TencentARC/InstantMesh |
| local_pdf | ref/instantmesh_2404_07191.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/InstantMesh |
| commit / license | 08822c5 / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: single object image / alpha mask.
- Outputs: textured mesh / OBJ with vertex colors or texture map.

## Full Method Pipeline
- Generate 3D-consistent sparse multi-view images using diffusion.
- Feed sparse views into LRM-style reconstruction model.
- Use differentiable iso-surface extraction/FlexiCubes for direct mesh output.
- Export OBJ/textured mesh within seconds.

## Losses / Objectives
multi-view diffusion objectives and reconstruction losses over mesh/depth/normal supervision.

## Assumptions
输入是干净单物体；输出未保证真实场景对齐。

## Failure Modes
生成背面可能错误；mesh 细节/scale/collision 需后处理。

## 对 Directional View Gap 的关系
可补单物体背面，需 reject test。

## Isaac Sim Transfer
adapter needed: OBJ/mesh 可导入但需 scale/material/collision。

## 可迁移模块
- scene/object representation: single-image mesh generation baseline
- view/object completion: 可补单物体背面，需 reject test。
- geometry/collision: textured mesh / OBJ with vertex colors or texture map.
- simulator integration: adapter needed: OBJ/mesh 可导入但需 scale/material/collision。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 quick generative mesh baseline。

## Next Experiment
同一 object crop 跑 InstantMesh/Hunyuan3D/GaussianObject，比较 mesh vs 3DGS visual layer。
