# EmbodiedGen: Towards a Generative 3D World Engine for Embodied AI

## 定位
长期方向：帮助扩充资产库和低置信区域先验，不替代真实指定物体。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.0/5 |
| family | generative embodied 3D world / asset prior |
| sources | https://github.com/HorizonRobotics/EmbodiedGen<br>https://arxiv.org/abs/2506.10600 |
| local_pdf | ref/embodiedgen_2506_10600.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/EmbodiedGen |
| commit / license | 658cd3f / n/a (cloned) |

## Inputs / Outputs
- Inputs: generative prompts/conditions for embodied scenes/assets.
- Outputs: 3D worlds/assets for embodied AI; varies by release.

## Full Method Pipeline
- Use generative models to create embodied 3D assets/worlds.
- Provide assets/scene priors for simulation data scaling.
- Potentially combine mesh/3DGS/physics outputs depending module.
- Requires registration to real scenes for real2sim use.

## Losses / Objectives
generative model training objectives; not tightly tied to our real scene.

## Assumptions
需要生成而非忠实重建；真实对齐弱。

## Failure Modes
可能生成好看但不真实的场景/物体；physics correctness 不确定。

## 对 Directional View Gap 的关系
作为 semantic/visual prior。

## Isaac Sim Transfer
adapter needed。

## 可迁移模块
- scene/object representation: generative embodied 3D world / asset prior
- view/object completion: 作为 semantic/visual prior。
- geometry/collision: 3D worlds/assets for embodied AI; varies by release.
- simulator integration: adapter needed。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1/P2 long-term generative prior。

## Next Experiment
仅用于补默认资产库或低置信候选，不纳入短期闭环。
