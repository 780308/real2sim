# RialTo: A Real-to-Sim-to-Real Approach for Robust Manipulation

## 定位
不是 3DGS asset 方法，但给出老师关心的闭环：资产不是终点，要能提升 manipulation/navigation 任务。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.23/5 |
| family | real-to-sim-to-real manipulation loop / digital twin evaluation |
| sources | https://real-to-sim-to-real.github.io/RialTo/<br>https://github.com/real-to-sim-to-real/RialToPolicyLearning<br>https://arxiv.org/abs/2403.03949 |
| local_pdf | ref/rialto_2403_03949.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/RialToPolicyLearning |
| commit / license | 9556a93 / n/a (cloned) |

## Inputs / Outputs
- Inputs: scanned real scene/digital twin, user corrections, demonstrations/policies.
- Outputs: real-to-sim-to-real manipulation policies and evaluation loop.

## Full Method Pipeline
- Create digital twin from real setup.
- Use simulation to train/robustify policy.
- Deploy policy to real robot and collect failures.
- Iteratively improve digital twin/policy.

## Losses / Objectives
policy learning/reinforcement/imitation objectives depending task.

## Assumptions
digital twin 足够可编辑且用户能修正；不自动解决 asset generation。

## Failure Modes
人工参与较多；visual fidelity 不一定等于 3DGS 质量。

## 对 Directional View Gap 的关系
无直接关系。

## Isaac Sim Transfer
conceptual adapter; 可作为 evaluation loop。

## 可迁移模块
- scene/object representation: real-to-sim-to-real manipulation loop / digital twin evaluation
- view/object completion: 无直接关系。
- geometry/collision: real-to-sim-to-real manipulation policies and evaluation loop.
- simulator integration: conceptual adapter; 可作为 evaluation loop。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 evaluation/process reference。

## Next Experiment
把 object asset 质量最终和 Go2 navigation/manipulation rollout 成功率挂钩，不只看 PSNR/LPIPS。
