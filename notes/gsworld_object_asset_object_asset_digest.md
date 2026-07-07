# GSWorld: Closed-Loop Photo-Realistic Simulation Suite for Robotic Manipulation

## 定位
最贴合师兄原始任务的主线：它已经把 3DGS visual layer、mesh/collision、URDF、physics engine 和 manipulation policy loop 放在同一资产协议中。

| 字段 | 内容 |
| --- | --- |
| priority / score | P0 / 4.33/5 |
| family | object-centric real2sim simulator / GSDF asset format |
| sources | https://github.com/luccachiang/GSWorld<br>https://arxiv.org/abs/2510.20813<br>https://huggingface.co/datasets/GqJiang/gsworld |
| local_pdf | ref/gsworld_2510_20813.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/GSWorld |
| commit / license | 5329504 / n/a (cloned) |

## Inputs / Outputs
- Inputs: short multi-view captures, COLMAP poses, ArUco metric scale, robot URDF, cropped point cloud / object assets.
- Outputs: GSDF asset: Gaussian-on-Mesh visual layer + robot URDF + objects + collision meshes + material properties; ManiSkill/physics-engine tasks.

## Full Method Pipeline
- COLMAP + ArUco scaling trains metric 3DGS from real images.
- Sample semantic point cloud from robot URDF meshes, crop reconstructed point cloud, then manually align and refine with ICP.
- Transfer per-link semantic labels, segment robot/object Gaussians, and attach collision meshes/material properties.
- Use GSDF assets inside a physics simulator for policy training, evaluation, DAgger data collection, and sim-to-real replay.

## Losses / Objectives
3DGS photometric reconstruction losses; ICP/alignment objectives; simulator side uses task reward / policy learning losses rather than a single reconstruction loss.

## Assumptions
需要短多视角采集、ArUco 或等价 metric scaling、机器人/物体可分割；细粒度 collision mesh 和 material 仍需人工或辅助工具校验。

## Failure Modes
遮挡严重或物体背面缺失会污染 Gaussian-on-Mesh；ICP 初值差会造成 robot/object/GS 坐标错位；GSDF 当前更偏 manipulation tabletop，迁移 Go2 大场景需重写 asset adapter。

## 对 Directional View Gap 的关系
不直接解决大偏角补视角，但它定义了补齐结果最终应进入的 object asset contract。

## Isaac Sim Transfer
adapter needed: 可把 GSDF 思路迁移到 Isaac Sim 5.0 的 USD/URDF/mesh/collision；短期先复现其 real2sim asset construction，再写 Isaac exporter。

## 可迁移模块
- scene/object representation: object-centric real2sim simulator / GSDF asset format
- view/object completion: 不直接解决大偏角补视角，但它定义了补齐结果最终应进入的 object asset contract。
- geometry/collision: GSDF asset: Gaussian-on-Mesh visual layer + robot URDF + objects + collision meshes + material properties; ManiSkill/physics-engine tasks.
- simulator integration: adapter needed: 可把 GSDF 思路迁移到 Isaac Sim 5.0 的 USD/URDF/mesh/collision；短期先复现其 real2sim asset construction，再写 Isaac exporter。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
第一复现对象和系统设计锚点；把本项目目标重写为 GS visual layer + geometry/collision layer 的 asset contract。

## Next Experiment
选择一个门/椅子/桌子小物体，按 GSWorld real2sim 流程完成 metric 3DGS、object mask、mesh/collision、URDF/USD 对齐，作为所有补全模块的验收接口。
