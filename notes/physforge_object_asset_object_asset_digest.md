# PhysForge: Generating Physics-Grounded 3D Assets for Interactive Virtual World

## 定位
长期非常相关：直接面向可交互资产而非静态 mesh，但当前代码成熟度和真实场景锚定弱。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.46/5 |
| family | physics-grounded part-aware asset generation |
| sources | https://github.com/HKU-MMLab/PhysForge<br>https://arxiv.org/abs/2605.05163<br>https://hku-mmlab.github.io/PhysForge/ |
| local_pdf | ref/physforge_2605_05163.pdf |
| local_supplementary_pdfs | 无 |
| local_repo | repos/PhysForge |
| commit / license | adfdca8 / n/a (cloned) |

## Inputs / Outputs
- Inputs: single image plus VLM-generated Hierarchical Physical Blueprint.
- Outputs: functionally plausible simulation-ready 3D assets with part materials, masses, joint types, affordances, kinematic parameters.

## Full Method Pipeline
- VLM planner acts as physical architect and generates hierarchical physical blueprint.
- Blueprint defines part layout, materials, mass, function, joint type, affordances.
- Diffusion stage uses KineVoxel Injection to jointly synthesize geometry and kinematic parameters.
- Assets are demonstrated in physics simulator/game virtual world.

## Losses / Objectives
diffusion generation objective conditioned on blueprint and KineVoxel; VLM planning is prompt/annotation-driven.

## Assumptions
VLM blueprint 正确；生成资产不需要和真实扫描严格一致。

## Failure Modes
容易生成 plausible interactive object 但不是当前真实物体；repo 目前较轻，短期复现风险高。

## 对 Directional View Gap 的关系
可补未观测部件/关节，但不是 real-scene anchored completion。

## Isaac Sim Transfer
adapter needed: blueprint 可映射 USD/URDF/PhysX，但需实际 exporter。

## 可迁移模块
- scene/object representation: physics-grounded part-aware asset generation
- view/object completion: 可补未观测部件/关节，但不是 real-scene anchored completion。
- geometry/collision: functionally plausible simulation-ready 3D assets with part materials, masses, joint types, affordances, kinematic parameters.
- simulator integration: adapter needed: blueprint 可映射 USD/URDF/PhysX，但需实际 exporter。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 long-term prior；不作为短期主线。

## Next Experiment
抽取其 blueprint schema，用于给 Hunyuan3D/GaussianObject mesh 自动生成 Isaac 物理默认值。
