# OpenReal2Sim: Toolbox for Real-to-Sim Reconstruction and Robotic Simulation

## 定位
最接近本地 Isaac asset glue code 的工具箱；适合作为我们最终 exporter/interface 的代码参考。

| 字段 | 内容 |
| --- | --- |
| priority / score | P0 / 4.06/5 |
| family | real2sim toolbox / GLB scene.json USD conversion |
| sources | https://github.com/IntelLabs/OpenReal2Sim |
| local_pdf | 无 |
| local_supplementary_pdfs | 无 |
| local_repo | repos/OpenReal2Sim |
| commit / license | 8f69a19 / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: single image / monocular video / depth / camera preprocessing outputs.
- Outputs: background/object meshes, scene.json, GLB assets, IsaacLab USD conversion demos.

## Full Method Pipeline
- Preprocess input to metric depth/camera assets.
- Generate background/object mesh assets and scene config.
- Convert assets through GLB/scene.json path.
- Run IsaacLab demos and manipulation/planning examples.

## Losses / Objectives
工程 pipeline 而非单篇论文；重建模块各自有对应 losses。

## Assumptions
需要适配我们的 Go2/RGB-D/3DGS 输入；默认 object extraction 可能偏单图/局部。

## Failure Modes
不解决高质量物体 3DGS visual layer；depth/inpainting 错误会污染 mesh。

## 对 Directional View Gap 的关系
把补齐模块放在 preprocess 和 reconstruction 之间。

## Isaac Sim Transfer
direct: GLB/scene.json/USD conversion 是当前最实用的 Isaac path。

## 可迁移模块
- scene/object representation: real2sim toolbox / GLB scene.json USD conversion
- view/object completion: 把补齐模块放在 preprocess 和 reconstruction 之间。
- geometry/collision: background/object meshes, scene.json, GLB assets, IsaacLab USD conversion demos.
- simulator integration: direct: GLB/scene.json/USD conversion 是当前最实用的 Isaac path。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P0 Isaac exporter scaffold；和 GSWorld asset contract 结合。

## Next Experiment
用一个 ObjectGS/GaussianObject/SuGaR 输出物体，包装成 OpenReal2Sim-style scene.json + GLB/USD。
