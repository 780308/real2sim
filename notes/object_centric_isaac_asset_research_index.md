# Object-Centric Isaac Asset Research Index

## 更新后的调研问题
给定单视角或多视角 RGB/RGB-D、camera poses、point cloud / depth / 3DGS 等真实观测，针对指定可交互物体生成 Isaac Sim 可用的 dual-layer asset：**3DGS visual layer + geometry/collision/physics layer**。原来的 directional view completion 仍保留，但定位为“补齐指定物体未观测面/反向视角”的子模块。

## Scoring Weights
- object-level match: 25%
- Isaac / simulator transfer: 25%
- geometry / collision / physics output: 20%
- code / weights reproducibility: 15%
- view or backside completion ability: 10%
- engineering readiness: 5%

| priority | score | method | depth | local notes |
| --- | --- | --- | --- | --- |
| P0 | 4.33 | GSWorld: Closed-Loop Photo-Realistic Simulation Suite for Robotic Manipulation | deep | notes/gsworld_object_asset_object_asset_digest.md<br>notes/gsworld_object_asset.html |
| P0 | 4.23 | Re3Sim: Generating High-Fidelity Simulation Data via 3D-Photorealistic Real-to-Sim for Robotic Manipulation | deep | notes/re3sim_object_asset_digest.md<br>notes/re3sim.html |
| P0 | 4.19 | SuGaR: Surface-Aligned Gaussian Splatting for Efficient 3D Mesh Reconstruction | deep | notes/sugar_object_asset_object_asset_digest.md<br>notes/sugar_object_asset.html |
| P0 | 4.19 | Scalable Real2Sim: Physics-Aware Asset Generation via Robotic Pick-and-Place Setups | deep | notes/scalable_real2sim_object_asset_digest.md<br>notes/scalable_real2sim.html |
| P0 | 4.06 | OpenReal2Sim: Toolbox for Real-to-Sim Reconstruction and Robotic Simulation | deep | notes/openreal2sim_object_asset_object_asset_digest.md<br>notes/openreal2sim_object_asset.html |
| P0 | 3.93 | ObjectGS: Object-aware Scene Reconstruction and Scene Understanding via Gaussian Splatting | deep | notes/objectgs_object_asset_digest.md<br>notes/objectgs.html |
| P0 | 3.91 | GaussianObject: High-Quality 3D Object Reconstruction from Four Views with Gaussian Splatting | deep | notes/gaussianobject_object_asset_digest.md<br>notes/gaussianobject.html |
| P0 | 3.88 | RoboSimGS: High-Fidelity Simulated Data Generation for Real-World Zero-Shot Robotic Manipulation Learning with Gaussian Splatting | deep | notes/robosimgs_object_asset_digest.md<br>notes/robosimgs.html |
| P0 | 3.88 | SAGE-3D: Towards Physically Executable 3D Gaussian for Embodied Navigation | deep | notes/sage_3d_object_asset_object_asset_digest.md<br>notes/sage_3d_object_asset.html |
| P0 | 3.83 | PGSR: Planar-based Gaussian Splatting for Efficient and High-Fidelity Surface Reconstruction | deep | notes/pgsr_object_asset_object_asset_digest.md<br>notes/pgsr_object_asset.html |
| P0 | 3.83 | 2D Gaussian Splatting for Geometrically Accurate Radiance Fields | deep | notes/2dgs_object_asset_object_asset_digest.md<br>notes/2dgs_object_asset.html |
| P0 | 3.73 | RoboGSim: A Real2Sim2Real Robotic Gaussian Splatting Simulator | deep | notes/robogsim_object_asset_digest.md<br>notes/robogsim.html |
| P0 | 3.63 | 3DGRT/3DGUT/3DGRUT and NVIDIA NuRec-oriented Gaussian Rendering | deep | notes/3dgrut_nurec_object_asset_object_asset_digest.md<br>notes/3dgrut_nurec_object_asset.html |
| P1 | 3.99 | Hunyuan3D-Omni: A Unified Framework for Controllable Generation of 3D Assets | standard | notes/hunyuan3d_omni_object_asset_object_asset_digest.md<br>notes/hunyuan3d_omni_object_asset.html |
| P1 | 3.89 | Hunyuan3D 2.1: From Images to High-Fidelity 3D Assets with Production-Ready PBR Material | standard | notes/hunyuan3d_21_object_asset_object_asset_digest.md<br>notes/hunyuan3d_21_object_asset.html |
| P1 | 3.83 | PhysX-3D: Physical-Grounded 3D Asset Generation | standard | notes/physx_3d_object_asset_object_asset_digest.md<br>notes/physx_3d_object_asset.html |
| P1 | 3.75 | Hunyuan3D-Part: P3-SAM and X-Part for 3D Part Segmentation and Shape Decomposition | standard | notes/hunyuan3d_part_object_asset_object_asset_digest.md<br>notes/hunyuan3d_part_object_asset.html |
| P1 | 3.71 | InstantMesh: Efficient 3D Mesh Generation from a Single Image with Sparse-view Large Reconstruction Models | standard | notes/instantmesh_object_asset_object_asset_digest.md<br>notes/instantmesh_object_asset.html |
| P1 | 3.56 | GSDF: 3DGS Meets SDF for Improved Neural Rendering and Reconstruction | standard | notes/gsdf_object_asset_object_asset_digest.md<br>notes/gsdf_object_asset.html |
| P1 | 3.46 | PhysForge: Generating Physics-Grounded 3D Assets for Interactive Virtual World | standard | notes/physforge_object_asset_object_asset_digest.md<br>notes/physforge_object_asset.html |
| P1 | 3.43 | LGM: Large Multi-View Gaussian Model for High-Resolution 3D Content Creation | standard | notes/lgm_object_asset_object_asset_digest.md<br>notes/lgm_object_asset.html |
| P1 | 3.42 | TripoSR: Fast 3D Object Reconstruction from a Single Image | standard | notes/triposr_object_asset_object_asset_digest.md<br>notes/triposr_object_asset.html |
| P1 | 3.42 | CRM: Single Image to 3D Textured Mesh with Convolutional Reconstruction Model | standard | notes/crm_object_asset_object_asset_digest.md<br>notes/crm_object_asset.html |
| P1 | 3.41 | Gaussian Grouping: Segment and Edit Anything in 3D Scenes | standard | notes/gaussian_grouping_object_asset_object_asset_digest.md<br>notes/gaussian_grouping_object_asset.html |
| P1 | 3.37 | Wonder3D: Single Image to 3D using Cross-Domain Diffusion | standard | notes/wonder3d_object_asset_object_asset_digest.md<br>notes/wonder3d_object_asset.html |
| P1 | 3.23 | RialTo: A Real-to-Sim-to-Real Approach for Robust Manipulation | standard | notes/rialto_object_asset_object_asset_digest.md<br>notes/rialto_object_asset.html |
| P1 | 3.15 | SAGA: Segment Any 3D Gaussians | standard | notes/saga_object_asset_object_asset_digest.md<br>notes/saga_object_asset.html |
| P1 | 3.08 | Splat-MOVER: Robotic Manipulation via Editable Gaussian Splatting | standard | notes/splat_mover_object_asset_object_asset_digest.md<br>notes/splat_mover_object_asset.html |
| P1 | 3.01 | GraspSplats: Efficient Manipulation with 3D Feature Splatting | standard | notes/graspsplats_object_asset_object_asset_digest.md<br>notes/graspsplats_object_asset.html |
| P1 | 3.0 | EmbodiedGen: Towards a Generative 3D World Engine for Embodied AI | standard | notes/embodiedgen_object_asset_object_asset_digest.md<br>notes/embodiedgen_object_asset.html |
| P1 | 3.0 | RoboSplat: 3DGS-based Robotic Demonstration Generation | standard | notes/robosplat_object_asset_object_asset_digest.md<br>notes/robosplat_object_asset.html |
| P1 | 2.89 | GaussianGrasper: 3D Language Gaussian Splatting for Open-vocabulary Robotic Grasping | standard | notes/gaussian_grasper_object_asset_object_asset_digest.md<br>notes/gaussian_grasper_object_asset.html |
| P1 | 2.56 | Object-Aware Gaussian Splatting for Robotic Manipulation | standard | notes/object_aware_gaussian_robotics_object_asset_digest.md<br>notes/object_aware_gaussian_robotics.html |
| P2 | 2.54 | R2G: Real-to-Generative Robot Simulation Repository | skim | notes/r2g_repo_only_object_asset_object_asset_digest.md<br>notes/r2g_repo_only_object_asset.html |
| P2 | 2.54 | 3DGen4Robot: Survey/Collection for 3D Generation in Robot Learning | skim | notes/3dgen4robot_object_asset_object_asset_digest.md<br>notes/3dgen4robot_object_asset.html |
| P2 | 2.49 | Gen2Sim: Scaling up Robot Learning in Simulation with Generative Models | skim | notes/gen2sim_object_asset_object_asset_digest.md<br>notes/gen2sim_object_asset.html |
