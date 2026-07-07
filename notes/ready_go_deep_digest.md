# ReaDy-Go 深度阅读 Digest

论文: **ReaDy-Go: Real-to-Sim Dynamic 3D Gaussian Splatting Simulation for Environment-Specific Visual Navigation with Moving Obstacles**  
本地文件: `ref/ReaDy-Go.pdf`  
阅读目标: 服务 collaborative real2sim simulation platform，关注 real2sim 质量、open-world / unseen-scene、partially observed scenes。

## 1. Problem Setting

ReaDy-Go 解决的是 **environment-specific RGB-only visual navigation in dynamic real-world environments**。

问题背景:

- 真实机器人导航通常需要在家庭、餐厅、工厂、校园等具体目标环境中部署。
- 只用 RGB camera 的 navigation policy 硬件成本低，但 monocular depth ambiguity 和 sim-to-real gap 会使真实部署不稳。
- 传统 simulation 训练容易有 domain gap。
- 3D Gaussian Splatting-based real-to-sim 可以用真实视频重建目标环境，生成 photorealistic observations，降低视觉 gap。
- 现有 GS-based navigation 多数只处理 static scenes；动态障碍常用非 photorealistic simulator assets，例如 Unity human mesh。

ReaDy-Go 的问题定义:

给定目标环境的一段 **static monocular video**，重建该环境的 static GS scene，插入可动画化的 **human GS obstacles**，生成 dynamic navigation datasets，并训练目标环境专属的 RGB-only policy。

它的下游任务是 **goal navigation**:

- robot 从 start 到 goal。
- static task: 避开静态障碍。
- dynamic task: 还要避开 1 到 2 个 moving human obstacles。
- policy 输入 RGB history、previous action、relative goal。
- policy 输出 linear velocity `v` 和 angular velocity `w`。

## 2. Core Hypothesis

核心假设可以拆成三层:

1. **Photorealistic dynamic obstacles matter**  
   如果动态人也是 GS representation，而不是 mesh / Unity asset，那么训练出的 RGB-only navigation policy 在动态真实环境中更稳。

2. **Environment-specific real-to-sim beats generic navigation for target deployment**  
   对一个固定目标环境，基于该环境视频生成数据训练的小模型，可能比大规模 general navigation model 更可靠、更快。

3. **GS can serve as a data-generation simulator, not only a renderer**  
   Static GS scene 不只是 novel-view rendering，它还能被 voxelized 成 occupancy / navigable maps，作为 planner 和 dataset generator 的中间表示。

对我们平台来说，最有价值的是第 3 点: GS 可以成为 real2sim 的统一视觉底座，但必须额外补上 geometry confidence、semantics、physics proxies 和 simulator state。

## 3. Pipeline Diagram in Text Form

```text
真实目标环境
  |
  |  static monocular video + ArUco metric scale
  v
COLMAP camera poses
  |
  v
PGSR static 3DGS reconstruction
  |
  |--> photorealistic renderer
  |
  |--> static GS voxelization
          |
          | opacity filtering
          | height projection
          v
      2D robot navigable map
      2D human walkable map

Human asset branch:
NeuMan videos
  |
  v
HUGS extracts animatable human GS avatars
  |
  v
Human GS asset library

Scenario generation:
robot start / goal sampling
human start / goal sampling
  |
  |--> human planner:
  |      A* seed path on human walkable map
  |      spline-based optimization
  |      2D human trajectory
  |
  |--> motion generation:
  |      2D trajectory -> root velocities
  |      PriorMDM -> 3D body joints
  |      SMPLify -> SMPL parameters
  |      SMPL motion -> animated human GS in world frame
  |
  |--> robot expert planner:
         dynamic obstacle projection to robot map
         Hybrid A* + motion primitives
         reactive replanning
         expert action sequence (v, w)

Dynamic GS simulator:
static scene GS + animated human GS + robot camera poses
  |
  v
photorealistic RGB observations
  |
  v
training tuples:
(RGB_t-2:t, previous action, relative goal, expert action)
  |
  v
RGB-only navigation policy via imitation learning
  |
  v
sim-to-real deployment on physical robot
```

## 4. Representation Analysis

| Representation | ReaDy-Go 是否使用 | 作用 | 对 real2sim 平台的意义 |
|---|---:|---|---|
| Mesh | 基本不使用 | 作者强调无需 mesh extraction 和 physics engine integration | 这是轻量优势，但缺少 contact-rich physics 和精细 collision geometry |
| Point cloud | 间接使用 | human GS 过滤后用 mean positions / voxel-grid downsampling 得到 points，再投影到 2D map | 可作为 dynamic actor 的 collision proxy 初版 |
| NeRF | 不使用 | 论文路线选择 3DGS 而非 NeRF | 3DGS 更适合实时 rendering 和显式 primitive 操作 |
| 3DGS | 核心表示 | static scene GS + human GS avatars | real2sim 的视觉底座，适合 novel-view dataset generation |
| Occupancy / voxel | 核心中间表示 | GS voxelization，opacity filtering，height projection 到 2D maps | 从视觉重建走向 planning / simulation 的关键桥 |
| Object-centric assets | 部分使用 | human GS avatar 是 object-centric dynamic asset | 应推广到 carts、doors、chairs、vehicles、movable objects |
| Simulator state | 弱显式 | 论文有 robot pose、goal、human trajectory、GS state，但不是完整 physics state | 我们平台需要把 visual state、semantic state、physics state、planning state 统一成 schema |

关键观察:

- ReaDy-Go 的 3DGS 是 **rendering-first representation**。
- Occupancy map 是 **planning-first representation**。
- Human GS avatar 是 **object-centric visual asset**。
- 它没有完整 simulator state abstraction，这是我们平台可以补强的位置。

## 5. What Is Learned vs. What Is Engineered

### Learned

- **PGSR static GS reconstruction**  
  学习 static scene 的 Gaussian parameters，包括 position、rotation、scale、opacity、color 等。目标来自 photometric loss 和 geometric regularization。

- **HUGS human GS avatar extraction**  
  从 human video 中学习可动画化 human GS，并与 SMPL / triplane features / LBS weights 绑定。

- **PriorMDM motion generation**  
  使用 motion diffusion prior，从 trajectory-conditioned input 生成 plausible human body motion。

- **Navigation policy**  
  10-layer CNN encoder + 3-layer MLP，用 imitation learning 学习 `(RGB history, previous action, relative goal) -> (v, w)`。

### Engineered

- COLMAP + ArUco metric scale pipeline。
- GS voxelization 规则: voxel 与 `1 sigma ellipsoid` 相交则 occupied。
- Opacity threshold filtering。
- Height projection 到 robot navigable map / human walkable map。
- Occupancy inflation by robot / human radius。
- Human scenario sampling: human path 与 robot start-goal line cross 或 parallel。
- Human path: A* seed path + spline smoothing。
- Robot expert planner: Hybrid A* + motion primitive library。
- Dynamic obstacle handling: FOV + safety margin gating，2 s constant velocity safety buffer。
- Reactive replanning trigger。
- Evaluation protocol: SR / ART, static / dynamic, sim / real, seen / unseen。

我的判断:

ReaDy-Go 的创新不是一个新的 neural architecture，而是把已有 learning components 和 engineered planning/rendering components 拼成一个稳定的数据工厂。它是很好的 platform paper，不是纯模型 paper。

## 6. Open-World or Unseen-Scene Handling

论文有 **unseen environment zero-shot deployment**，但没有真正解决 open-world scene completion。

它做了什么:

- 在 Outside、Lobby、Library 三个环境中各生成数据。
- 把三个环境共 1,200 episodes 合并训练。
- 将 policy 部署到一个 unseen environment。
- 结果: Static SR 70%，Dynamic SR 50%，ART 分别为 30.60 s 和 35.45 s。

它没有做什么:

- 不补全未观测区域。
- 不进行 amodal object completion。
- 不生成 unseen object assets。
- 不推断 hidden geometry。
- 不显式处理 semantic unknowns。
- 不构建 probabilistic world hypotheses。
- 不做 online map update 或 active exploration。

对我们平台的含义:

ReaDy-Go 可以作为 **seen-scene real2sim data factory**。如果要用于 open-world / partially observed scenes，需要在 static GS reconstruction 后增加:

```text
partial GS
  -> coverage / uncertainty estimation
  -> semantic object proposal
  -> layout and object completion hypotheses
  -> multi-hypothesis simulator rollout
  -> planner / policy training under uncertainty
  -> real feedback to select or revise hypotheses
```

也就是说，ReaDy-Go 是我们 open-world 方法的前半段，不是完整答案。

## 7. Real2Sim Quality Levers

| Lever | ReaDy-Go 做法 | 强项 | 短板 | 我们平台可加的东西 |
|---|---|---|---|---|
| Geometry | PGSR + voxelization + opacity filtering | 比 vanilla GS 更适合 surface / occupancy extraction | GS geometry 仍可能漂浮、缺失、弱纹理失败 | uncertainty-aware occupancy, TSDF / mesh proxy, floor-plane constraints |
| Appearance | static GS + human GS | 动态人 photorealistic，视觉 sim-to-real gap 小 | 光照变化、反射、透明物体未系统处理 | illumination editing, appearance randomization, relighting |
| Semantics | 几乎没有显式语义 | pipeline 简洁 | 无法区分 chair / wall / door / movable object | semantic GS labels, object-centric scene graph |
| Physics | 基本绕开 physics engine | 数据生成轻量，避免 mesh integration | 无接触、质量、摩擦、可操作物体动力学 | collision proxy, physics material estimation, articulated object state |
| Interaction | human path 与 robot path cross / parallel | 能制造动态避障场景 | 互动逻辑浅，human 不响应 robot policy 的复杂行为 | social navigation model, reciprocal collision avoidance, learned human planner |
| Controllability | 2D trajectory controls human motion | 可以定制障碍路径和场景 | 控制维度主要限于人类路径 | scenario DSL, event scripting, asset-level controls |
| Runtime | 3DGS 快速 rendering，小 policy 2M params | 有利于大规模数据生成和 on-board inference | 论文未充分报告 generator throughput | renderer benchmark, batching, cache occupancy / trajectories |

## 8. Evidence from Experiments

### 8.1 Dataset and Setup

- 三个目标环境: Outside、Lobby、Library。
- 每个环境用约 6 分钟 monocular video 重建。
- 每个环境 1,000 到 1,500 images。
- 使用 6 个 human GS avatars。
- 每个环境生成 400 training episodes，约 80k 到 120k samples。
- 每环境 50 validation episodes。
- Simulation evaluation: 每个 task / environment 100 episodes。
- Real-world evaluation: 每个 task / environment 10 episodes。
- 机器人: differential wheeled robot，fixed forward-facing ZED2 camera，unicycle model，Jetson Orin NX onboard inference。
- 成功定义: 50 s 内到达 goal 1 m 内。
- Metrics: Success Rate, Average Reaching Time。

### 8.2 Simulation Results

Static:

- ReaDy-Go 与 Vid2Sim 接近。
- Outside: ReaDy-Go 90% SR，Vid2Sim 89%。
- Lobby: ReaDy-Go 98%，Vid2Sim 98%。
- Library: ReaDy-Go 86%，Vid2Sim 91%。

Dynamic:

- ReaDy-Go 明显优于 Vid2Sim。
- Outside: ReaDy-Go 78%，Vid2Sim 57%。
- Lobby: ReaDy-Go 78%，Vid2Sim 70%。
- Library: ReaDy-Go 80%，Vid2Sim 68%。

解释:

- Static 下两者都受益于 target-environment real-to-sim。
- Dynamic 下差异主要来自 dynamic obstacle representation: ReaDy-Go 用 photorealistic human GS，Vid2Sim 用 Unity human asset。

### 8.3 Real-World Results

Dynamic real world:

- Outside: ReaDy-Go 90%，Vid2Sim 60%，ViNT 30%。
- Lobby: ReaDy-Go 70%，Vid2Sim 40%，ViNT 20%。
- Library: ReaDy-Go 80%，Vid2Sim 60%，ViNT 40%。

Static real world:

- Outside: ReaDy-Go 100%，Vid2Sim 90%，ViNT 50%。
- Lobby: ReaDy-Go 90%，Vid2Sim 70%，ViNT 60%。
- Library: ReaDy-Go 100%，Vid2Sim 90%，ViNT 80%。

解释:

- Environment-specific real-to-sim policy 明显优于 general navigation model。
- Photorealistic dynamic data 对动态真实环境帮助大。
- ReaDy-Go policy 只有 2M parameters，而 ViNT 是 30M。

### 8.4 Unseen Environment

- Static: SR 70%，ART 30.60 s。
- Dynamic: SR 50%，ART 35.45 s。

解释:

- 说明 policy 学到了一些通用避障行为。
- 但 dynamic unseen performance 仍然较弱。
- 要成为 open-world real2sim 方法，需要更多环境、多样 assets、语义和不确定性建模。

## 9. Failure Modes and Assumptions

### 明确假设

- 采集视频时目标环境基本静态。
- Monocular COLMAP pose 可靠。
- ArUco marker 可提供 metric scale。
- 目标任务主要是 ground robot goal navigation。
- 动态障碍主要是 humans。
- Human motion 可以由 2D trajectory + PriorMDM 生成。
- 2D occupancy map 足够支持导航规划。
- Robot 在真实部署时可获得 relative goal，论文中用 wheel odometry。

### 隐藏假设

- GS visual quality 与 planning geometry quality 足够一致。实际可能不成立。
- Opacity threshold 可以区分地面噪声和真实障碍。不同场景需要调参。
- Dynamic human GS 的视觉真实性会转化为 policy robustness。实验支持，但机制没有被完全隔离。
- 真实人类运动可由 constant velocity 2 s prediction 做安全 buffer。复杂交互会失效。
- 只有 RGB policy 可以吸收动态障碍的时序信息。三帧 history 可能不足以处理复杂遮挡和高速运动。

### 可能失败场景

- 弱纹理地面、玻璃、镜面、透明障碍导致 GS geometry 错误。
- 未观测区域被当作 free space 或 occupied space。
- 人从遮挡后突然出现，2 s constant velocity buffer 无法预测。
- 动态障碍不止人，例如推车、门、椅子移动、车辆、机器人群。
- 光照、家具布局、地面材质在采集和部署间变化大。
- Wheel odometry drift 导致 relative goal 不可靠。
- Policy 在目标环境 overfit，换环境 dynamic SR 下降。
- 无物理交互，无法支持 manipulation 或 contact-rich navigation。

## 10. Direct Relevance to My Real2Sim Platform

最直接相关的不是 policy，而是 **real2sim data generation stack**。

建议把 ReaDy-Go 拆成 6 个平台接口:

1. `SceneReconstructor`
   - 输入: video / images / poses。
   - 输出: `GSScene`。
   - 平台扩展: 加 coverage、uncertainty、semantic labels。

2. `GSGeometryExtractor`
   - 输入: `GSScene`。
   - 输出: `VoxelMap`, `Occupancy2D`, `FreeSpace2D`。
   - 平台扩展: uncertainty-aware occupancy，而非 hard threshold。

3. `DynamicAssetRegistry`
   - 输入: human GS / object GS / mesh / procedural asset。
   - 输出: object-centric assets with visual model + collision proxy + motion controller。
   - 平台扩展: 不只做人，要支持可移动物体。

4. `ScenarioFactory`
   - 输入: scene map、start-goal sampling rules、dynamic actor rules。
   - 输出: scenario configs。
   - 平台扩展: scenario DSL，可控地生成 rare events 和 partially observed cases。

5. `PlannerSupervisor`
   - 输入: simulator state、occupancy、goal、actor predictions。
   - 输出: expert action / trajectory。
   - 平台扩展: Hybrid A*、MPC、social navigation、learned world-model planner 多后端。

6. `DatasetRenderer`
   - 输入: scenario rollout。
   - 输出: `(observation, state, action, goal, metadata)`。
   - 平台扩展: 保存 hidden state、uncertainty、semantic mask、depth / normal / flow 等 training signals。

对你的研究方向，ReaDy-Go 给了一个清晰落点:

- **scene representation**: 用 3DGS 做 photorealistic substrate。
- **object completion**: 论文缺失，正是你的可贡献点。
- **asset generation**: human GS actor 是起点，可扩展到 open-world object-centric assets。
- **physical parameter estimation**: 论文基本没有，是另一个可贡献点。
- **simulator integration**: 论文轻量但弱物理，我们可以做 hybrid GS rendering + physics state。
- **evaluation metrics**: SR / ART 可复用，但要增加 real2sim quality metrics。

## 11. Minimal Prototype I Can Implement in 1 Week

目标: 不复现完整 ReaDy-Go，而是在你的 real2sim platform 中做一个 **ReaDy-Go-inspired dynamic dataset generator MVP**。

### Day 1: 输入与场景资产整理

- 选一个已有 static 3DGS scene，或者先用已有点云 / mesh / occupancy map 代替。
- 定义统一 schema:

```text
Scene:
  visual_model: GS or placeholder
  occupancy_2d: grid
  scale: meters
  bounds: x/y range

Actor:
  type: human_placeholder
  visual_model: billboard / mesh / simple capsule / GS if available
  collision_proxy: circle or capsule
  trajectory: list of poses

Robot:
  kinematics: unicycle
  radius
  camera_pose
```

### Day 2: GS / map 到 occupancy

- 如果已有 GS: 实现 `GSScene.to_occupancy_2d()` 的简化版。
- 如果没有 GS parser: 先用手工 occupancy map 或从已有 point cloud rasterize。
- 加 safety inflation。
- 输出 `robot_navigable_map` 和 `human_walkable_map`。

### Day 3: Human trajectory generator

- 采样 robot start / goal。
- 采样 human start / goal，使 human path 与 robot path cross 或 parallel。
- 用 A* 生成 seed path。
- 用简单 spline 或 moving average 平滑。
- 暂时不接 PriorMDM，用 cylinder / billboard / mesh human placeholder 表示动态人。

### Day 4: Robot expert planner

- 实现 Hybrid A* 可以较重，MVP 可先用:
  - A* on 2D grid。
  - path following controller。
  - dynamic obstacle inflation by constant velocity 2 s。
  - periodic replanning。
- 输出 expert actions `(v, w)`。

### Day 5: Lightweight renderer / logger

- 如果有 GS renderer: 从 robot camera pose 渲染 RGB。
- 如果暂时没有: 用 top-down RGB / semantic grid / synthetic camera placeholder。
- 统一记录:

```text
obs_rgb
occupancy_2d
robot_pose
human_pose
goal_relative
expert_action
collision_flag
min_distance_to_actor
scenario_metadata
```

### Day 6: Dataset generation and sanity evaluation

- 生成 100 到 300 episodes。
- 检查:
  - start / goal 是否在 free space。
  - human 是否真的 cross / parallel。
  - expert 是否能避开动态人。
  - 轨迹是否平滑。
- 输出 SR、collision rate、near-miss count、ART。

### Day 7: 接入 real2sim 质量评估

- 增加 quality report:
  - geometry coverage。
  - occupancy uncertainty placeholder。
  - interaction richness。
  - dynamic obstacle diversity。
  - controllability score。
- 写一个 notebook 或 HTML dashboard 对比 static vs dynamic scenarios。

### 一周原型不做的事

- 不训练完整 RGB policy。
- 不复现 HUGS / PriorMDM。
- 不做真实人 GS avatar。
- 不做 physics engine integration。
- 不做 open-world completion 的最终版。

### 一周原型要证明的事

这个 prototype 要证明平台里已经有一条闭环:

```text
real scene representation
  -> occupancy / state abstraction
  -> dynamic actor insertion
  -> expert rollout
  -> photorealistic or structured observation
  -> dataset + metrics
```

只要这条闭环跑通，后续就能逐步替换模块:

- placeholder visual actor -> human GS actor。
- A* expert -> Hybrid A* / MPC。
- hard occupancy -> uncertainty-aware occupancy。
- static scene -> completed multi-hypothesis scene。
- simple rollout -> world-model-guided rollout。

## 12. Final Takeaway

ReaDy-Go 最值得学习的是它把 real2sim 从“重建一个好看的 3D 场景”推进到“生成能训练 policy 的动态任务数据”。它的真正贡献在系统接口层: 3DGS rendering、occupancy extraction、dynamic actor insertion、planner supervision 和 behavior cloning 数据集。

对你的 real2sim 平台，最佳迁移策略是先复刻这个数据工厂的骨架，再把论文没有解决的部分变成你的研究贡献: unseen / partial scene completion、object-centric open-world assets、physics-aware state、uncertainty-aware planning，以及更强的 simulator quality evaluation。
