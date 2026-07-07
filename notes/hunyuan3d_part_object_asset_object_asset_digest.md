# Hunyuan3D-Part: P3-SAM and X-Part for 3D Part Segmentation and Shape Decomposition

## 定位
对门把手、椅腿、抽屉、铰链等可交互部件很有价值，补足 object-level 资产中的 part decomposition。

| 字段 | 内容 |
| --- | --- |
| priority / score | P1 / 3.75/5 |
| family | part-level mesh segmentation and decomposition |
| sources | https://github.com/Tencent-Hunyuan/Hunyuan3D-Part<br>https://arxiv.org/abs/2509.06784<br>https://arxiv.org/abs/2509.08643 |
| local_pdf | ref/p3_sam_2509_06784.pdf |
| local_supplementary_pdfs | ref/xpart_2509_08643.pdf |
| local_repo | repos/Hunyuan3D-Part |
| commit / license | e96be06 / LICENSE (cloned) |

## Inputs / Outputs
- Inputs: holistic scanned or generated mesh; optional point prompts/bounding boxes.
- Outputs: part segmentation, part bounding boxes, semantic features, complete part-level decomposed meshes.

## Full Method Pipeline
- P3-SAM segments arbitrary 3D objects into parts using point-promptable segmentation.
- Automatically sample prompts and merge masks into part instances.
- X-Part uses bounding boxes and semantic features to generate coherent parts.
- Outputs can support part-level editing, retopology, UV, and articulation preparation.

## Losses / Objectives
segmentation losses for P3-SAM; diffusion/generation objectives for X-Part part decomposition.

## Assumptions
输入 mesh 已有较完整 holistic geometry；当前 release 是 light version，完整能力可能在 studio。

## Failure Modes
分件语义不一定等于物理关节；细部件可能过分/欠分；不估计 mass/friction/joints。

## 对 Directional View Gap 的关系
不补视角；用于完成 mesh 后的 part-level asset structuring。

## Isaac Sim Transfer
adapter needed: part meshes 可映射 USD hierarchy / articulation links，仍需 joint/physics 参数。

## 可迁移模块
- scene/object representation: part-level mesh segmentation and decomposition
- view/object completion: 不补视角；用于完成 mesh 后的 part-level asset structuring。
- geometry/collision: part segmentation, part bounding boxes, semantic features, complete part-level decomposed meshes.
- simulator integration: adapter needed: part meshes 可映射 USD hierarchy / articulation links，仍需 joint/physics 参数。
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
P1 part decomposition tool；在 Hunyuan3D/GaussianObject 生成完整 mesh 后使用。

## Next Experiment
对生成/扫描的门或椅子 mesh 跑 P3-SAM/X-Part，检查能否分离门板/把手/椅腿并转换为 USD prim hierarchy。
