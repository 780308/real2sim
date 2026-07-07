# Hunyuan3D-Omni: A Unified Framework for Controllable Generation of 3D Assets

## 定位
比普通 image-to-3D 更适合 real2sim，因为可以用 point cloud/bbox 约束生成几何和比例。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.99/5 |
| family | controllable 3D asset generation with point/bbox/voxel/skeleton controls |
| sources | https://github.com/Tencent-Hunyuan/Hunyuan3D-Omni<br>https://arxiv.org/abs/2509.21245<br>https://huggingface.co/tencent/Hunyuan3D-Omni |
| local_pdf | ref/hunyuan3d_omni_2509_21245.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/Hunyuan3D-Omni |
| commit / license | 4d47c0c / License.txt (cloned) |

## Inputs / Outputs
- Inputs: image plus optional point cloud, voxel, bounding box, or skeleton controls.
- Outputs: controlled 3D mesh assets from Hunyuan3D 2.1-style latent diffusion.

## Full Method Pipeline
- Encode additional controls through unified control encoder.
- Fuse image and structured controls in DiT/VAE generation path.
- Generate geometry constrained by point cloud/bbox/voxel/skeleton.
- Use output mesh as completion prior subject to registration and rejection.

## Losses / Objectives
flow matching / diffusion objective conditioned on image and structured controls.

## Assumptions
控制信号质量高；生成结果仍是 prior 而非测量；weights/VRAM 需求高。

## Failure Modes
point cloud sparse/noisy 时生成偏差；bbox 只约束比例不约束细节；拓扑可能变化。

## 对 Directional View Gap 的关系
适合作为物体未观测面的 controlled completion，优先级高于纯 open world model。

## Isaac Sim Transfer
adapter needed: mesh output 可转 USD/GLB，collision/physics 另接 PhysX/ScalableReal2Sim。

## 可迁移模块
- scene/object representation: controllable 3D asset generation with point/bbox/voxel/skeleton controls
- view/object completion: 适合作为物体未观测面的 controlled completion，优先级高于纯 open world model。
- geometry/collision: controlled 3D mesh assets from Hunyuan3D 2.1-style latent diffusion.
- simulator integration: adapter needed: mesh output 可转 USD/GLB，collision/physics 另接 PhysX/ScalableReal2Sim。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1+ generative completion prior；若 Hunyuan3D-2.1 不够受约束，升级到 Omni。

## Next Experiment
用真实 object point cloud + bbox 作为 control，生成完整 mesh，做 ICP/reprojection/free-space reject test。
