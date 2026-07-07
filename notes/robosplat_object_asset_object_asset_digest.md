# RoboSplat: 3DGS-based Robotic Demonstration Generation

## 定位
数据生成与 policy augmentation 参考，不是资产生成核心。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.0/5 |
| family | robot data generation with 3DGS |
| sources | https://github.com/InternRobotics/RoboSplat<br>https://arxiv.org/abs/2504.13175 |
| local_pdf | ref/robosplat_2504_13175.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/RoboSplat |
| commit / license | 372c9c7 / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: robot demonstrations and 3DGS scene representation.
- Outputs: augmented/synthetic robotic demonstrations.

## Full Method Pipeline
- Build 3DGS scene/robot representation.
- Transform/recompose demonstrations in 3D.
- Render synthetic observations.
- Use generated demos for policy learning.

## Losses / Objectives
reconstruction and policy/demonstration learning objectives.

## Assumptions
已有可用 3DGS asset；不解决物体 mesh/collision。

## Failure Modes
输入 asset 坏则输出数据也坏。

## 对 Directional View Gap 的关系
不补视角。

## Isaac Sim Transfer
indirect。

## 可迁移模块
- scene/object representation: robot data generation with 3DGS
- view/object completion: 不补视角。
- geometry/collision: augmented/synthetic robotic demonstrations.
- simulator integration: indirect。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 后续 data scaling 参考。

## Next Experiment
在 asset pipeline 稳定后再考虑用其生成 Go2/robot policy data。
