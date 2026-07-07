# Re3Sim: Generating High-Fidelity Simulation Data via 3D-Photorealistic Real-to-Sim for Robotic Manipulation

## 定位
直接展示 IsaacLab 中 visual layer 与 collision/mesh layer 如何协同，适合做 Isaac 端工程模板。

| 字段 | 内容 |
| --- | --- |
| priority / score | P0 / 4.23/5 |
| family | IsaacLab real2sim manipulation pipeline / hybrid 3DGS+mesh |
| sources | https://github.com/InternRobotics/Re3Sim<br>https://arxiv.org/abs/2502.08645<br>https://xshenhan.github.io/Re3Sim/ |
| local_pdf | ref/re3sim_2502_08645.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/Re3Sim |
| commit / license | 681da6f / n/a (cloned) |

## Inputs / Outputs
- Inputs: custom scene photos, alignment image/ArUco, OpenMVS background/object mesh, 3DGS background, IsaacLab resources.
- Outputs: USD/textured meshes, collision meshes, hybrid visual rendering, simulated manipulation data in IsaacLab.

## Full Method Pipeline
- Recover scene/object meshes separately for collision and simulation.
- Train 3DGS for background photorealistic rendering.
- Composite foreground mesh rendering and 3DGS background by Z-buffer/depth.
- Align real-world, simulator, and 3DGS coordinates with markers and ICP, then generate policy data.

## Losses / Objectives
MVS/3DGS reconstruction losses; policy data generation relies privileged simulation information and task rewards.

## Assumptions
背景与前景物体可分开重建；物体 rendering 面积较小时不必 3DGS 渲染；需要 IsaacLab 环境和资源。

## Failure Modes
它选择 mesh 渲染前景物体，可能不足以满足师兄要求的 object 3DGS visual layer；OpenMVS mesh 对细节/遮挡敏感。

## 对 Directional View Gap 的关系
支持 cross-view camera simulation，但补 unseen surfaces 仍依赖补采集或外部 completion。

## Isaac Sim Transfer
direct: 以 IsaacLab 为默认仿真后端，是本项目迁移路线的重要参考。

## 可迁移模块
- scene/object representation: IsaacLab real2sim manipulation pipeline / hybrid 3DGS+mesh
- view/object completion: 支持 cross-view camera simulation，但补 unseen surfaces 仍依赖补采集或外部 completion。
- geometry/collision: USD/textured meshes, collision meshes, hybrid visual rendering, simulated manipulation data in IsaacLab.
- simulator integration: direct: 以 IsaacLab 为默认仿真后端，是本项目迁移路线的重要参考。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P0 Isaac integration baseline；对比 GSWorld 的 GSDF asset design。

## Next Experiment
用 Re3Sim 自定义场景流程导入一个简单对象，替换其 mesh foreground 为 ObjectGS/GaussianObject visual layer，测试 IsaacLab 渲染/碰撞一致性。
