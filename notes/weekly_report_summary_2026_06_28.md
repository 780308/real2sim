# 本周工作汇报摘要

本周主要围绕 real2sim 当前暴露出的视角失效问题进行了问题收敛和文献调研。基于现有 Go2 20s 诊断结果，当前失败不宜简单归因于“3DGS 训练质量差”或“仿真相机离训练轨迹太远”，更准确的表述是 **directional view coverage gap**：训练数据主要覆盖单一观察方向，当仿真相机在相近位置转向反向或大偏角 yaw 时，3DGS 缺少对应观测支撑，导致 black holes、碎片化、低亮度和结构丢失。该定义把后续工作从泛泛提升渲染质量，收敛到“如何补齐大偏角/反向 novel view，并保持 3D consistency 和仿真可用性”。

围绕该问题，我完成了一轮面向实现路径的文献与开源项目调研，共整理 29 个条目，生成 per-paper/project notes、transfer matrix 和最终综合报告。调研结果显示，handoff 中提到的“开放世界模型”更适合作为 semantic / visual prior，而不是第一主线；原因是其生成结果可能 plausible，但未必与真实 Go2 场景在 metric geometry、拓扑、free space 和 collision 上一致。

| 方向 | 代表方法/项目 | 结论 |
|---|---|---|
| 视角补齐 | GEN3C, SEVA, MVGD | 最直接解决反向/大偏角 novel view，建议优先实验 |
| 几何修复 | PGSR, SuGaR, 2DGS | 将补齐后的观测转为更稳定的 surface / mesh |
| Isaac 接入 | OpenReal2Sim, omni-3dgs-extension | 提供 GLB / USD / IsaacLab 接入参考 |
| 开放世界模型 | HY-World 2.0, LingBot, InSpatio | 可作先验或对照，不能无约束替换真实场景 |

下一步建议先做最小闭环实验：在 A* 黑帧相机中心指定反向 yaw target cameras，用 SEVA/GEN3C 生成 pseudo views；通过亮度、depth/point cloud reprojection 和 free-space violation 过滤后，回灌 PGSR/2DGS/3DGS 重建，再复跑 A* yaw ablation，观察 dark-frame ratio 是否下降且 training-camera replay 不被破坏。若该闭环有效，再进一步用 SuGaR/2DGS 抽取 mesh，并参考 OpenReal2Sim 路线导出 GLB/USD，验证 Isaac Sim 中的 visual observation 和 collision proxy 可用性。
