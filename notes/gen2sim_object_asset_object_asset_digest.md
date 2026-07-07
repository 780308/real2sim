# Gen2Sim: Scaling up Robot Learning in Simulation with Generative Models

## 定位
概念上支持生成式资产库，但与真实指定物体 fidelity 不匹配。

| 字段 | 内容 |
| --- | --- |
| priority / score | P2 / 2.49/5 |
| family | generative simulation asset/data scaling |
| sources | https://arxiv.org/abs/2310.18308 |
| local_pdf | ref/gen2sim_2310_18308.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | 无 |
| commit / license | n/a / n/a (no-repo) |

## Inputs / Outputs
- Inputs: generative model-created objects/scenes/tasks.
- Outputs: simulation assets/tasks for robot learning.

## Full Method Pipeline
- Use generative models to create diverse simulation objects/scenes.
- Train robot policies in generated simulation.
- Evaluate sim-to-real/task generalization.
- Iterate generation/evaluation.

## Losses / Objectives
policy learning objectives; generative losses outside focus.

## Assumptions
目标是 diversity 而非 real2sim accuracy。

## Failure Modes
不保证 Isaac-ready object/collision。

## 对 Directional View Gap 的关系
无直接关系。

## Isaac Sim Transfer
indirect。

## 可迁移模块
- scene/object representation: generative simulation asset/data scaling
- view/object completion: 无直接关系。
- geometry/collision: simulation assets/tasks for robot learning.
- simulator integration: indirect。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P2 背景参考。

## Next Experiment
不投入短期复现。
