# Final Report: Object-Centric Isaac Asset Reconstruction for Real2Sim

## 0. 更新后的研究问题
师兄两个月前给出的任务比前一轮 directional view completion 更上位：目标不是只补场景视角，而是面向数字孪生仿真器，为门、桌椅等指定可交互对象生成 **3DGS visual layer + 完整 geometry/collision/physics layer**，并能符合 Isaac Sim / IsaacLab 的导入和交互需求。

因此，本轮调研把旧问题重构为：

> 给定单视角或多视角 RGB/RGB-D、camera poses、point cloud / depth / 3DGS 等真实观测，针对指定可交互物体生成 Isaac Sim 可用的 dual-layer asset；directional view completion 是其中用于补齐物体未观测面或反向视角的子模块。

## 1. 关键结论
- **GSWorld 是当前最贴合原任务的第一主线**：它已经把 metric 3DGS、Gaussian-on-Mesh、URDF、collision mesh、material properties 和 physics engine 放进一个 GSDF asset contract。
- **SuGaR/PGSR/2DGS 是几何层必需后端**：它们不负责 hallucinate 缺失内容，但负责把补齐后的 visual observations 或 3DGS 变成 mesh/collision proxy。
- **ObjectGS/GaussianObject 补上“指定物体”和“物体背面缺失”两个关键缺口**：前者负责 object extraction，后者负责 sparse-view object completion。
- **OpenReal2Sim/Re3Sim/SAGE-3D 负责 Isaac/IsaacLab 落地参照**：最终验收必须是 USD/GLB/URDF/collision 在 Isaac 中可渲染、可碰撞、可交互。
- **Hunyuan3D/PhysX/PhysForge 是生成式先验，不是无约束主线**：它们可补背面、PBR、part hierarchy、material/kinematics，但必须受真实 point cloud、scale、bbox 和 collision tests 约束。

## 2. 综合排序 Top 15
1. **GSWorld: Closed-Loop Photo-Realistic Simulation Suite for Robotic Manipulation** (4.33/5, P0): 第一复现对象和系统设计锚点；把本项目目标重写为 GS visual layer + geometry/collision layer 的 asset contract。
2. **Re3Sim: Generating High-Fidelity Simulation Data via 3D-Photorealistic Real-to-Sim for Robotic Manipulation** (4.23/5, P0): P0 Isaac integration baseline；对比 GSWorld 的 GSDF asset design。
3. **SuGaR: Surface-Aligned Gaussian Splatting for Efficient 3D Mesh Reconstruction** (4.19/5, P0): P0 几何层后端；与 GSWorld/OpenReal2Sim/Isaac importer 组成 asset export baseline。
4. **Scalable Real2Sim: Physics-Aware Asset Generation via Robotic Pick-and-Place Setups** (4.19/5, P0): P0 物理层参考；用于建立 asset validation schema 和后续 physical parameter estimation 实验。
5. **OpenReal2Sim: Toolbox for Real-to-Sim Reconstruction and Robotic Simulation** (4.06/5, P0): P0 Isaac exporter scaffold；和 GSWorld asset contract 结合。
6. **Hunyuan3D-Omni: A Unified Framework for Controllable Generation of 3D Assets** (3.99/5, P1): P1+ generative completion prior；若 Hunyuan3D-2.1 不够受约束，升级到 Omni。
7. **ObjectGS: Object-aware Scene Reconstruction and Scene Understanding via Gaussian Splatting** (3.93/5, P0): P0 object selection/extraction 工具；优先用于门、椅子、桌子等指定物体分离。
8. **GaussianObject: High-Quality 3D Object Reconstruction from Four Views with Gaussian Splatting** (3.91/5, P0): P0 object backside completion baseline；和 ObjectGS 输出的 object crop/mask 串联。
9. **Hunyuan3D 2.1: From Images to High-Fidelity 3D Assets with Production-Ready PBR Material** (3.89/5, P1): P1/P0 边界的 generative object prior；用于低覆盖面的补全候选。
10. **RoboSimGS: High-Fidelity Simulated Data Generation for Real-World Zero-Shot Robotic Manipulation Learning with Gaussian Splatting** (3.88/5, P0): P0/P1 之间的设计参考；用于物体 articulation/physical property 默认值生成。
11. **SAGE-3D: Towards Physically Executable 3D Gaussian for Embodied Navigation** (3.88/5, P0): P0 Isaac 5.0 视觉/物理混合环境参考；对 Go2 导航平台非常相关。
12. **PhysX-3D: Physical-Grounded 3D Asset Generation** (3.83/5, P1): P1 physical property prior；和 Scalable Real2Sim 的实测参数形成对照。
13. **PGSR: Planar-based Gaussian Splatting for Efficient and High-Fidelity Surface Reconstruction** (3.83/5, P0): P0 几何后端，尤其针对门/桌面/墙体。
14. **2D Gaussian Splatting for Geometrically Accurate Radiance Fields** (3.83/5, P0): P0 几何后端，与 SuGaR/PGSR 并列比较。
15. **Hunyuan3D-Part: P3-SAM and X-Part for 3D Part Segmentation and Shape Decomposition** (3.75/5, P1): P1 part decomposition tool；在 Hunyuan3D/GaussianObject 生成完整 mesh 后使用。

## 3. 新 Taxonomy：从视角补齐到物体资产
| layer | role | preferred methods | why |
| --- | --- | --- | --- |
| 1 object selection | 从整场景中得到指定物体 visual subset | ObjectGS, Gaussian Grouping, SAGA | 没有 object identity，就无法输出指定物体资产，也无法给门/桌椅做独立 collision。 |
| 2 object view/backside completion | 补齐稀疏视角下物体背面和压缩区域 | GaussianObject, Hunyuan3D-Omni/2.1, InstantMesh/CRM/LGM | 把原 directional view gap 从 scene-level 收束到 object-level missing surfaces。 |
| 3 visual layer | 保持照片级观察输入 | GSWorld, ObjectGS, LGM, 3DGRUT/NuRec | 3DGS 负责 photorealistic rendering，但不承担物理碰撞。 |
| 4 geometry/collision layer | 输出可导入模拟器的 mesh/collision proxy | SuGaR, PGSR, 2DGS, GSDF, Scalable Real2Sim | Isaac 交互依赖稳定几何、凸分解、质量/惯量。 |
| 5 simulator integration | 导入 Isaac / IsaacLab 并验证任务 | OpenReal2Sim, Re3Sim, SAGE-3D, GSWorld | 最终验收不是只看图像，而是 USD/GLB/URDF/collision 在 Isaac 中可运行。 |
| 6 physical semantics | 补 part/material/affordance/kinematics | Scalable Real2Sim, PhysX-3D, PhysForge, Hunyuan3D-Part | 门、抽屉、桌椅等可交互对象需要 part hierarchy 和物理属性。 |

## 4. 为什么旧 directional view completion 不删除，而是降级为子模块
前一轮调研正确识别了 Go2 场景中的 **directional view coverage gap**：相机中心接近训练轨迹，但 yaw 反向时 3DGS 出现黑洞和低亮度。这仍然是一个真实问题，但如果目标是“指定物体 3DGS 渲染层 + 完整几何层”，那么它只回答了资产生成流程中的一个局部问题：**物体未观测面如何补齐**。

新的主线应先确定 object identity，再补 unseen surface，最后导出 geometry/collision/physics。换句话说：

`scene-level 3DGS failure` -> `object selection` -> `object-level view/backside completion` -> `surface/mesh extraction` -> `collision/physics annotation` -> `Isaac import and task validation`

## 5. 推荐实现路线
### Short-term: 最小对象资产闭环
先选一个可控对象，而不是整段走廊：例如椅子、桌子、门板/门把手或可移动小物体。用 ObjectGS/Gaussian Grouping 得到 object-only Gaussians/masks；用 GaussianObject 或 Hunyuan3D-Omni 补未观测背面；用 SuGaR/PGSR/2DGS 抽取 mesh；用 OpenReal2Sim/Re3Sim-style adapter 导出 GLB/USD/collision proxy；最后在 Isaac 中验证 RGB rendering 和 contact/collision。

### Mid-term: 物理属性和部件层
对可搬动物体，参考 Scalable Real2Sim 估计 mass、center of mass、inertia；对门、抽屉、桌椅等大物体，用 Hunyuan3D-Part、PhysX-3D、PhysForge 生成 part hierarchy/material/affordance/kinematics 的候选，再人工和仿真验证。

### Long-term: 生成式模型作为受约束先验
Hunyuan3D、PhysForge、EmbodiedGen 这类模型可用于 low-confidence / unobserved regions，但不能直接替换真实资产。所有生成结果都要通过 point-cloud reprojection、free-space violation、mesh/collision、Isaac import 和 task rollout 检查。

## 6. 实验计划
| phase | experiment | success criteria |
| --- | --- | --- |
| E0 | 复现 GSWorld/SuGaR 最小对象：一个小物体或门/椅子局部 | 得到 metric 3DGS + mesh + collision proxy，并能在 Isaac/IsaacLab 中渲染和碰撞。 |
| E1 | ObjectGS/Gaussian Grouping 提取指定物体 | object-only rendering/mesh export 成功；物体边界不粘连背景。 |
| E2 | GaussianObject/Hunyuan3D-Omni 补物体未观测面 | 背面 novel view 可用，且与真实 point cloud/depth 不冲突。 |
| E3 | SuGaR/PGSR/2DGS mesh extraction 对比 | holes/free-space violation 降低；collision proxy 不封死可通行/可操作空间。 |
| E4 | OpenReal2Sim/Re3Sim-style Isaac adapter | 导出 GLB/USD/URDF/scene.json；Isaac camera RGB 与 collision body 坐标一致。 |
| E5 | Physical property schema | 小物体用 Scalable Real2Sim；大物体用 PhysX/PhysForge prior + 手工校验；mass/friction/joint 可追溯。 |

## 7. Reject Tests
| test | reject condition |
| --- | --- |
| visual consistency | 补齐视角在相邻 camera sweep 中出现跳变、结构漂移或 brightness hole。 |
| metric geometry | 生成 mesh 与已有 depth/point cloud reprojection error 过大。 |
| free space | 补全物体侵入已知可通行/可操作 free space。 |
| collision | convex decomposition 后封死门口、桌下空间或生成不稳定 contact。 |
| object identity | ObjectGS/Grouping 输出物体和背景/机器人 link 粘连。 |
| task utility | Isaac rollout 的 collision rate、navigation/manipulation success 不升反降。 |

## 8. 对老师汇报时的简洁定位
本周调研需要表述为：我们在原先 directional view gap 的基础上，进一步对齐师兄交接中的 object-centric Isaac asset 目标，明确了后续主线不是“开放世界模型生成场景”，而是 **指定物体的双层资产生成**：3DGS 负责高保真视觉，mesh/collision/physics 负责 Isaac 可交互性。开放世界/3D 生成模型只作为受真实几何约束的补全先验。
