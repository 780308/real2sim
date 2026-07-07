# TripoSR: Fast 3D Object Reconstruction from a Single Image

## 定位
速度极快，适合当 sanity check baseline，而非高保真主线。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.42/5 |
| family | ultra-fast single-image object mesh reconstruction |
| sources | https://github.com/VAST-AI-Research/TripoSR<br>https://arxiv.org/abs/2403.02151<br>https://huggingface.co/stabilityai/TripoSR |
| local_pdf | ref/triposr_2403_02151.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/TripoSR |
| commit / license | 107cefd / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: single object image.
- Outputs: mesh from feed-forward triplane/LRM-style reconstruction in under 0.5s on A100.

## Full Method Pipeline
- Encode image with transformer model.
- Decode image tokens into triplane-NeRF representation.
- Extract mesh with texture/vertex color.
- Use as fast object shape prior.

## Losses / Objectives
mask/color/rendering reconstruction losses in LRM training.

## Assumptions
物体居中干净；几何细节/真实对齐要求不高。

## Failure Modes
shape oversmoothing, scale unknown, physical/collision absent。

## 对 Directional View Gap 的关系
粗略背面先验。

## Isaac Sim Transfer
adapter needed; mesh需后处理。

## 可迁移模块
- scene/object representation: ultra-fast single-image object mesh reconstruction
- view/object completion: 粗略背面先验。
- geometry/collision: mesh from feed-forward triplane/LRM-style reconstruction in under 0.5s on A100.
- simulator integration: adapter needed; mesh需后处理。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1/P2 快速 baseline。

## Next Experiment
把 TripoSR 作为 1 秒级低成本对照，判断复杂方法是否真正提升。
