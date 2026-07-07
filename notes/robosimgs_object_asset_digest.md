# RoboSimGS: High-Fidelity Simulated Data Generation for Real-World Zero-Shot Robotic Manipulation Learning with Gaussian Splatting

## 定位
强化“可交互物体不应只用 3DGS”的结论：背景可 3DGS，物体必须有 mesh/physics/articulation。

| 字段 | 内容 |
| --- | --- |
| priority / score | P0 / 3.88/5 |
| family | R2S2R hybrid 3DGS background + mesh interactive objects |
| sources | https://github.com/Maxwell-Zhao/RoboSimGS<br>https://robosimgs.github.io/<br>https://arxiv.org/abs/2510.10637 |
| local_pdf | ref/robosimgs_2510_10637.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/RoboSimGS |
| commit / license | 3f767f5 / n/a (cloned) |

## Inputs / Outputs
- Inputs: multi-view real-world images, segmentation, MLLM physical/articulation inference, simulator alignment.
- Outputs: photorealistic 3DGS static background, interactive mesh objects, inferred density/stiffness/hinge/rail parameters, simulated data.

## Full Method Pipeline
- Reconstruct a hybrid scene where 3DGS captures static photorealism and mesh primitives represent interactive objects.
- Use MLLM to infer physical properties and kinematic structure from visual data.
- Align hybrid scene with simulator and apply holistic augmentation over objects, cameras, lighting, and trajectories.
- Train manipulation policy on generated data for zero-shot sim-to-real.

## Losses / Objectives
standard reconstruction/policy losses; MLLM-inferred physical properties are not directly supervised by real measurements in the paper pipeline.

## Assumptions
MLLM 能合理推断物体物理/运动结构；真实场景对齐可靠；代码成熟度需进一步核验。

## Failure Modes
VLM/MLLM 物理参数可能 plausible but wrong；对门/抽屉等 articulated object 需要强校验。

## 对 Directional View Gap 的关系
不以补视角为核心，但 hybrid design 能接收 GaussianObject/Hunyuan3D 生成的物体 mesh。

## Isaac Sim Transfer
adapter needed; paper目标是 physics engine interactive environments，和 Isaac 资产需求高度一致。

## 可迁移模块
- scene/object representation: R2S2R hybrid 3DGS background + mesh interactive objects
- view/object completion: 不以补视角为核心，但 hybrid design 能接收 GaussianObject/Hunyuan3D 生成的物体 mesh。
- geometry/collision: photorealistic 3DGS static background, interactive mesh objects, inferred density/stiffness/hinge/rail parameters, simulated data.
- simulator integration: adapter needed; paper目标是 physics engine interactive environments，和 Isaac 资产需求高度一致。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P0/P1 之间的设计参考；用于物体 articulation/physical property 默认值生成。

## Next Experiment
让 VLM/LLM 为门、椅子生成候选 joint/material/mass schema，再和 Isaac 交互测试中的碰撞/关节行为对照。
