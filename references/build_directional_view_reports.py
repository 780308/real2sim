from __future__ import annotations

import html
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"
REF = ROOT / "ref"
REPOS = ROOT / "repos"
REGISTRY = ROOT / "references" / "source_registry.jsonl"
BIB = ROOT / "references" / "bibliography.bib"


WEIGHTS = {
    "problem_match": 0.30,
    "sim_transfer": 0.25,
    "code": 0.20,
    "consistency": 0.15,
    "cost": 0.10,
}


def score(sub):
    return round(sum(sub[k] * w for k, w in WEIGHTS.items()), 2)


def repo_meta(repo):
    if not repo:
        return {"commit": "", "license_file": ""}
    path = REPOS / repo
    if not path.exists():
        return {"commit": "", "license_file": ""}
    commit = ""
    try:
        commit = subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "--short", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        pass
    lic = ""
    for p in path.iterdir():
        if p.is_file() and p.name.lower().startswith(("license", "licence", "copying")):
            lic = p.name
            break
    return {"commit": commit, "license_file": lic}


def link(text, url):
    return f"[{text}]({url})"


ENTRIES = [
    {
        "id": "seva",
        "slug": "seva_stable_virtual_camera",
        "title": "Stable Virtual Camera (SEVA): Generative View Synthesis with Diffusion Models",
        "type": "paper+repo+weights",
        "priority": "P0",
        "review_depth": "deep",
        "family": "pose-conditioned large-angle NVS",
        "pdf": "seva_stable_virtual_camera_iccv2025.pdf",
        "repo": "stable-virtual-camera",
        "sources": [
            "https://stable-virtual-camera.github.io",
            "https://github.com/Stability-AI/stable-virtual-camera",
            "https://huggingface.co/stabilityai/stable-virtual-camera",
            "https://openaccess.thecvf.com/content/ICCV2025/html/Zhou_Stable_Virtual_Camera_Generative_View_Synthesis_with_Diffusion_Models_ICCV_2025_paper.html",
        ],
        "sub": {"problem_match": 4.8, "sim_transfer": 2.5, "code": 4.2, "consistency": 4.1, "cost": 2.8},
        "input": "任意数量 input views + target cameras/trajectory；可从 Go2 training poses 选定目标反向 yaw。",
        "output": "目标相机序列下的 RGB / multi-view video；不是 mesh 或 USD。",
        "pipeline": [
            "把 input images 编码为条件，显式输入 target camera path。",
            "diffusion model 生成目标视角序列；sampling strategy 支持不同 view synthesis tasks。",
            "输出结果可作为 pseudo observations 回灌到 3DGS/2DGS/PGSR 训练，或作为 novel-view data augmentation。",
        ],
        "objectives": "论文核心是 diffusion denoising objective + view/camera-conditioned training recipe；不直接优化 sim geometry 或 collision。",
        "assumptions": "输入视图与目标视角仍属于同一真实场景；模型允许 hallucination，因此需要 depth/pose/3DGS 重建做二次约束。",
        "failure": "大角度下可能生成 plausible 但不 metric-correct 的内容；对细窄走廊的门、墙面、可通行边界可能产生语义漂移。",
        "transfer": "visual-only；最适合作为 short-term view completion generator，不适合作为 Isaac asset 直接来源。",
        "recommendation": "第一优先级试验：在 A* 黑帧相机中心上指定反向 yaw target cameras，生成 pseudo views，再用 3DGS/PGSR 重训并检测 dark-frame ratio。",
    },
    {
        "id": "gen3c",
        "slug": "gen3c",
        "title": "GEN3C: 3D-Informed World-Consistent Video Generation with Precise Camera Control",
        "type": "paper+repo+weights",
        "priority": "P0",
        "review_depth": "deep",
        "family": "3D-informed camera-controlled world-consistent video",
        "pdf": "gen3c_3d_informed_world_consistent_video_generation.pdf",
        "repo": "GEN3C",
        "sources": [
            "https://research.nvidia.com/labs/toronto-ai/GEN3C/",
            "https://github.com/nv-tlabs/GEN3C",
            "https://huggingface.co/nvidia/GEN3C-Cosmos-7B",
        ],
        "sub": {"problem_match": 5.0, "sim_transfer": 2.8, "code": 4.3, "consistency": 4.5, "cost": 2.0},
        "input": "single/multi-view image, camera path, depth/pose informed conditioning；README 支持 interactive GUI author arbitrary camera trajectories。",
        "output": "camera-controlled video / novel views；后续版本还关联 Lyra static/dynamic 3DGS decoder。",
        "pipeline": [
            "先用 3D information 帮模型理解已观测结构，而不是只靠 pose token。",
            "在推理时给定任意 camera trajectory，模型把生成能力集中到 unobserved regions 和时序推进。",
            "可通过 multi-view inference 或 video-to-video pipeline 与真实采集片段对齐。",
        ],
        "objectives": "视频扩散/生成 objective，强调 temporal 3D consistency 和 precise camera control；不是显式 geometry loss 的重建器。",
        "assumptions": "需要大模型权重和较高 GPU 资源；license 包括 NVIDIA Open Model License，需要确认项目合规。",
        "failure": "视频一致性强于普通 video model，但仍可能在 metric scale、障碍物边界和地面可通行区域上不可靠。",
        "transfer": "visual-only / pseudo-view generator；若结合 Lyra 或 3DGS decoder，可作为中期 3DGS 修复方向。",
        "recommendation": "与 SEVA 并列 P0。若算力允许，优先用 GEN3C 做 camera-controlled 反向 yaw 补帧，因为它的问题表述最贴合 directional view gap。",
    },
    {
        "id": "mvgd",
        "slug": "mvgd",
        "title": "MVGD: Zero-Shot Novel View and Depth Synthesis with Multi-View Geometric Diffusion",
        "type": "paper",
        "priority": "P0",
        "review_depth": "deep",
        "family": "novel view + scale-consistent depth synthesis",
        "pdf": "mvgd_cvpr2025.pdf",
        "repo": "",
        "sources": [
            "https://openaccess.thecvf.com/content/CVPR2025/html/Guizilini_Zero-Shot_Novel_View_and_Depth_Synthesis_with_Multi-View_Geometric_Diffusion_CVPR_2025_paper.html",
        ],
        "sub": {"problem_match": 4.8, "sim_transfer": 3.2, "code": 1.5, "consistency": 4.7, "cost": 3.2},
        "input": "sparse posed images / target viewpoints。",
        "output": "novel RGB + scale-consistent depth maps。",
        "pipeline": [
            "用 geometric diffusion 直接生成目标视角 RGB 和 depth，而不是先建完整 radiance field。",
            "输出 depth 使 pseudo-view 不只停留在 RGB，可以参与 TSDF、mesh、PGSR 或 Isaac collision proxy。",
            "zero-shot 设定降低重新训练成本，但工程可复现性取决于代码/权重公开状态。",
        ],
        "objectives": "diffusion generation objective + multi-view geometric/depth consistency 约束。",
        "assumptions": "论文路线很适合本问题，但本轮未找到完整官方 repo；只能作为方法强参考。",
        "failure": "若代码不可用，短期落地弱；depth 虽 scale-consistent，仍需和 Go2 metric scale / point cloud 校准。",
        "transfer": "adapter needed；比纯 RGB NVS 更接近 Isaac，因为 depth 可参与 mesh/collision。",
        "recommendation": "若官方或第三方实现可用，应升级为 SEVA/GEN3C 后的第二个验证模块。",
    },
    {
        "id": "cat3d",
        "slug": "cat3d",
        "title": "CAT3D: Create Anything in 3D with Multi-View Diffusion Models",
        "type": "paper",
        "priority": "P0",
        "review_depth": "deep",
        "family": "multi-view diffusion for reconstruction input synthesis",
        "pdf": "cat3d_2405_10314.pdf",
        "repo": "",
        "sources": ["https://cat3d.github.io", "https://arxiv.org/abs/2405.10314"],
        "sub": {"problem_match": 4.4, "sim_transfer": 2.8, "code": 1.2, "consistency": 4.4, "cost": 3.2},
        "input": "任意数量 input images + target novel viewpoints。",
        "output": "multi-view consistent generated views，可送入 3D reconstruction。",
        "pipeline": [
            "模拟真实 capture process：从少量输入合成一批目标相机视角。",
            "把生成视图交给已有 3D reconstruction 技术产出 3D representation。",
            "适合补齐 Go2 未覆盖 yaw 后再训练 3DGS/mesh。",
        ],
        "objectives": "multi-view diffusion generation objective；不直接估计物理属性。",
        "assumptions": "公开资料以论文/项目页为主，代码可用性不足；更适合作为策略范式而非第一工程依赖。",
        "failure": "可能生成与真实局部不完全一致的 backside content；无显式 collision guarantee。",
        "transfer": "adapter needed；作为 pseudo-view synthesis 前端。",
        "recommendation": "保留为强方法参考，短期优先使用有代码/权重的 SEVA/GEN3C 替代。",
    },
    {
        "id": "cat4d",
        "slug": "cat4d",
        "title": "CAT4D: Create Anything in 4D with Multi-View Video Diffusion Models",
        "type": "paper",
        "priority": "P1",
        "review_depth": "standard",
        "family": "dynamic multi-view video diffusion",
        "pdf": "cat4d_cvpr2025.pdf",
        "repo": "",
        "sources": ["https://cat-4d.github.io", "https://openaccess.thecvf.com/content/CVPR2025/html/Wu_CAT4D_Create_Anything_in_4D_with_Multi-View_Video_Diffusion_Models_CVPR_2025_paper.html"],
        "sub": {"problem_match": 3.6, "sim_transfer": 2.4, "code": 1.2, "consistency": 4.1, "cost": 2.4},
        "input": "monocular video + specified camera poses/timestamps。",
        "output": "multi-view video for dynamic 4D scenes。",
        "pipeline": ["从单目视频生成指定 camera/time 的多视角视频。", "可扩展 ReaDy-Go 式 dynamic actor/obstacle，但当前问题先聚焦静态走廊。"],
        "objectives": "multi-view video diffusion objective。",
        "assumptions": "动态能力强，但静态 directional gap 不是它最直接的目标。",
        "failure": "可能过度关注时间变化；无直接 Isaac geometry/collision 输出。",
        "transfer": "visual-only；作为长期 dynamic extension。",
        "recommendation": "P1。先不投入工程验证，等静态方向补全闭环成立后再回看。",
    },
    {
        "id": "genrc",
        "slug": "genrc",
        "title": "GenRC: Generative 3D Room Completion from Sparse Image Collections",
        "type": "paper",
        "priority": "P0",
        "review_depth": "deep",
        "family": "room-scale RGB-D mesh completion",
        "pdf": "genrc_eccv2024.pdf",
        "repo": "",
        "sources": ["https://minfenli.github.io/GenRC/", "https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/5406_ECCV_2024_paper.php"],
        "sub": {"problem_match": 4.4, "sim_transfer": 4.2, "code": 1.4, "consistency": 4.0, "cost": 3.0},
        "input": "sparse RGB-D images / sparse image collections。",
        "output": "room-scale completed 3D mesh with texture。",
        "pipeline": [
            "把 sparse RGB-D 投影为 highly incomplete 3D mesh。",
            "用 E-Diffusion 生成 view-consistent panoramic RGB-D，保证 global geometry/appearance consistency。",
            "把补全后的 panoramic RGB-D 融合为完整 room mesh。",
        ],
        "objectives": "training-free pipeline，核心依赖 diffusion prior 和 RGB-D consistency；不是 end-to-end supervised scene completion。",
        "assumptions": "非常贴合室内/走廊，且输出 mesh；但本轮未确认官方代码完整可用。",
        "failure": "completion 可能补出合理但错误的房间拓扑；门后/转角等 high uncertainty 区域要标注置信度。",
        "transfer": "adapter needed but strong；mesh 输出最接近 Isaac USD/collision proxy。",
        "recommendation": "作为 mid-term 主线：补视觉后，GenRC/SceneCompleter/Seen2Scene 负责把低覆盖区域转成物理几何假设。",
    },
    {
        "id": "scenecompleter",
        "slug": "scenecompleter",
        "title": "SceneCompleter: Dense 3D Scene Completion for Generative Novel View Synthesis",
        "type": "paper",
        "priority": "P0",
        "review_depth": "deep",
        "family": "dense 3D completion for generative NVS",
        "pdf": "scenecompleter_2506_10981.pdf",
        "repo": "",
        "sources": ["https://arxiv.org/abs/2506.10981"],
        "sub": {"problem_match": 4.7, "sim_transfer": 3.7, "code": 1.2, "consistency": 4.5, "cost": 3.0},
        "input": "partial 3D / generated novel-view context；关注 2D inpainting 导致 geometry distortion 的问题。",
        "output": "dense completed 3D scene representation for NVS。",
        "pipeline": [
            "先补 dense 3D scene，而不是逐帧 2D inpainting。",
            "用完整 3D 表示约束 generative novel view synthesis，降低 appearance drift。",
            "更适合在 3DGS 黑洞处生成结构先验，再渲染多视角。",
        ],
        "objectives": "3D completion + generative NVS consistency；论文强调避免 2D inpainting paradigm 的几何漂移。",
        "assumptions": "代码状态不明；需要验证输入格式是否能接 Go2 3DGS/point cloud。",
        "failure": "若场景拓扑先验错误，所有补视角会一致地错；需 uncertainty map 和 active re-capture 对照。",
        "transfer": "adapter needed；比纯 world model 更适合 Isaac 的几何中间层。",
        "recommendation": "P0 方法参考，工程上排在有代码的 SEVA/GEN3C/PGSR/OpenReal2Sim 之后。",
    },
    {
        "id": "gld",
        "slug": "gld",
        "title": "Geometric Latent Diffusion (GLD): Multi-view Diffusion with Geometric Foundation Models",
        "type": "repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "geometry-latent multi-view diffusion",
        "pdf": "",
        "repo": "GLD",
        "sources": ["https://github.com/cvlab-kaist/GLD", "https://arxiv.org/abs/2603.22275", "https://huggingface.co/SeonghuJeon/GLD"],
        "sub": {"problem_match": 4.2, "sim_transfer": 3.0, "code": 4.0, "consistency": 4.2, "cost": 1.8},
        "input": "multi-view inputs and cameras；使用 Depth Anything 3 / VGGT feature space。",
        "output": "NVS outputs；demo 还能生成 GLB + COLMAP 3D reconstructions。",
        "pipeline": ["在 geometric foundation model latent space 中做 multi-view diffusion。", "用 depth/geometry backbone 约束 zero-shot geometry。", "demo 输出可用于后续 mesh/GLB 实验。"],
        "objectives": "multi-view diffusion objective in geometric latent space。",
        "assumptions": "需要 48GB+ VRAM，工程成本高；2026 新项目，需复现实测。",
        "failure": "高资源门槛；foundation geometry 可能不适配低纹理走廊。",
        "transfer": "adapter needed；GLB 输出使其比普通 NVS 更接近 sim asset。",
        "recommendation": "P1+。作为 MVGD/SEVA 的几何增强替代，若硬件可用值得验证。",
    },
    {
        "id": "pgsr",
        "slug": "pgsr",
        "title": "PGSR: Planar-based Gaussian Splatting for Efficient and High-Fidelity Surface Reconstruction",
        "type": "paper+repo",
        "priority": "P0",
        "review_depth": "deep",
        "family": "3DGS geometry regularization / mesh extraction",
        "pdf": "pgsr_2406_06521.pdf",
        "repo": "PGSR",
        "sources": ["https://zju3dv.github.io/pgsr/", "https://github.com/zju3dv/PGSR", "https://arxiv.org/abs/2406.06521"],
        "sub": {"problem_match": 3.5, "sim_transfer": 4.0, "code": 4.0, "consistency": 4.3, "cost": 3.2},
        "input": "multi-view RGB / SfM poses；无需预训练 depth/normal prior。",
        "output": "planar-constrained 3DGS and surface reconstruction / mesh。",
        "pipeline": ["用 planar-based Gaussian 表达增强 surface alignment。", "通过 multi-view constraints 提高 geometry accuracy。", "用于把 pseudo views + 原始 views 重训成更适合 mesh/Isaac 的表示。"],
        "objectives": "RGB reconstruction + planar/geometric regularization；目标是高保真 surface reconstruction。",
        "assumptions": "不能凭空补未观测反向内容；必须与 NVS 或补采集结合。",
        "failure": "若 pseudo views 错误，PGSR 会把错误几何固化；需要 confidence weighting。",
        "transfer": "adapter needed but strong；可作为 GS-to-surface bridge。",
        "recommendation": "P0 工程后端：SEVA/GEN3C 生成反向视角后，用 PGSR 验证重训是否减少黑洞并改善 mesh。",
    },
    {
        "id": "sugar",
        "slug": "sugar",
        "title": "SuGaR: Surface-Aligned Gaussian Splatting for Efficient 3D Mesh Reconstruction",
        "type": "paper+repo",
        "priority": "P0",
        "review_depth": "deep",
        "family": "3DGS-to-mesh extraction",
        "pdf": "sugar_2311_12775.pdf",
        "repo": "SuGaR",
        "sources": ["https://anttwo.github.io/sugar/", "https://github.com/Anttwo/SuGaR", "https://arxiv.org/abs/2311.12775"],
        "sub": {"problem_match": 3.2, "sim_transfer": 4.5, "code": 4.4, "consistency": 4.0, "cost": 3.4},
        "input": "vanilla 3DGS checkpoint or COLMAP dataset。",
        "output": "mesh, textured mesh, hybrid Mesh+Gaussians representation。",
        "pipeline": ["短 3DGS optimization。", "SuGaR optimization 让 Gaussians align with surface。", "mesh extraction 和 mesh+Gaussian refinement。"],
        "objectives": "surface alignment regularization + mesh/Gaussian refinement。",
        "assumptions": "它修几何和导 mesh，不生成缺失反向视角。",
        "failure": "在 directional holes 中会抽出错误或缺失 mesh；需先补观测或加 completion。",
        "transfer": "direct-ish for Isaac after USD conversion；作为 mesh/collision 生成工具。",
        "recommendation": "P0 支撑模块：不解决 root cause，但对 Isaac Sim 长期目标必需。",
    },
    {
        "id": "2dgs",
        "slug": "2d_gaussian_splatting",
        "title": "2D Gaussian Splatting for Geometrically Accurate Radiance Fields",
        "type": "paper+repo",
        "priority": "P0",
        "review_depth": "deep",
        "family": "surfel Gaussian representation / mesh extraction",
        "pdf": "2d_gaussian_splatting_2403_17888.pdf",
        "repo": "2d-gaussian-splatting",
        "sources": ["https://surfsplatting.github.io/", "https://github.com/hbb1/2d-gaussian-splatting", "https://arxiv.org/abs/2403.17888"],
        "sub": {"problem_match": 3.4, "sim_transfer": 4.2, "code": 4.2, "consistency": 4.2, "cost": 3.2},
        "input": "COLMAP/NeRF-style posed images。",
        "output": "2D surfel Gaussians, rendered RGB/depth, mesh extraction including unbounded scenes。",
        "pipeline": ["用 2D oriented disks/surfels 取代无结构 3D Gaussian ellipsoids。", "normal consistency / depth distortion regularization。", "TSDF/adaptive meshing 输出 mesh。"],
        "objectives": "RGB rendering loss + normal/depth/distortion regularization。",
        "assumptions": "同样不能无中生有补 unseen yaw，但在有 pseudo views 后更适合 surface geometry。",
        "failure": "输入视角不足时会过拟合已见表面；走廊反向墙面需额外 NVS/采集。",
        "transfer": "adapter needed；mesh extraction 对 Isaac 有价值。",
        "recommendation": "P0 后处理候选，与 PGSR/SuGaR 共同组成 GS repair baseline。",
    },
    {
        "id": "gs_playground",
        "slug": "gs_playground",
        "title": "GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning",
        "type": "paper+repo",
        "priority": "P0",
        "review_depth": "deep",
        "family": "3DGS simulator / real2sim framework",
        "pdf": "gs_playground_2604_25459.pdf",
        "repo": "gs_playground",
        "sources": ["https://gsplayground.github.io", "https://github.com/discoverse-dev/gs_playground", "https://arxiv.org/abs/2604.25459"],
        "sub": {"problem_match": 3.8, "sim_transfer": 4.8, "code": 4.0, "consistency": 3.8, "cost": 3.0},
        "input": "3DGS assets + robot/physics assets；Real2Sim workflow via GS-Real2Sim。",
        "output": "batched RGB/depth observations, contact/physics integration, sim-ready assets。",
        "pipeline": ["把 parallel physics engine 与 batch 3DGS rendering 耦合。", "Rigid-Link Gaussian Kinematics 将 Gaussian clusters 绑定刚体。", "支持 navigation/manipulation/locomotion 视觉 RL。"],
        "objectives": "系统框架，不是单个 learning loss；重点是 throughput、synchronized visuals、asset packaging。",
        "assumptions": "README 标注 full Real2Sim asset packaging/collision sync 仍在 release plan；Isaac 不是主后端。",
        "failure": "它不主动补 unseen yaw；坏 3DGS 进来仍会坏。",
        "transfer": "adapter needed；是 Isaac 之外最重要的 sim architecture reference。",
        "recommendation": "P0 平台参考。吸收 batch 3DGS observation + physics separation，但 directional completion 仍靠 NVS/completion 模块。",
    },
    {
        "id": "gaussgym",
        "slug": "gaussgym",
        "title": "GaussGym: An Open-Source Real-to-Sim Framework for Learning Locomotion from Pixels",
        "type": "paper",
        "priority": "P0",
        "review_depth": "deep",
        "family": "real-to-sim 3DGS locomotion framework",
        "pdf": "gaussgym_2510_15352.pdf",
        "repo": "",
        "sources": ["https://arxiv.org/abs/2510.15352"],
        "sub": {"problem_match": 3.6, "sim_transfer": 4.4, "code": 2.0, "consistency": 3.5, "cost": 3.0},
        "input": "phone scan/video or generative video model outputs + 3DGS rendering integrated with IsaacGym-style pipeline。",
        "output": "photorealistic high-throughput robot learning environment。",
        "pipeline": ["把 3D Gaussian renderer 集成到 GPU robot simulation。", "支持从手机扫描/视频模型构建真实感世界。", "用于 pixel-based locomotion policy training。"],
        "objectives": "系统框架与 RL performance；不是 view completion loss。",
        "assumptions": "paper 可得，但本轮未确认官方 repo 完整可用。",
        "failure": "它是整合路径，不解决反向视角观测缺失；对 geometry/collision 细节需继续核验。",
        "transfer": "adapter needed / possibly direct if IsaacGym branch available。",
        "recommendation": "P0 概念参考，工程优先级低于 OpenReal2Sim/GS-Playground，因为代码证据较弱。",
    },
    {
        "id": "openreal2sim",
        "slug": "openreal2sim",
        "title": "OpenReal2Sim: Toolbox for Real-to-Sim Reconstruction and Robotic Simulation",
        "type": "repo",
        "priority": "P0",
        "review_depth": "deep",
        "family": "sim-ready real2sim toolbox",
        "pdf": "",
        "repo": "OpenReal2Sim",
        "sources": ["https://github.com/PointsCoder/OpenReal2Sim"],
        "sub": {"problem_match": 4.0, "sim_transfer": 5.0, "code": 4.5, "consistency": 3.6, "cost": 2.8},
        "input": "single image / monocular video / GT depth image；preprocess 得到 metric depth、intrinsics/extrinsics、dynamic point clouds。",
        "output": "background/object meshes, scene.json, GLB/mesh assets, IsaacLab USD conversion, grasp/trajectory demos。",
        "pipeline": ["preprocess: image extraction, metric depth prediction/calibration, camera estimation。", "reconstruction: object segmentation, background pixel/point inpainting, background/object mesh generation, scenario construction, pose/collision optimization。", "simulation: IsaacLab USD conversion, Maniskill/MuJoCo support, trajectory replay and heuristic manipulation。"],
        "objectives": "系统 pipeline；核心是 mesh/scene construction 和 simulator import，不是 NVS loss。",
        "assumptions": "非常贴合最终 Isaac Sim 目标，但更多面向 object-centric manipulation；需要改造成走廊/导航场景。",
        "failure": "background inpainting/point inpainting 可能过于单图/局部；未显式解决 large-angle camera-conditioned view consistency。",
        "transfer": "direct for IsaacLab/Isaac Sim path；是本项目 mid-term integration anchor。",
        "recommendation": "P0 平台主线。把 NVS/scene-completion 模块接在 preprocess/reconstruction 之间，最终走 USD conversion。",
    },
    {
        "id": "hy_world_2",
        "slug": "hy_world_2",
        "title": "HY-World 2.0: Multi-Modal World Model for 3D World Generation and Reconstruction",
        "type": "tech report+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "open 3D world model",
        "pdf": "hy_world_2_0_tech_report.pdf",
        "repo": "HY-World-2.0",
        "sources": ["https://3d.hunyuan.tencent.com/sceneTo3D", "https://github.com/Tencent-Hunyuan/HY-World-2.0"],
        "sub": {"problem_match": 3.8, "sim_transfer": 4.0, "code": 4.2, "consistency": 3.5, "cost": 1.8},
        "input": "text, single-view image, multi-view images, video。",
        "output": "3D world representations: meshes / 3DGS / point cloud / depth / normals / camera parameters。",
        "pipeline": ["World Generation: HY-Pano 2.0 -> WorldNav -> WorldStereo 2.0 -> WorldMirror 2.0 + 3DGS learning。", "World Reconstruction: WorldMirror 2.0 feed-forward predicts depth, normals, camera, point cloud, 3DGS attributes。", "README 明确可导入 Blender/Unity/Unreal/Isaac 类引擎。"],
        "objectives": "多模型组合 world generation/reconstruction；报告重在系统能力而非单一 loss。",
        "assumptions": "世界模型会生成 plausible 3D world，但未必 metric-align 到 Go2 真实走廊；需要真实几何约束和局部锁定。",
        "failure": "可能改变拓扑/物体布局；如果无约束替换原场景，会损害 real2sim fidelity。",
        "transfer": "adapter needed but promising；mesh/3DGS 输出和 Isaac 兼容表述使其比纯 video world model 更有用。",
        "recommendation": "P1 强候选：作为 semantic/geometry prior，不作为第一主线。",
    },
    {
        "id": "inspatio",
        "slug": "inspatio_worldfm",
        "title": "InSpatio-WorldFM: Open-Source Real-Time Generative Frame Model",
        "type": "paper+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "interactive world/video frame model",
        "pdf": "inspatio_worldfm_2603_11911.pdf",
        "repo": "inspatio-world",
        "sources": ["https://inspatio.github.io/inspatio-world/", "https://github.com/inspatio/inspatio-world", "https://huggingface.co/inspatio/world"],
        "sub": {"problem_match": 3.5, "sim_transfer": 2.5, "code": 4.0, "consistency": 3.2, "cost": 2.0},
        "input": "video/image states and controls for real-time frame generation。",
        "output": "interactive/generated frames; not persistent mesh/USD。",
        "pipeline": ["real-time frame model for spatial intelligence。", "支持 checkpoint 下载和 v2v inference。", "更像 interactive visual simulator，而非 metric reconstruction。"],
        "objectives": "world/frame generation objective。",
        "assumptions": "开放且可运行，但输出仍偏 video/frame，不直接适合 collision。",
        "failure": "缺少 metric 3D anchoring；可能对走廊几何漂移。",
        "transfer": "visual-only；可作为 long-term policy/world-model data generator。",
        "recommendation": "P1。可调研但不作为 directional view completion 第一优先级。",
    },
    {
        "id": "lingbot_world",
        "slug": "lingbot_world",
        "title": "LingBot-World: Open-Source World Simulator from Video Generation",
        "type": "paper+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "camera/action-conditioned video world model",
        "pdf": "lingbot_world_2601_20540.pdf",
        "repo": "lingbot-world",
        "sources": ["https://github.com/robbyant/lingbot-world", "https://huggingface.co/collections/robbyant/lingbot-world", "https://arxiv.org/abs/2601.20540"],
        "sub": {"problem_match": 3.9, "sim_transfer": 2.3, "code": 4.2, "consistency": 3.4, "cost": 2.2},
        "input": "initial frames + camera poses or actions；README 使用 poses.npy [num_frames,4,4] OpenCV transforms。",
        "output": "long-horizon camera/action-conditioned videos。",
        "pipeline": ["Base(Cam) / Base(Act) / Fast 模型支持 camera poses 或 actions。", "用 run scripts 生成长时域视频。", "可用于模拟反向 camera motion，但不产生 3D assets。"],
        "objectives": "video world model generation objective。",
        "assumptions": "camera-conditioned 是亮点；但 geometry anchoring 比 SEVA/GEN3C 弱。",
        "failure": "长视频可能保持视觉连续但不保持 metric scene structure；不可直接用于 Isaac collision。",
        "transfer": "visual-only。",
        "recommendation": "P1。作为开放 world model 对照组，比较它和 SEVA/GEN3C 在反向 yaw pseudo views 的漂移差异。",
    },
    {
        "id": "bwm",
        "slug": "boundless_world_model",
        "title": "Boundless World Model (BWM)",
        "type": "repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "action-conditioned robot video world model",
        "pdf": "",
        "repo": "boundless-world-model",
        "sources": ["https://github.com/boundless-large-model/boundless-world-model", "https://huggingface.co/BLM-Lab/Boundless-World-Model"],
        "sub": {"problem_match": 2.7, "sim_transfer": 2.0, "code": 3.5, "consistency": 3.0, "cost": 2.3},
        "input": "initial frames + robot action sequences。",
        "output": "action-conditioned robot manipulation videos。",
        "pipeline": ["基于 Wan2.2-TI2V-5B；已释放 inference code/model definition/weights。", "训练代码和 technical report 仍 TODO。", "WorldArena 机器人 manipulation videos 表现强。"],
        "objectives": "action-conditioned video generation。",
        "assumptions": "主要用于 manipulation，不是 room-scale static geometry completion。",
        "failure": "无法输出 mesh/USD；对 Go2 走廊反向 yaw 只是视觉预测参考。",
        "transfer": "visual-only / not suitable for geometry。",
        "recommendation": "P1/P2 边界。保留在开放 world model 对照组，不投入主线工程。",
    },
    {
        "id": "tau0_wm",
        "slug": "tau0_wm",
        "title": "τ0-WM: A Unified Video-Action World Model for Robotic Manipulation",
        "type": "paper",
        "priority": "P1",
        "review_depth": "standard",
        "family": "video-action manipulation world model",
        "pdf": "tau0_wm_2606_01027.pdf",
        "repo": "",
        "sources": ["https://arxiv.org/abs/2606.01027"],
        "sub": {"problem_match": 2.5, "sim_transfer": 2.0, "code": 1.2, "consistency": 3.0, "cost": 2.5},
        "input": "robot observation/action sequences。",
        "output": "future video prediction, action evaluation, policy-related outputs。",
        "pipeline": ["共享未来预测框架同时服务 policy learning、video prediction、action evaluation。", "目标是 manipulation action grounding。"],
        "objectives": "video-action prediction/evaluation objectives。",
        "assumptions": "方向与 embodied world model 有关，但与静态走廊 large-angle view completion 间接。",
        "failure": "无 geometry/collision asset；没有直接补 3DGS 黑洞路线。",
        "transfer": "not suitable for current visual asset completion。",
        "recommendation": "P1 低位，仅在最终报告中作为 world-model 辅助方向。",
    },
    {
        "id": "kairos",
        "slug": "kairos",
        "title": "Kairos: Native World Model Stack for Physical AI",
        "type": "paper+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "general physical-AI world model stack",
        "pdf": "kairos_2606_16533.pdf",
        "repo": "kairos-sensenova",
        "sources": ["https://github.com/kairos-agi/kairos-sensenova", "https://huggingface.co/collections/kairos-agi/kairos30", "https://arxiv.org/abs/2606.16533"],
        "sub": {"problem_match": 2.8, "sim_transfer": 2.0, "code": 3.5, "consistency": 3.2, "cost": 1.8},
        "input": "open-world videos, human behavior data, robot interactions。",
        "output": "video/world-model predictions for physical AI reasoning and robot tasks。",
        "pipeline": ["Native pre-training paradigm + cross-embodiment data curriculum。", "README 提供 multiple model weights for robot/general generation。"],
        "objectives": "large world model pretraining and downstream task objectives。",
        "assumptions": "范围太大，不是针对 view completion；资料多但工程迁移路径不短。",
        "failure": "可能给出漂亮预测但不 metric align；无 direct Isaac asset。",
        "transfer": "visual/model prior only。",
        "recommendation": "P1 低位。作为 long-term world prior，不作为近期解决方案。",
    },
    {
        "id": "sgnn",
        "slug": "sgnn",
        "title": "SG-NN: Sparse Generative Neural Networks for Self-Supervised Scene Completion of RGB-D Scans",
        "type": "paper+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "RGB-D scan geometry completion",
        "pdf": "sgnn_cvpr2020.pdf",
        "repo": "sgnn",
        "sources": ["https://github.com/angeladai/sgnn", "https://arxiv.org/abs/1912.00036"],
        "sub": {"problem_match": 3.8, "sim_transfer": 4.0, "code": 3.5, "consistency": 3.6, "cost": 2.5},
        "input": "partial/noisy RGB-D scans。",
        "output": "completed high-resolution 3D reconstruction / unseen geometry。",
        "pipeline": ["self-supervised: 从 incomplete scan 中移除 frames 构造更不完整输入。", "sparse generative network 预测 missing geometry。", "marching cubes 可视化 surface。"],
        "objectives": "self-supervised scene completion losses。",
        "assumptions": "老项目依赖 Python 2.7 / PyTorch 1.1 / SparseConvNet，工程成本较高。",
        "failure": "几何补全不处理 photorealistic texture；需另接 NVS/texture pipeline。",
        "transfer": "adapter needed；可作为 geometry-only baseline。",
        "recommendation": "P1。方法理念值得借鉴，直接复现优先级低于 Seen2Scene/GenRC。",
    },
    {
        "id": "seen2scene",
        "slug": "seen2scene",
        "title": "Seen2Scene: Completing Realistic 3D Scenes with Visibility-Guided Flow",
        "type": "repo",
        "priority": "P1",
        "review_depth": "standard",
        "family": "real-scan 3D scene completion",
        "pdf": "",
        "repo": "seen2scene",
        "sources": ["https://github.com/quan-meng/seen2scene", "https://arxiv.org/abs/2603.28548"],
        "sub": {"problem_match": 4.0, "sim_transfer": 4.0, "code": 2.0, "consistency": 4.0, "cost": 2.5},
        "input": "incomplete real-world 3D scans, TSDF sparse grids, layout boxes。",
        "output": "completed realistic 3D scenes。",
        "pipeline": ["visibility-guided flow matching mask unknown regions in real scans。", "sparse transformer models complex scene structures。", "layout boxes provide conditioning。"],
        "objectives": "flow matching objective with visibility masking。",
        "assumptions": "repo 当前很轻，完整代码/weights 状态需持续跟踪；但问题定义极贴合 partial observation。",
        "failure": "需要 TSDF/scan preprocessing；与 Go2 3DGS/point cloud 的接口需实现。",
        "transfer": "adapter needed; strong for Isaac mesh proxy if code matures。",
        "recommendation": "P1+。作为 GenRC/SceneCompleter 的最新替代线持续关注。",
    },
    {
        "id": "voxformer",
        "slug": "voxformer",
        "title": "VoxFormer: Sparse Voxel Transformer for Camera-based 3D Semantic Scene Completion",
        "type": "paper+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "semantic scene completion",
        "pdf": "voxformer_2302_12251.pdf",
        "repo": "VoxFormer",
        "sources": ["https://github.com/NVlabs/VoxFormer", "https://arxiv.org/abs/2302.12251"],
        "sub": {"problem_match": 3.0, "sim_transfer": 3.0, "code": 3.6, "consistency": 3.5, "cost": 2.8},
        "input": "single/multiple camera images; depth-estimated sparse visible voxels。",
        "output": "dense 3D semantic voxels。",
        "pipeline": ["stage 1 query proposal from depth-estimated visible structures。", "stage 2 masked autoencoder propagates information to full voxel volume。"],
        "objectives": "semantic occupancy completion losses。",
        "assumptions": "户外自动驾驶语境强；室内 Go2 走廊需 domain adaptation。",
        "failure": "语义 voxel 不等于 textured mesh/NVS；不补 RGB 画面。",
        "transfer": "adapter needed; useful as uncertainty/occupancy prior。",
        "recommendation": "P1 baseline，用于生成 occupancy prior，不作为视觉补帧主线。",
    },
    {
        "id": "symphonies",
        "slug": "symphonies",
        "title": "Symphonies: 3D Semantic Scene Completion with Contextual Instance Queries",
        "type": "paper+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "semantic scene completion",
        "pdf": "symphonies_2306_15670.pdf",
        "repo": "Symphonies",
        "sources": ["https://github.com/hustvl/Symphonies", "https://arxiv.org/abs/2306.15670"],
        "sub": {"problem_match": 2.8, "sim_transfer": 3.0, "code": 3.8, "consistency": 3.7, "cost": 2.5},
        "input": "camera images/depth predictions on SemanticKITTI/KITTI-360 style data。",
        "output": "3D semantic occupancy/voxels。",
        "pipeline": ["contextual instance queries 建模场景实例与上下文。", "输出 semantic scene completion。"],
        "objectives": "semantic voxel completion losses。",
        "assumptions": "自动驾驶数据域，室内/Isaac asset 需要转换。",
        "failure": "不生成 texture / photorealistic novel view；仅作为语义/occupancy prior。",
        "transfer": "adapter needed。",
        "recommendation": "P1 低位，作为 occupancy prior 代表，不建议优先实现。",
    },
    {
        "id": "omni_3dgs_extension",
        "slug": "omni_3dgs_extension",
        "title": "Omniverse 3D Gaussian Splatting Extension",
        "type": "repo",
        "priority": "P1",
        "review_depth": "standard",
        "family": "Isaac/Omniverse 3DGS integration",
        "pdf": "",
        "repo": "omni-3dgs-extension",
        "sources": ["https://github.com/j3soon/omni-3dgs-extension"],
        "sub": {"problem_match": 2.8, "sim_transfer": 4.5, "code": 4.0, "consistency": 2.8, "cost": 3.0},
        "input": "3DGS scene files and Isaac Sim/Omniverse container setup。",
        "output": "3DGS rendering inside Omniverse/Isaac Sim extension。",
        "pipeline": ["Docker-based Isaac Sim extension loads 3DGS renderer/viewer。", "可作为视觉 layer 接入 Isaac，但不处理 geometry/collision。"],
        "objectives": "engineering integration, no learning objective。",
        "assumptions": "Linux/RTX/Docker/IsaacSim 约束；适合后端验证。",
        "failure": "只解决渲染，不解决 black holes 或 physical asset。",
        "transfer": "direct for visual Isaac integration; no collision。",
        "recommendation": "P1 工具。若短期只要 Isaac camera RGB，可以优先试；若要物理交互，需 OpenReal2Sim/SuGaR mesh。",
    },
    {
        "id": "real2sim_eval",
        "slug": "real2sim_eval",
        "title": "Real-to-Sim Robot Policy Evaluation with Gaussian Splatting Simulation of Soft-Body Interactions",
        "type": "repo",
        "priority": "P2",
        "review_depth": "skim",
        "family": "policy evaluation / GS simulator",
        "pdf": "",
        "repo": "real2sim-eval",
        "sources": ["https://github.com/kywind/real2sim-eval"],
        "sub": {"problem_match": 2.0, "sim_transfer": 3.2, "code": 3.0, "consistency": 2.5, "cost": 2.8},
        "input": "Gaussian Splatting simulation setup for robot policy evaluation。",
        "output": "policy evaluation environment, soft-body interaction demos。",
        "pipeline": ["关注 robot policy evaluation rather than scene completion。"],
        "objectives": "simulation/evaluation pipeline。",
        "assumptions": "与导航走廊和 Isaac asset 间接相关。",
        "failure": "不补视角，不输出完整场景几何。",
        "transfer": "supplementary only。",
        "recommendation": "P2。最终报告中作为 evaluation 思路参考即可。",
    },
    {
        "id": "worldarena",
        "slug": "worldarena",
        "title": "WorldArena: Benchmark for Embodied World Models",
        "type": "repo",
        "priority": "P2",
        "review_depth": "skim",
        "family": "world model benchmark",
        "pdf": "",
        "repo": "WorldArena",
        "sources": ["https://github.com/tsinghua-fib-lab/WorldArena", "https://world-arena.ai/"],
        "sub": {"problem_match": 2.0, "sim_transfer": 2.0, "code": 3.5, "consistency": 2.5, "cost": 3.5},
        "input": "world model generated videos and evaluation tasks。",
        "output": "benchmark scores / human and automated evaluation protocols。",
        "pipeline": ["用于比较 embodied world model 的感知和 functional utility。"],
        "objectives": "benchmark not method。",
        "assumptions": "对本项目可提供 evaluation inspiration，不提供补全模块。",
        "failure": "不能直接修复 Go2 3DGS。",
        "transfer": "evaluation-only。",
        "recommendation": "P2。用来构造 world model 对照实验，而非主线。",
    },
    {
        "id": "hunyuan_voyager",
        "slug": "hunyuan_world_voyager",
        "title": "HunyuanWorld-Voyager",
        "type": "repo",
        "priority": "P2",
        "review_depth": "skim",
        "family": "explorable video/world generation",
        "pdf": "",
        "repo": "HunyuanWorld-Voyager",
        "sources": ["https://github.com/Tencent-Hunyuan/HunyuanWorld-Voyager"],
        "sub": {"problem_match": 3.0, "sim_transfer": 2.0, "code": 2.5, "consistency": 3.0, "cost": 2.0},
        "input": "Hunyuan world/video generation inputs。",
        "output": "explorable/generated world videos or assets depending release state。",
        "pipeline": ["与 HY-World 生态相邻，本轮只作补充记录。"],
        "objectives": "world generation。",
        "assumptions": "仓库 clone 后内容很少，资料不足以做 deep report。",
        "failure": "不可作为当前工程依赖。",
        "transfer": "unverified。",
        "recommendation": "P2。等待资料完善。",
    },
    {
        "id": "mvgenmaster",
        "slug": "mvgenmaster",
        "title": "MvGenMaster: Scaling Multi-View Consistent Image Generation",
        "type": "repo",
        "priority": "P2",
        "review_depth": "skim",
        "family": "multi-view image generation",
        "pdf": "",
        "repo": "mvgenmaster",
        "sources": ["https://github.com/ewrfcas/mvgenmaster"],
        "sub": {"problem_match": 3.0, "sim_transfer": 2.2, "code": 3.5, "consistency": 3.4, "cost": 2.5},
        "input": "multi-view generation conditions。",
        "output": "multi-view consistent images。",
        "pipeline": ["multi-view consistent image generation 方向的补充项目。"],
        "objectives": "generation consistency objective。",
        "assumptions": "不是专门 real2sim/Isaac pipeline。",
        "failure": "3D geometry/collision 输出弱。",
        "transfer": "visual-only。",
        "recommendation": "P2。作为 CAT3D/SEVA 的替补线。",
    },
]


def write_report(e):
    meta = repo_meta(e.get("repo"))
    e["commit"] = meta["commit"]
    e["license_file"] = meta["license_file"]
    e["score"] = score(e["sub"])
    depth_name = {"deep": "deep_digest", "standard": "standard_digest", "skim": "skim_digest"}[e["review_depth"]]
    md_path = NOTES / f"{e['slug']}_{depth_name}.md"
    html_path = NOTES / f"{e['slug']}.html"
    src_lines = "\n".join(f"- {s}" for s in e["sources"])
    pipe_lines = "\n".join(f"- {p}" for p in e["pipeline"])
    md = f"""# {e['title']}

优先级：**{e['priority']}** | 阅读深度：**{e['review_depth']}** | 类别：**{e['family']}** | 综合分：**{e['score']}/5**

## 资料状态
- 类型：{e['type']}
- 本地 PDF：{('ref/' + e['pdf']) if e.get('pdf') else '无 / 技术项目'}
- 本地 repo：{('repos/' + e['repo']) if e.get('repo') else '无'}
- commit：{e.get('commit') or 'N/A'}
- license 文件：{e.get('license_file') or '未在 repo 根目录确认'}
- Sources:
{src_lines}

## 对 directional view coverage gap 的定位
{e['recommendation']}

## Inputs / Outputs
- Inputs：{e['input']}
- Outputs：{e['output']}

## Method Pipeline
{pipe_lines}

## Objectives / Losses
{e['objectives']}

## Assumptions
{e['assumptions']}

## Failure Modes
{e['failure']}

## Isaac Sim / 平台迁移判断
{e['transfer']}

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | {e['family']} |
| camera-pose conditioning | {'强' if e['sub']['problem_match'] >= 4.4 else '中/弱'} |
| large-angle support | {'强' if e['sub']['problem_match'] >= 4.4 else '需验证'} |
| 3D consistency | {e['sub']['consistency']}/5 |
| Isaac Sim path | {e['transfer']} |
| code/weights | {e['sub']['code']}/5 |
| priority score | {e['score']}/5 |
"""
    md_path.write_text(md, encoding="utf-8")

    def ul(items):
        return "<ul>" + "".join(f"<li>{html.escape(x)}</li>" for x in items) + "</ul>"

    source_html = ul(e["sources"])
    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{html.escape(e['title'])}</title>
<style>
body {{ font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; line-height:1.65; margin:0; color:#202124; background:#f7f7f5; }}
main {{ max-width: 980px; margin: 0 auto; padding: 32px 24px 56px; background:#fff; }}
h1 {{ font-size: 30px; margin:0 0 8px; }}
h2 {{ margin-top: 30px; border-top:1px solid #ddd; padding-top:18px; }}
.meta {{ color:#5f6368; }}
.badge {{ display:inline-block; padding:2px 8px; border:1px solid #ccc; border-radius:6px; margin-right:6px; background:#fafafa; }}
table {{ border-collapse: collapse; width:100%; margin: 14px 0; }}
td, th {{ border:1px solid #ddd; padding:8px; vertical-align:top; }}
th {{ background:#f1f3f4; }}
code {{ background:#f1f3f4; padding:2px 4px; border-radius:4px; }}
</style>
</head>
<body><main>
<h1>{html.escape(e['title'])}</h1>
<p class="meta"><span class="badge">{e['priority']}</span><span class="badge">{e['review_depth']}</span><span class="badge">score {e['score']}/5</span><span class="badge">{html.escape(e['family'])}</span></p>
<h2>资料状态</h2>
<table>
<tr><th>类型</th><td>{html.escape(e['type'])}</td></tr>
<tr><th>本地 PDF</th><td>{html.escape(('ref/' + e['pdf']) if e.get('pdf') else '无 / 技术项目')}</td></tr>
<tr><th>本地 repo</th><td>{html.escape(('repos/' + e['repo']) if e.get('repo') else '无')}</td></tr>
<tr><th>commit</th><td>{html.escape(e.get('commit') or 'N/A')}</td></tr>
<tr><th>license 文件</th><td>{html.escape(e.get('license_file') or '未在 repo 根目录确认')}</td></tr>
</table>
<h2>Sources</h2>{source_html}
<h2>对 directional view coverage gap 的定位</h2><p>{html.escape(e['recommendation'])}</p>
<h2>Inputs / Outputs</h2>
<ul><li><strong>Inputs:</strong> {html.escape(e['input'])}</li><li><strong>Outputs:</strong> {html.escape(e['output'])}</li></ul>
<h2>Method Pipeline</h2>{ul(e['pipeline'])}
<h2>Objectives / Losses</h2><p>{html.escape(e['objectives'])}</p>
<h2>Assumptions</h2><p>{html.escape(e['assumptions'])}</p>
<h2>Failure Modes</h2><p>{html.escape(e['failure'])}</p>
<h2>Isaac Sim / 平台迁移判断</h2><p>{html.escape(e['transfer'])}</p>
<h2>Transfer Matrix 摘要</h2>
<table>
<tr><th>method family</th><td>{html.escape(e['family'])}</td></tr>
<tr><th>camera-pose conditioning</th><td>{'强' if e['sub']['problem_match'] >= 4.4 else '中/弱'}</td></tr>
<tr><th>large-angle support</th><td>{'强' if e['sub']['problem_match'] >= 4.4 else '需验证'}</td></tr>
<tr><th>3D consistency</th><td>{e['sub']['consistency']}/5</td></tr>
<tr><th>Isaac Sim path</th><td>{html.escape(e['transfer'])}</td></tr>
<tr><th>code/weights</th><td>{e['sub']['code']}/5</td></tr>
<tr><th>priority score</th><td>{e['score']}/5</td></tr>
</table>
</main></body></html>
"""
    html_path.write_text(html_doc, encoding="utf-8")
    e["note_paths"] = [str(md_path.relative_to(ROOT)), str(html_path.relative_to(ROOT))]


def write_matrix(entries):
    rows = sorted(entries, key=lambda x: x["score"], reverse=True)
    headers = [
        "method family",
        "input requirement",
        "output asset",
        "camera-pose conditioning",
        "large-angle support",
        "3D consistency",
        "Isaac Sim path",
        "code/weights",
        "risk",
        "priority score",
        "recommended role",
    ]
    md = "# Directional View Completion Transfer Matrix\n\n"
    md += "| 项目 | " + " | ".join(headers) + " |\n"
    md += "|---|" + "|".join(["---"] * len(headers)) + "|\n"
    for e in rows:
        cam = "强" if e["sub"]["problem_match"] >= 4.4 else ("中" if e["sub"]["problem_match"] >= 3.5 else "弱")
        large = "强" if e["sub"]["problem_match"] >= 4.4 else ("需实测" if e["sub"]["problem_match"] >= 3.2 else "弱")
        risk = e["failure"].replace("|", "/")
        role = e["recommendation"].replace("|", "/")
        vals = [
            e["family"],
            e["input"],
            e["output"],
            cam,
            large,
            f"{e['sub']['consistency']}/5",
            e["transfer"],
            f"{e['sub']['code']}/5",
            risk,
            f"{e['score']}/5",
            role,
        ]
        note_link = Path(e["note_paths"][1]).name.replace(" ", "%20")
        md += f"| [{e['title']}]({note_link}) | " + " | ".join(v.replace("\n", " ") for v in vals) + " |\n"
    (NOTES / "transfer_matrix_directional_view_completion.md").write_text(md, encoding="utf-8")

    table = "<table><thead><tr><th>项目</th>" + "".join(f"<th>{html.escape(h)}</th>" for h in headers) + "</tr></thead><tbody>"
    for e in rows:
        cam = "强" if e["sub"]["problem_match"] >= 4.4 else ("中" if e["sub"]["problem_match"] >= 3.5 else "弱")
        large = "强" if e["sub"]["problem_match"] >= 4.4 else ("需实测" if e["sub"]["problem_match"] >= 3.2 else "弱")
        vals = [
            e["family"], e["input"], e["output"], cam, large, f"{e['sub']['consistency']}/5",
            e["transfer"], f"{e['sub']['code']}/5", e["failure"], f"{e['score']}/5", e["recommendation"],
        ]
        table += f"<tr><td><a href='{html.escape(Path(e['note_paths'][1]).name)}'>{html.escape(e['title'])}</a></td>" + "".join(f"<td>{html.escape(v)}</td>" for v in vals) + "</tr>"
    table += "</tbody></table>"
    html_doc = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>Transfer Matrix</title>
<style>body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin:0;background:#f7f7f5;color:#202124}}main{{padding:28px;max-width:1500px;margin:auto;background:#fff}}table{{border-collapse:collapse;width:100%;font-size:13px}}td,th{{border:1px solid #ddd;padding:8px;vertical-align:top}}th{{background:#f1f3f4;position:sticky;top:0}}a{{color:#0b57d0}}</style></head><body><main>
<h1>Directional View Completion Transfer Matrix</h1>
<p>排序依据：problem match 30%、Isaac/sim transfer 25%、code/weights 20%、3D consistency 15%、engineering cost 10%。</p>
{table}
</main></body></html>"""
    (NOTES / "transfer_matrix_directional_view_completion.html").write_text(html_doc, encoding="utf-8")


def write_final(entries):
    rows = sorted(entries, key=lambda x: x["score"], reverse=True)
    top = rows[:12]
    top_md = "\n".join(f"{i+1}. **{e['title']}** ({e['score']}/5, {e['priority']}): {e['recommendation']}" for i, e in enumerate(top))
    all_md = "\n".join(f"- {e['title']}: {e['score']}/5, {e['family']}" for e in rows)
    completion_order = [
        "GEN3C / SEVA：最先验证。二者都支持 target camera 或 camera trajectory，是直接攻击反向 yaw 黑洞的工具。",
        "MVGD / GLD：若代码和算力可用，优先补 depth，因为 pseudo depth 能参与 mesh/TSDF/Isaac collision proxy。",
        "CAT3D：作为 multi-view diffusion 范式参考，不作为第一工程依赖，除非找到可复现实现。",
        "GenRC / SceneCompleter / Seen2Scene：用于低覆盖区域的 room-scale geometry hypotheses，不替代真实观测。",
        "HY-World 2.0：仅在需要 semantic/layout prior 或局部 3D asset prior 时使用，必须受原始 poses/depth/point cloud 约束。",
    ]
    integration_order = [
        "OpenReal2Sim：IsaacLab/Isaac Sim 路径最清晰，已有 GLB、scene.json、USD conversion 和 IsaacLab demo。",
        "SuGaR / 2DGS / PGSR：把修复后的 GS 变成 surface/mesh，是 Isaac collision proxy 的关键桥。",
        "omni-3dgs-extension：如果短期只需要 Isaac 内 RGB camera observation，可直接验证 3DGS visual layer。",
        "GS-Playground / GaussGym：吸收 batch 3DGS rendering + physics separation 的系统设计，但不直接替代 Isaac Sim 后端。",
    ]
    completion_md = "\n".join(f"{i+1}. {x}" for i, x in enumerate(completion_order))
    integration_md = "\n".join(f"{i+1}. {x}" for i, x in enumerate(integration_order))
    md = f"""# Final Report: Directional View Completion for Real2Sim / Isaac Sim

## 0. 研究问题
当前 Go2 20s 诊断场景的问题不是 3DGS 整体失效，也不是相机中心离训练轨迹太远，而是 **directional view coverage gap**：训练相机主要看向一个方向，仿真相机在相近位置看向反向或大偏角 yaw 时缺少观测支撑，导致 black holes、floaters、低亮度和结构丢失。

因此，第一主线不是无约束 open world generation，而是：**真实场景锚定 + camera/pose-conditioned large-angle novel-view completion + 3D/geometry consistency + Isaac-transferable assets**。

## 1. 综合排序 Top 12
{top_md}

这张综合排序把 Isaac/sim transfer 也计入权重，因此 OpenReal2Sim、GS-Playground、SuGaR 等工程桥接项排名很高。若只问“谁最直接解决反向/大偏角 novel view”，应采用下面的 solution-module ranking。

## 2. Solution-module ranking：先解决黑洞，再进 Isaac
{completion_md}

## 3. Integration ranking：补全结果如何变成 Isaac Sim 资产
{integration_md}

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
{all_md}

## 9. 关键结论
开放世界模型仍然有价值，但它在本问题中应作为 **prior** 或 **fallback generator**，不是第一优先级。第一优先级是可以被真实 Go2 数据和 camera pose 锚定的方法：SEVA/GEN3C/MVGD 负责补视角，PGSR/SuGaR/2DGS 负责表面化，OpenReal2Sim 负责 Isaac Sim 资产路径。
"""
    (NOTES / "final_directional_view_completion_report.md").write_text(md, encoding="utf-8")
    html_doc = "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><title>Final Directional View Completion Report</title><style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:0;background:#f7f7f5;color:#202124}main{max-width:1050px;margin:auto;background:#fff;padding:32px 28px 60px;line-height:1.7}h1{font-size:32px}h2{margin-top:30px;border-top:1px solid #ddd;padding-top:18px}h3{margin-top:22px}li{margin:6px 0}code{background:#f1f3f4;padding:2px 4px;border-radius:4px}</style></head><body><main>"
    # Small markdown-ish renderer for the generated report.
    for line in md.splitlines():
        if line.startswith("# "):
            html_doc += f"<h1>{html.escape(line[2:])}</h1>"
        elif line.startswith("## "):
            html_doc += f"<h2>{html.escape(line[3:])}</h2>"
        elif line.startswith("### "):
            html_doc += f"<h3>{html.escape(line[4:])}</h3>"
        elif line.startswith("- "):
            html_doc += f"<p>• {html.escape(line[2:])}</p>"
        elif line and line[0].isdigit() and ". " in line[:4]:
            html_doc += f"<p>{html.escape(line)}</p>"
        elif line.strip():
            html_doc += f"<p>{html.escape(line)}</p>"
    html_doc += "</main></body></html>"
    (NOTES / "final_directional_view_completion_report.html").write_text(html_doc, encoding="utf-8")


def write_index(entries):
    rows = sorted(entries, key=lambda x: (x["priority"], -x["score"]))
    md = "# Directional View Completion Research Index\n\n"
    md += "本索引列出本轮生成的所有单项报告、资料状态和调研深度。\n\n"
    md += "| Priority | Depth | Score | Title | Local notes | Sources |\n|---|---:|---:|---|---|---|\n"
    for e in rows:
        notes = ", ".join(f"[{Path(p).name}]({Path(p).name})" for p in e["note_paths"])
        sources = "<br>".join(e["sources"])
        md += f"| {e['priority']} | {e['review_depth']} | {e['score']} | {e['title']} | {notes} | {sources} |\n"
    (NOTES / "directional_view_completion_research_index.md").write_text(md, encoding="utf-8")

    table = "<table><tr><th>Priority</th><th>Depth</th><th>Score</th><th>Title</th><th>Notes</th><th>Sources</th></tr>"
    for e in rows:
        notes = " ".join(f"<a href='{html.escape(Path(p).name)}'>{html.escape(Path(p).name)}</a>" for p in e["note_paths"])
        sources = "<br>".join(f"<a href='{html.escape(s)}'>{html.escape(s)}</a>" for s in e["sources"])
        table += f"<tr><td>{e['priority']}</td><td>{e['review_depth']}</td><td>{e['score']}</td><td>{html.escape(e['title'])}</td><td>{notes}</td><td>{sources}</td></tr>"
    table += "</table>"
    (NOTES / "directional_view_completion_research_index.html").write_text(
        "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><title>Research Index</title><style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:0;background:#f7f7f5}main{max-width:1300px;margin:auto;background:#fff;padding:28px}table{border-collapse:collapse;width:100%;font-size:13px}td,th{border:1px solid #ddd;padding:8px;vertical-align:top}th{background:#f1f3f4}</style></head><body><main><h1>Directional View Completion Research Index</h1>"
        + table
        + "</main></body></html>",
        encoding="utf-8",
    )


def write_registry(entries):
    with REGISTRY.open("w", encoding="utf-8") as f:
        for e in entries:
            rec = {
                "id": e["id"],
                "title": e["title"],
                "type": e["type"],
                "priority": e["priority"],
                "sources": e["sources"],
                "local_pdf": str((REF / e["pdf"]).relative_to(ROOT)) if e.get("pdf") else "",
                "local_repo": str((REPOS / e["repo"]).relative_to(ROOT)) if e.get("repo") else "",
                "commit": e.get("commit", ""),
                "license": e.get("license_file", ""),
                "status": "downloaded" if e.get("pdf") or e.get("repo") else "metadata-only",
                "note_paths": e.get("note_paths", []),
                "review_depth": e["review_depth"],
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def write_bib(entries):
    chunks = []
    for e in entries:
        if "arxiv.org/abs/" in " ".join(e["sources"]):
            arxiv = ""
            for s in e["sources"]:
                if "arxiv.org/abs/" in s:
                    arxiv = s.rsplit("/", 1)[-1]
            chunks.append(
                "@misc{%s,\n  title = {%s},\n  howpublished = {arXiv:%s},\n  note = {Verified source registry entry; see notes/%s.html}\n}\n"
                % (e["id"], e["title"], arxiv, e["slug"])
            )
        else:
            chunks.append(
                "@misc{%s,\n  title = {%s},\n  howpublished = {%s},\n  note = {Project/source registry entry; see notes/%s.html}\n}\n"
                % (e["id"], e["title"], e["sources"][0], e["slug"])
            )
    BIB.write_text("\n".join(chunks), encoding="utf-8")


def main():
    NOTES.mkdir(exist_ok=True)
    (NOTES / "assets").mkdir(exist_ok=True)
    for e in ENTRIES:
        write_report(e)
    write_matrix(ENTRIES)
    write_final(ENTRIES)
    write_index(ENTRIES)
    write_registry(ENTRIES)
    write_bib(ENTRIES)
    print(f"wrote {len(ENTRIES)} reports")


if __name__ == "__main__":
    main()
