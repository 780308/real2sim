# PhysX-3D: Physical-Grounded 3D Asset Generation

## 定位
补上 Isaac 可交互资产最容易缺失的物理属性 schema，尤其 part-level material/affordance/kinematics。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.83/5 |
| family | physical-grounded 3D asset generation / URDF annotation |
| sources | https://github.com/ziangcao0312/PhysX-3D<br>https://arxiv.org/abs/2507.12465<br>https://physx-3d.github.io/ |
| local_pdf | ref/physx_3d_2507_12465.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/PhysX-3D |
| commit / license | 4f54e75 / LICENCE (cloned) |

## Inputs / Outputs
- Inputs: image/object asset plus PhysXNet annotations; part-level material, affordance, kinematics, function descriptions.
- Outputs: physical-property annotated assets, generated geometry with scale/material/affordance/kinematic predictions, URDF conversion script.

## Full Method Pipeline
- Build PhysXNet with five properties: absolute scale, material, affordance, kinematics, function.
- Use human-in-the-loop/VLM annotation for part-level physics properties.
- Train PhysXGen dual-branch model to inject physical knowledge into 3D structural space.
- Convert JSON annotations into URDF via provided script.

## Losses / Objectives
VAE/diffusion training plus property prediction losses; evaluation includes scale distance, PSNR for property maps, kinematic distance.

## Assumptions
物理属性是从数据/语言先验推断，非真实测量；需对关键交互对象人工校验。

## Failure Modes
mass/material/friction 推断不可靠；URDF 转换不等于 Isaac articulation 全部可用；几何质量受底层 3D generator 限制。

## 对 Directional View Gap 的关系
不是视角补齐方法，而是补物理语义和互动层。

## Isaac Sim Transfer
adapter needed but useful: URDF/part-level annotations 可转 Isaac USD/PhysX schema。

## 可迁移模块
- scene/object representation: physical-grounded 3D asset generation / URDF annotation
- view/object completion: 不是视角补齐方法，而是补物理语义和互动层。
- geometry/collision: physical-property annotated assets, generated geometry with scale/material/affordance/kinematic predictions, URDF conversion script.
- simulator integration: adapter needed but useful: URDF/part-level annotations 可转 Isaac USD/PhysX schema。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 physical property prior；和 Scalable Real2Sim 的实测参数形成对照。

## Next Experiment
把一个门/椅子 mesh 的 part hierarchy 输入 PhysX annotation/URDF schema，导入 Isaac 检查关节和碰撞。
