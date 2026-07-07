# SAGE-3D: Towards Physically Executable 3D Gaussian for Embodied Navigation

## 定位
虽是导航而非 manipulation，但它系统化验证了 object-level semantics + collision bodies + 3DGS visual layer 的必要性。

| 字段 | 内容 |
| --- | --- |
| priority / score | P0 / 3.88/5 |
| family | semantically and physically aligned 3DGS environment |
| sources | https://github.com/Galery23/SAGE-3D_Official<br>https://arxiv.org/abs/2510.21307<br>https://sage-3d.github.io/ |
| local_pdf | ref/sage_3d_2510_21307.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/SAGE-3D_Official |
| commit / license | 1b841f2 / n/a (cloned) |

## Inputs / Outputs
- Inputs: 3DGS indoor scenes, object annotations, mesh scenes/collision bodies, Isaac Sim 5.0+.
- Outputs: InteriorGS object-annotated 3DGS scenes, collision meshes, USDZ assets, VLN benchmark.

## Full Method Pipeline
- Ground object-level semantics into 3DGS scenes.
- Extract collision bodies for each object from mesh sources.
- Use 3DGS-Mesh hybrid representation: 3DGS for appearance, mesh collision for physics.
- Run embodied navigation benchmark in Isaac Sim 5.0+.

## Losses / Objectives
dataset/benchmark construction; policy training uses VLN losses/rewards; not a reconstruction-loss paper.

## Assumptions
数据来自 artist-created mesh scenes rather than real scans；对真实 Go2 场景需构建 equivalent asset pipeline。

## Failure Modes
可执行性来自已有 mesh，不是从坏 3DGS 自动恢复；navigation collision 简化不等于 manipulation contact 精度。

## 对 Directional View Gap 的关系
不补视角，但证明 3DGS 必须和 object/collision layer 对齐才能用于 embodied tasks。

## Isaac Sim Transfer
direct: README 明确 Isaac Sim 5.0+，并有 USDZ/Collision Mesh datasets。

## 可迁移模块
- scene/object representation: semantically and physically aligned 3DGS environment
- view/object completion: 不补视角，但证明 3DGS 必须和 object/collision layer 对齐才能用于 embodied tasks。
- geometry/collision: InteriorGS object-annotated 3DGS scenes, collision meshes, USDZ assets, VLN benchmark.
- simulator integration: direct: README 明确 Isaac Sim 5.0+，并有 USDZ/Collision Mesh datasets。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P0 Isaac 5.0 视觉/物理混合环境参考；对 Go2 导航平台非常相关。

## Next Experiment
参考 InteriorGS 数据格式，为一个 Go2 room scene 生成 object annotation + collision body + 3DGS visual package。
