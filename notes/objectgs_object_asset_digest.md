# ObjectGS: Object-aware Scene Reconstruction and Scene Understanding via Gaussian Splatting

## 定位
解决“指定物体”如何从整场景 3DGS 中分离出来，是 object-level asset pipeline 的前端。

| 字段 | 内容 |
| --- | --- |
| priority / score | P0 / 3.93/5 |
| family | object-aware Gaussian reconstruction / instance extraction |
| sources | https://github.com/RuijieZhu94/ObjectGS<br>https://ruijiezhu94.github.io/ObjectGS_page/<br>https://arxiv.org/abs/2507.15454 |
| local_pdf | ref/objectgs_2507_15454.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/ObjectGS |
| commit / license | 16dfc2f / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: posed multi-view RGB, SAM/2D segmentation labels, object IDs; supports 3DGS and 2DGS variants.
- Outputs: object-aware neural Gaussians, 2D/3D semantic rendering, single-object rendering, scene/object mesh export.

## Full Method Pipeline
- Use 2D segmentation pipeline to assign object IDs and lift them to 3D by voting.
- Initialize anchors and generate object-aware neural Gaussians per object.
- Attach deterministic one-hot object ID semantics and use classification constraints during reconstruction.
- Render single objects or export object meshes via query_label_id.

## Losses / Objectives
photometric reconstruction loss plus object-ID classification/semantic constraints; anchor grow/prune controls object geometry coverage.

## Assumptions
2D masks跨视角一致性足够；目标物体在多视角中有可见区域；dataset preprocessing 成本不低。

## Failure Modes
SAM/DEVA mask 错误会污染 object IDs；离散 ID 会遇到细小接触物体边界粘连；mesh export 质量仍受 3DGS surface quality 限制。

## 对 Directional View Gap 的关系
本身不补背面，但能把需要补齐的 object subset 精确抽出来再送 GaussianObject/Hunyuan3D/SuGaR。

## Isaac Sim Transfer
adapter needed: object mesh export 后可进入 USD/collision，object Gaussians 可作 visual layer。

## 可迁移模块
- scene/object representation: object-aware Gaussian reconstruction / instance extraction
- view/object completion: 本身不补背面，但能把需要补齐的 object subset 精确抽出来再送 GaussianObject/Hunyuan3D/SuGaR。
- geometry/collision: object-aware neural Gaussians, 2D/3D semantic rendering, single-object rendering, scene/object mesh export.
- simulator integration: adapter needed: object mesh export 后可进入 USD/collision，object Gaussians 可作 visual layer。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P0 object selection/extraction 工具；优先用于门、椅子、桌子等指定物体分离。

## Next Experiment
在现有 Go2 场景中标注/检测一个椅子或门，用 ObjectGS 输出 query object mesh 与 object-only Gaussians，再检查导入 Isaac 的可分离性。
