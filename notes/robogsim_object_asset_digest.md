# RoboGSim: A Real2Sim2Real Robotic Gaussian Splatting Simulator

## 定位
与师兄任务描述几乎同构，但代码证据弱于 GSWorld/Re3Sim；适合作为系统 taxonomy 和指标参考。

| 字段 | 内容 |
| --- | --- |
| priority / score | P0 / 3.73/5 |
| family | R2S2R Gaussian reconstructor + digital twins builder |
| sources | https://arxiv.org/abs/2411.11839<br>https://robogsim.github.io/ |
| local_pdf | ref/robogsim_2411_11839.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | 无 |
| commit / license | n/a / n/a (no-repo) |

## Inputs / Outputs
- Inputs: multi-view RGB image sequences, robotic arm MDH parameters, real layout measurements.
- Outputs: 3DGS scene/object reconstruction, mesh reconstruction, layout-aligned digital twin in Isaac Sim, novel view/object/trajectory simulated data.

## Full Method Pipeline
- Gaussian Reconstructor builds 3DGS scene/objects and segments robotic arm.
- Digital Twins Builder reconstructs scene/object meshes and aligns real/sim/GS coordinate spaces.
- Scene Composer synthesizes novel objects, scenes and views.
- Interactive Engine connects Isaac Sim collision/kinematics with GS renderer feedback to policy.

## Losses / Objectives
3DGS reconstruction losses, mesh reconstruction objectives, policy/evaluation metrics for sim2real consistency.

## Assumptions
需要 MDH/robot setup 和 layout measurements；digital twin builder 的实现可用性需进一步核验。

## Failure Modes
如果没有代码，短期复现成本高；layout alignment 误差会直接导致 grasp/collision mismatch。

## 对 Directional View Gap 的关系
可以生成 novel views，但不是针对 unseen backside completion 的方法。

## Isaac Sim Transfer
direct conceptually: 明确使用 Isaac Sim 做 digital twin；工程落地需找完整代码。

## 可迁移模块
- scene/object representation: R2S2R Gaussian reconstructor + digital twins builder
- view/object completion: 可以生成 novel views，但不是针对 unseen backside completion 的方法。
- geometry/collision: 3DGS scene/object reconstruction, mesh reconstruction, layout-aligned digital twin in Isaac Sim, novel view/object/trajectory simulated data.
- simulator integration: direct conceptually: 明确使用 Isaac Sim 做 digital twin；工程落地需找完整代码。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P0 方法论参考，工程优先级排在 GSWorld/Re3Sim 后。

## Next Experiment
抽取其四模块接口，映射到本项目：Gaussian Reconstructor/Object Extractor/Isaac Asset Builder/Interactive Evaluator。
