# Hunyuan3D 2.1: From Images to High-Fidelity 3D Assets with Production-Ready PBR Material

## 定位
师兄提到的 Hunyuan3D 路线：适合作为物体背面/完整形状/PBR texture prior，而不是无约束替代真实扫描。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.89/5 |
| family | image-to-3D mesh + PBR texture generation |
| sources | https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1<br>https://arxiv.org/abs/2506.15442<br>https://huggingface.co/tencent/Hunyuan3D-2.1 |
| local_pdf | ref/hunyuan3d_2_1_2506_15442.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/Hunyuan3D-2.1 |
| commit / license | 82920d6 / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: single object image; optional custom mesh for Hunyuan3D-Paint texture synthesis.
- Outputs: high-resolution polygon mesh, PBR material maps/albedo/metallic/roughness textures.

## Full Method Pipeline
- Use Hunyuan3D-DiT and ShapeVAE for image-conditioned shape generation.
- Decode latent tokens into polygon mesh.
- Use Hunyuan3D-Paint multi-view PBR diffusion to synthesize light-free, view-consistent material maps.
- Export textured mesh for downstream asset pipeline.

## Losses / Objectives
flow matching/diffusion objective for shape; multi-view PBR texture diffusion losses and alignment modules.

## Assumptions
输入需是清晰单物体图；生成 mesh 未必 metric-aligned，需用真实 point cloud / bbox / scale 对齐。

## Failure Modes
会 hallucinate 与真实物体不一致的背面、尺寸或拓扑；collision 需要简化且物理参数缺失。

## 对 Directional View Gap 的关系
强 visual backside prior；必须通过 real depth/point cloud reject test。

## Isaac Sim Transfer
adapter needed but promising: mesh + PBR maps 可转 USD/GLB，collision 和 scale 需后处理。

## 可迁移模块
- scene/object representation: image-to-3D mesh + PBR texture generation
- view/object completion: 强 visual backside prior；必须通过 real depth/point cloud reject test。
- geometry/collision: high-resolution polygon mesh, PBR material maps/albedo/metallic/roughness textures.
- simulator integration: adapter needed but promising: mesh + PBR maps 可转 USD/GLB，collision 和 scale 需后处理。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1/P0 边界的 generative object prior；用于低覆盖面的补全候选。

## Next Experiment
对同一物体输入正面 crop 生成 mesh/PBR，再按真实点云 scale/ICP 对齐，和 GaussianObject 的 3DGS 补面结果比较。
