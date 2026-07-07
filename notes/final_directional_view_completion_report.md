# Final Report: Directional View Completion for Real2Sim / Isaac Sim

## 2026-06-29 更新说明
本报告仍然有效，但其定位已经从“总主线”调整为 **object-centric Isaac asset reconstruction 的子模块**。根据师兄早期交接内容，当前更上位的任务是：针对门、桌椅等指定可交互对象，生成 **3DGS visual layer + geometry/collision/physics layer**，并导入 Isaac Sim / IsaacLab 正常渲染和交互。

因此，directional view completion 现在主要负责补齐指定物体的未观测面、背面或大偏角 novel views；完整主线、重新排序和实验路线见新增报告：`notes/final_object_centric_isaac_asset_report.md`、`notes/object_asset_transfer_matrix.md`。

## 0. 研究问题
当前 Go2 20s 诊断场景的问题不是 3DGS 整体失效，也不是相机中心离训练轨迹太远，而是 **directional view coverage gap**：训练相机主要看向一个方向，仿真相机在相近位置看向反向或大偏角 yaw 时缺少观测支撑，导致 black holes、floaters、低亮度和结构丢失。

因此，第一主线不是无约束 open world generation，而是：**真实场景锚定 + camera/pose-conditioned large-angle novel-view completion + 3D/geometry consistency + Isaac-transferable assets**。

## 1. 综合排序 Top 12
1. **OpenReal2Sim: Toolbox for Real-to-Sim Reconstruction and Robotic Simulation** (4.17/5, P0): P0 平台主线。把 NVS/scene-completion 模块接在 preprocess/reconstruction 之间，最终走 USD conversion。
2. **GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning** (4.01/5, P0): P0 平台参考。吸收 batch 3DGS observation + physics separation，但 directional completion 仍靠 NVS/completion 模块。
3. **GEN3C: 3D-Informed World-Consistent Video Generation with Precise Camera Control** (3.94/5, P0): 与 SEVA 并列 P0。若算力允许，优先用 GEN3C 做 camera-controlled 反向 yaw 补帧，因为它的问题表述最贴合 directional view gap。
4. **SuGaR: Surface-Aligned Gaussian Splatting for Efficient 3D Mesh Reconstruction** (3.91/5, P0): P0 支撑模块：不解决 root cause，但对 Isaac Sim 长期目标必需。
5. **2D Gaussian Splatting for Geometrically Accurate Radiance Fields** (3.86/5, P0): P0 后处理候选，与 PGSR/SuGaR 共同组成 GS repair baseline。
6. **PGSR: Planar-based Gaussian Splatting for Efficient and High-Fidelity Surface Reconstruction** (3.81/5, P0): P0 工程后端：SEVA/GEN3C 生成反向视角后，用 PGSR 验证重训是否减少黑洞并改善 mesh。
7. **Stable Virtual Camera (SEVA): Generative View Synthesis with Diffusion Models** (3.8/5, P0): 第一优先级试验：在 A* 黑帧相机中心上指定反向 yaw target cameras，生成 pseudo views，再用 3DGS/PGSR 重训并检测 dark-frame ratio。
8. **HY-World 2.0: Multi-Modal World Model for 3D World Generation and Reconstruction** (3.69/5, P1): P1 强候选：作为 semantic/geometry prior，不作为第一主线。
9. **SG-NN: Sparse Generative Neural Networks for Self-Supervised Scene Completion of RGB-D Scans** (3.63/5, P1): P1。方法理念值得借鉴，直接复现优先级低于 Seen2Scene/GenRC。
10. **Geometric Latent Diffusion (GLD): Multi-view Diffusion with Geometric Foundation Models** (3.62/5, P1): P1+。作为 MVGD/SEVA 的几何增强替代，若硬件可用值得验证。
11. **MVGD: Zero-Shot Novel View and Depth Synthesis with Multi-View Geometric Diffusion** (3.56/5, P0): 若官方或第三方实现可用，应升级为 SEVA/GEN3C 后的第二个验证模块。
12. **GenRC: Generative 3D Room Completion from Sparse Image Collections** (3.55/5, P0): 作为 mid-term 主线：补视觉后，GenRC/SceneCompleter/Seen2Scene 负责把低覆盖区域转成物理几何假设。

这张综合排序把 Isaac/sim transfer 也计入权重，因此 OpenReal2Sim、GS-Playground、SuGaR 等工程桥接项排名很高。若只问“谁最直接解决反向/大偏角 novel view”，应采用下面的 solution-module ranking。

## 2. Solution-module ranking：先解决黑洞，再进 Isaac
1. GEN3C / SEVA：最先验证。二者都支持 target camera 或 camera trajectory，是直接攻击反向 yaw 黑洞的工具。
2. MVGD / GLD：若代码和算力可用，优先补 depth，因为 pseudo depth 能参与 mesh/TSDF/Isaac collision proxy。
3. CAT3D：作为 multi-view diffusion 范式参考，不作为第一工程依赖，除非找到可复现实现。
4. GenRC / SceneCompleter / Seen2Scene：用于低覆盖区域的 room-scale geometry hypotheses，不替代真实观测。
5. HY-World 2.0：仅在需要 semantic/layout prior 或局部 3D asset prior 时使用，必须受原始 poses/depth/point cloud 约束。

## 3. Integration ranking：补全结果如何变成 Isaac Sim 资产
1. OpenReal2Sim：IsaacLab/Isaac Sim 路径最清晰，已有 GLB、scene.json、USD conversion 和 IsaacLab demo。
2. SuGaR / 2DGS / PGSR：把修复后的 GS 变成 surface/mesh，是 Isaac collision proxy 的关键桥。
3. omni-3dgs-extension：如果短期只需要 Isaac 内 RGB camera observation，可直接验证 3DGS visual layer。
4. GS-Playground / GaussGym：吸收 batch 3DGS rendering + physics separation 的系统设计，但不直接替代 Isaac Sim 后端。

## 4. Taxonomy
### A. Short-term: pose-conditioned NVS / pseudo-view generation
优先使用 SEVA、GEN3C、MVGD、CAT3D/GLD 等方法，在已知 A* camera centers 上指定反向/大偏角 target cameras，生成 pseudo RGB/depth views。该层直接回答 directional gap，但输出多为 visual observation，不能直接作为 collision asset。

### B. Reconstruction repair: GS/mesh consistency
用 PGSR、SuGaR、2DGS 将真实 views + pseudo views 重训为更稳定的 surface-aware GS/mesh。该层不负责 hallucinate 缺失内容，而负责把补来的观测转为更可导出的 geometry。

### C. Sim-ready pipeline
OpenReal2Sim 是最接近 Isaac Sim 的工程锚点：它已有 depth/camera preprocessing、background/object mesh generation、scene.json、GLB assets 和 IsaacLab USD conversion。GS-Playground/GaussGym 则提供 3DGS visual layer 与 physics/robot learning 的系统参考。

### D. 3D scene completion
GenRC、SceneCompleter、Seen2Scene、SG-NN 用于从 RGB-D/point cloud/TSDF 补全 room-scale geometry，适合 mid-term 生成 mesh/collision proxy。它们比纯 video world model 更适合 Isaac，但需要处理 uncertainty。

### E. Open world models
HY-World 2.0、LingBot-World、InSpatio、BWM、τ0-WM、Kairos 可提供 semantic/visual prior 或视频对照，但如果不被 camera pose、depth、point cloud、3DGS 锚定，容易生成“好看但不是当前真实场景”的内容。因此它们不是第一主线。

## 5. 为什么 open world model 不是第一优先级
当前失败帧通常离训练轨迹很近，只是 yaw 与最近训练相机相差约 160°+。这说明缺的是受 pose 约束的大偏角观测，而不是一个全新可探索世界。开放世界模型的优势是生成 plausible world，但弱点是 metric alignment、拓扑保持、可通行边界和 collision correctness。Isaac Sim 后端最终需要的是可验证的 geometry/collision/USD 资产，而不是看起来合理但可能改变真实走廊结构的视频。

开放世界模型可以升级为主线的条件很明确：
1. 输入能绑定真实 camera poses、depth/point cloud 或现有 3DGS。
2. 输出不是单纯 video，而是 mesh、3DGS、point cloud、depth/normal 或可注册的 3D representation。
3. 能对 low-confidence completion 区域给出 uncertainty 或多假设。
4. 通过 point-cloud reprojection、free-space violation 和 Isaac import test。

HY-World 2.0 是这类模型里最接近升级条件的，因为它声明输出 mesh/3DGS/point cloud/depth/camera parameters；LingBot/InSpatio/BWM/Kairos 目前更适合做 visual prior 或对照组。

## 6. 推荐实现路径
### Phase 1: 视觉补齐最小闭环
1. 从现有 diagnostics 中选取黑帧相机中心和目标 yaw。
2. 用 SEVA 或 GEN3C 生成 target cameras 下的 pseudo views；若可用 MVGD/GLD，同时生成 pseudo depth。
3. 过滤 pseudo views：检查亮度、光流/深度连续性、与现有 point cloud 投影的一致性。
4. 用原始 training views + 高置信 pseudo views 重训 3DGS/PGSR/2DGS。
5. 复跑 A* yaw ablation：核心指标是 dark frames 从 71/120 下降，且不破坏 training-camera replay。

推荐第一批实验：
1. **SEVA baseline**：输入原训练视角若干帧，target cameras 设为 A* 黑帧中心 + 训练相机反向/中位 yaw，对比 dark-frame ratio。
2. **GEN3C camera-control baseline**：同样 target cameras，但记录视频 temporal consistency、墙面/门框漂移和 point cloud reprojection error。
3. **PGSR repair baseline**：原始 views + 通过 reject test 的 pseudo views 重训，比较 replay PSNR、A* dark frames、keypose yaw sweep heatmap。

### Phase 2: 几何和 Isaac asset
1. 对修复后的 GS 用 SuGaR/2DGS/PGSR 抽取 mesh。
2. 对低置信区域用 GenRC/SceneCompleter/Seen2Scene 生成 geometry hypotheses。
3. 用 OpenReal2Sim 的 scene.json / GLB / USD conversion 思路接入 IsaacLab/Isaac Sim。
4. 为每个补全区域保留 uncertainty tag，planner 可选择避让或要求主动补采。

推荐第二批实验：
1. **SuGaR/2DGS mesh export**：检查 mesh 是否能承载 corridor wall/floor/door boundary，并统计 holes/free-space violation。
2. **OpenReal2Sim adapter**：把修复 mesh 写成 OpenReal2Sim-style scene.json + GLB，再跑 USD conversion。
3. **active recapture baseline**：少量补采反向 yaw 作为 oracle-lite，对比生成补全是否值得。

### Phase 3: world-model 增强
1. 用 HY-World 2.0 作为 text/image/video-to-3D prior，限定它只补 low-confidence/unobserved zones。
2. 用 LingBot/InSpatio/BWM/Kairos 生成 action/camera-conditioned video 对照，不直接替代 metric scene。
3. 把 world-model 输出与原始 point cloud/depth/pose 做 registration 和 reject test。

## 7. Evaluation and reject tests
- Visual failure proxy：dark-frame ratio、frame_mean、longest dark run。
- View consistency：同一 keypose yaw sweep 的 brightness/depth/feature consistency。
- 3D consistency：pseudo depth 与 point cloud reprojection error，mesh watertightness，free-space violation。
- Isaac readiness：mesh/GLB/USD 是否可导入，collision proxy 是否稳定，camera observation 是否可同步。
- Task utility：A* replay / policy rollout 中是否减少不可辨认 observation，并保持可通行区域合理。

建议采用 hard reject：
- pseudo view 与现有 depth/point cloud 投影冲突过大，丢弃。
- 生成内容侵入已知 free space，丢弃。
- mesh 导入 Isaac 后 collision proxy 封死可通行走廊，丢弃或标为 low confidence。
- training-camera replay 明显下降，说明 pseudo views 污染重建，应降低权重或回滚。

## 8. 完整排序清单
- OpenReal2Sim: Toolbox for Real-to-Sim Reconstruction and Robotic Simulation: 4.17/5, sim-ready real2sim toolbox
- GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning: 4.01/5, 3DGS simulator / real2sim framework
- GEN3C: 3D-Informed World-Consistent Video Generation with Precise Camera Control: 3.94/5, 3D-informed camera-controlled world-consistent video
- SuGaR: Surface-Aligned Gaussian Splatting for Efficient 3D Mesh Reconstruction: 3.91/5, 3DGS-to-mesh extraction
- 2D Gaussian Splatting for Geometrically Accurate Radiance Fields: 3.86/5, surfel Gaussian representation / mesh extraction
- PGSR: Planar-based Gaussian Splatting for Efficient and High-Fidelity Surface Reconstruction: 3.81/5, 3DGS geometry regularization / mesh extraction
- Stable Virtual Camera (SEVA): Generative View Synthesis with Diffusion Models: 3.8/5, pose-conditioned large-angle NVS
- HY-World 2.0: Multi-Modal World Model for 3D World Generation and Reconstruction: 3.69/5, open 3D world model
- SG-NN: Sparse Generative Neural Networks for Self-Supervised Scene Completion of RGB-D Scans: 3.63/5, RGB-D scan geometry completion
- Geometric Latent Diffusion (GLD): Multi-view Diffusion with Geometric Foundation Models: 3.62/5, geometry-latent multi-view diffusion
- MVGD: Zero-Shot Novel View and Depth Synthesis with Multi-View Geometric Diffusion: 3.56/5, novel view + scale-consistent depth synthesis
- GenRC: Generative 3D Room Completion from Sparse Image Collections: 3.55/5, room-scale RGB-D mesh completion
- SceneCompleter: Dense 3D Scene Completion for Generative Novel View Synthesis: 3.55/5, dense 3D completion for generative NVS
- Omniverse 3D Gaussian Splatting Extension: 3.48/5, Isaac/Omniverse 3DGS integration
- Seen2Scene: Completing Realistic 3D Scenes with Visibility-Guided Flow: 3.45/5, real-scan 3D scene completion
- GaussGym: An Open-Source Real-to-Sim Framework for Learning Locomotion from Pixels: 3.41/5, real-to-sim 3DGS locomotion framework
- LingBot-World: Open-Source World Simulator from Video Generation: 3.31/5, camera/action-conditioned video world model
- CAT3D: Create Anything in 3D with Multi-View Diffusion Models: 3.24/5, multi-view diffusion for reconstruction input synthesis
- VoxFormer: Sparse Voxel Transformer for Camera-based 3D Semantic Scene Completion: 3.17/5, semantic scene completion
- InSpatio-WorldFM: Open-Source Real-Time Generative Frame Model: 3.16/5, interactive world/video frame model
- Symphonies: 3D Semantic Scene Completion with Contextual Instance Queries: 3.16/5, semantic scene completion
- MvGenMaster: Scaling Multi-View Consistent Image Generation: 2.91/5, multi-view image generation
- CAT4D: Create Anything in 4D with Multi-View Video Diffusion Models: 2.77/5, dynamic multi-view video diffusion
- Kairos: Native World Model Stack for Physical AI: 2.7/5, general physical-AI world model stack
- Boundless World Model (BWM): 2.69/5, action-conditioned robot video world model
- Real-to-Sim Robot Policy Evaluation with Gaussian Splatting Simulation of Soft-Body Interactions: 2.66/5, policy evaluation / GS simulator
- HunyuanWorld-Voyager: 2.55/5, explorable video/world generation
- WorldArena: Benchmark for Embodied World Models: 2.52/5, world model benchmark
- τ0-WM: A Unified Video-Action World Model for Robotic Manipulation: 2.19/5, video-action manipulation world model

## 9. 关键结论
开放世界模型仍然有价值，但它在本问题中应作为 **prior** 或 **fallback generator**，不是第一优先级。第一优先级是可以被真实 Go2 数据和 camera pose 锚定的方法：SEVA/GEN3C/MVGD 负责补视角，PGSR/SuGaR/2DGS 负责表面化，OpenReal2Sim 负责 Isaac Sim 资产路径。
