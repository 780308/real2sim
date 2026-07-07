# Scalable Real2Sim: Physics-Aware Asset Generation via Robotic Pick-and-Place Setups

## 定位
最完整覆盖“完整几何层 + collision + physical parameters”的论文，补足 3DGS/mesh 方法通常缺失的物理属性层。

| 字段 | 内容 |
| --- | --- |
| priority / score | P0 / 4.19/5 |
| family | object visual geometry + collision geometry + inertial parameter estimation |
| sources | https://github.com/nepfaff/scalable-real2sim<br>https://scalable-real2sim.github.io/<br>https://arxiv.org/abs/2503.00370 |
| local_pdf | ref/scalable_real2sim_2503_00370.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/scalable-real2sim |
| commit / license | a8e4d97 / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: robot pick-and-place data, multi-view object observations, gripper masks, RGB/depth/video, robot torque/kinematic state.
- Outputs: textured visual mesh, convex collision geometry, mass, center of mass, rotational inertia.

## Full Method Pipeline
- Collect object observations with robot manipulation setup.
- Use alpha-transparent training and gripper masks to reconstruct object-centric visual geometry.
- Simplify visual geometry into convex collision geometry by approximate convex decomposition.
- Design excitation trajectories and solve physically feasible inertial parameters from robot measurements.

## Losses / Objectives
photometric/geometry reconstruction losses; inertial parameter estimation uses constrained optimization / augmented Lagrangian / physically feasible constraints.

## Assumptions
需要机器人可抓取/搬运物体并采集运动数据；数据采集链路比单纯视觉方法复杂。

## Failure Modes
gripper mask 错误会破坏重建；薄/软/透明物体参数估计困难；对大型固定物体如门/桌子需要改造采集 protocol。

## 对 Directional View Gap 的关系
不补视角，但可以把视觉补齐后的 mesh 变成 simulatable object description。

## Isaac Sim Transfer
direct conceptually: visual mesh + convex collision + inertial parameters 正是 Isaac asset 所需。

## 可迁移模块
- scene/object representation: object visual geometry + collision geometry + inertial parameter estimation
- view/object completion: 不补视角，但可以把视觉补齐后的 mesh 变成 simulatable object description。
- geometry/collision: textured visual mesh, convex collision geometry, mass, center of mass, rotational inertia.
- simulator integration: direct conceptually: visual mesh + convex collision + inertial parameters 正是 Isaac asset 所需。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P0 物理层参考；用于建立 asset validation schema 和后续 physical parameter estimation 实验。

## Next Experiment
先对小型可搬动物体复现 visual/collision/inertia schema；门/桌椅这类大物体用 VLM/PhysX 估计默认物理属性并人工校验。
