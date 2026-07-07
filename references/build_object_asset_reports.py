from __future__ import annotations

import html
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"
REF = ROOT / "ref"
REPOS = ROOT / "repos"
REFERENCES = ROOT / "references"
REGISTRY = REFERENCES / "source_registry.jsonl"
BIB = REFERENCES / "bibliography.bib"
OBJECT_BIB = REFERENCES / "bibliography_object_asset.bib"


WEIGHTS = {
    "object_match": 0.25,
    "isaac_transfer": 0.25,
    "geometry_collision": 0.20,
    "code_repro": 0.15,
    "view_completion": 0.10,
    "engineering_readiness": 0.05,
}


def weighted_score(sub: dict[str, float]) -> float:
    return round(sum(sub[k] * w for k, w in WEIGHTS.items()), 2)


def repo_meta(repo: str | None) -> dict[str, str]:
    if not repo:
        return {"commit": "", "license_file": "", "status": "no-repo"}
    path = REPOS / repo
    if not path.exists():
        return {"commit": "", "license_file": "", "status": "missing"}
    if not (path / ".git").exists():
        return {"commit": "", "license_file": "", "status": "partial-or-non-git"}
    try:
        commit = subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "--short", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        commit = ""
    license_file = ""
    try:
        for p in path.iterdir():
            if p.is_file() and p.name.lower().startswith(("license", "licence", "copying")):
                license_file = p.name
                break
    except Exception:
        pass
    return {"commit": commit, "license_file": license_file, "status": "cloned" if commit else "partial"}


def md_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join(["---"] * len(rows[0])) + " |"
    body = ["| " + " | ".join(str(c).replace("\n", "<br>") for c in row) + " |" for row in rows[1:]]
    return "\n".join([header, sep, *body])


def simple_md_to_html(md: str, title: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    in_ul = False
    in_pre = False
    for line in lines:
        if line.startswith("```"):
            if in_pre:
                out.append("</code></pre>")
                in_pre = False
            else:
                out.append("<pre><code>")
                in_pre = True
            continue
        if in_pre:
            out.append(html.escape(line))
            continue
        if line.startswith("# "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{html.escape(line[2:])}</li>")
        elif line.startswith("| "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<p class=\"table-line\">{html.escape(line)}</p>")
        elif not line.strip():
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append("")
        else:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<p>{html.escape(line)}</p>")
    if in_ul:
        out.append("</ul>")
    css = """
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.65;max-width:1120px;margin:32px auto;padding:0 24px;color:#17202a;background:#fbfbf8}
h1{font-size:30px;margin-bottom:8px}h2{font-size:22px;margin-top:30px;border-bottom:1px solid #ddd;padding-bottom:4px}h3{font-size:18px;margin-top:22px}
p,li{font-size:15px}.meta{color:#555}.card{border:1px solid #ddd;border-radius:8px;padding:14px 16px;background:#fff;margin:14px 0}
.table-line{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;white-space:pre-wrap;background:#fff;padding:2px 6px;margin:0;border-left:1px solid #ddd;border-right:1px solid #ddd}
pre{background:#111827;color:#f9fafb;padding:14px;border-radius:8px;overflow:auto}
"""
    return f"<!doctype html><html><head><meta charset=\"utf-8\"><title>{html.escape(title)}</title><style>{css}</style></head><body>{chr(10).join(out)}</body></html>"


ENTRIES: list[dict] = [
    {
        "id": "gsworld_object_asset",
        "slug": "gsworld_object_asset",
        "title": "GSWorld: Closed-Loop Photo-Realistic Simulation Suite for Robotic Manipulation",
        "authors_year": "Jiang et al., 2025",
        "type": "paper+repo+dataset",
        "priority": "P0",
        "review_depth": "deep",
        "family": "object-centric real2sim simulator / GSDF asset format",
        "pdf": "gsworld_2510_20813.pdf",
        "repo": "GSWorld",
        "sources": [
            "https://github.com/luccachiang/GSWorld",
            "https://arxiv.org/abs/2510.20813",
            "https://huggingface.co/datasets/GqJiang/gsworld",
        ],
        "sub": {"object_match": 5.0, "isaac_transfer": 4.1, "geometry_collision": 4.6, "code_repro": 4.4, "view_completion": 2.7, "engineering_readiness": 4.2},
        "inputs": "short multi-view captures, COLMAP poses, ArUco metric scale, robot URDF, cropped point cloud / object assets.",
        "outputs": "GSDF asset: Gaussian-on-Mesh visual layer + robot URDF + objects + collision meshes + material properties; ManiSkill/physics-engine tasks.",
        "pipeline": [
            "COLMAP + ArUco scaling trains metric 3DGS from real images.",
            "Sample semantic point cloud from robot URDF meshes, crop reconstructed point cloud, then manually align and refine with ICP.",
            "Transfer per-link semantic labels, segment robot/object Gaussians, and attach collision meshes/material properties.",
            "Use GSDF assets inside a physics simulator for policy training, evaluation, DAgger data collection, and sim-to-real replay.",
        ],
        "object_asset_role": "最贴合师兄原始任务的主线：它已经把 3DGS visual layer、mesh/collision、URDF、physics engine 和 manipulation policy loop 放在同一资产协议中。",
        "losses": "3DGS photometric reconstruction losses; ICP/alignment objectives; simulator side uses task reward / policy learning losses rather than a single reconstruction loss.",
        "assumptions": "需要短多视角采集、ArUco 或等价 metric scaling、机器人/物体可分割；细粒度 collision mesh 和 material 仍需人工或辅助工具校验。",
        "failure_modes": "遮挡严重或物体背面缺失会污染 Gaussian-on-Mesh；ICP 初值差会造成 robot/object/GS 坐标错位；GSDF 当前更偏 manipulation tabletop，迁移 Go2 大场景需重写 asset adapter。",
        "directional_gap": "不直接解决大偏角补视角，但它定义了补齐结果最终应进入的 object asset contract。",
        "isaac_path": "adapter needed: 可把 GSDF 思路迁移到 Isaac Sim 5.0 的 USD/URDF/mesh/collision；短期先复现其 real2sim asset construction，再写 Isaac exporter。",
        "recommended_role": "第一复现对象和系统设计锚点；把本项目目标重写为 GS visual layer + geometry/collision layer 的 asset contract。",
        "next_experiment": "选择一个门/椅子/桌子小物体，按 GSWorld real2sim 流程完成 metric 3DGS、object mask、mesh/collision、URDF/USD 对齐，作为所有补全模块的验收接口。",
        "bib": "@article{jiang2025gsworld,title={GSWorld: Closed-Loop Photo-Realistic Simulation Suite for Robotic Manipulation},author={Jiang, Guangqi and Chang, Haoran and Qiu, Ri-Zhao and Liang, Yutong and Ji, Mazeyu and Zhu, Jiyue and Dong, Zhao and Zou, Xueyan and Wang, Xiaolong},journal={arXiv preprint arXiv:2510.20813},year={2025}}",
    },
    {
        "id": "sugar_object_asset",
        "slug": "sugar_object_asset",
        "title": "SuGaR: Surface-Aligned Gaussian Splatting for Efficient 3D Mesh Reconstruction",
        "authors_year": "Guédon and Lepetit, 2023",
        "type": "paper+repo",
        "priority": "P0",
        "review_depth": "deep",
        "family": "3DGS-to-mesh / surface extraction",
        "pdf": "sugar_2311_12775.pdf",
        "repo": "SuGaR",
        "sources": ["https://github.com/Anttwo/SuGaR", "https://arxiv.org/abs/2311.12775"],
        "sub": {"object_match": 4.4, "isaac_transfer": 4.3, "geometry_collision": 4.8, "code_repro": 4.4, "view_completion": 1.8, "engineering_readiness": 4.2},
        "inputs": "COLMAP/posed images or pretrained vanilla 3DGS checkpoint.",
        "outputs": "surface-aligned Gaussians, mesh, textured mesh, hybrid mesh+Gaussians.",
        "pipeline": [
            "Start from existing 3DGS or train 3DGS from posed images.",
            "Regularize Gaussians to align with a surface estimate.",
            "Extract mesh and optionally bind Gaussians to mesh for high-quality rendering.",
            "Export mesh as downstream geometry/collision candidate.",
        ],
        "object_asset_role": "师兄明确要求复现的核心几何层工具；适合把已补视角/已分割的物体 3DGS 转成 Isaac 可处理 mesh。",
        "losses": "photometric rendering loss plus surface alignment/regularization terms; final mesh quality depends on input coverage.",
        "assumptions": "输入 3DGS 已经没有严重黑洞；物体边界/薄结构需要足够视角或额外 mask/depth。",
        "failure_modes": "对未观测背面不会凭空补全；如果 3DGS 有 floaters/holes，mesh 会固化这些错误；collision mesh 还需简化/凸分解。",
        "directional_gap": "不是补视角方法，但依赖 GaussianObject/SEVA/GEN3C/Hunyuan3D 等先补缺失面。",
        "isaac_path": "direct-ish: mesh/OBJ/PLY 可经 Blender/Omniverse 转 USD，collision 需另做 simplification/VHACD/convex decomposition。",
        "recommended_role": "P0 几何层后端；与 GSWorld/OpenReal2Sim/Isaac importer 组成 asset export baseline。",
        "next_experiment": "对同一指定物体分别用原始 views 和 pseudo/backside-completed views 训练 3DGS，再跑 SuGaR mesh extraction，比较 holes、mesh watertightness、free-space violation。",
        "bib": "@article{guedon2023sugar,title={SuGaR: Surface-Aligned Gaussian Splatting for Efficient 3D Mesh Reconstruction},author={Guédon, Antoine and Lepetit, Vincent},journal={arXiv preprint arXiv:2311.12775},year={2023}}",
    },
    {
        "id": "objectgs",
        "slug": "objectgs",
        "title": "ObjectGS: Object-aware Scene Reconstruction and Scene Understanding via Gaussian Splatting",
        "authors_year": "Zhu et al., 2025",
        "type": "paper+repo",
        "priority": "P0",
        "review_depth": "deep",
        "family": "object-aware Gaussian reconstruction / instance extraction",
        "pdf": "objectgs_2507_15454.pdf",
        "repo": "ObjectGS",
        "sources": ["https://github.com/RuijieZhu94/ObjectGS", "https://ruijiezhu94.github.io/ObjectGS_page/", "https://arxiv.org/abs/2507.15454"],
        "sub": {"object_match": 4.8, "isaac_transfer": 3.7, "geometry_collision": 4.0, "code_repro": 4.1, "view_completion": 2.0, "engineering_readiness": 3.8},
        "inputs": "posed multi-view RGB, SAM/2D segmentation labels, object IDs; supports 3DGS and 2DGS variants.",
        "outputs": "object-aware neural Gaussians, 2D/3D semantic rendering, single-object rendering, scene/object mesh export.",
        "pipeline": [
            "Use 2D segmentation pipeline to assign object IDs and lift them to 3D by voting.",
            "Initialize anchors and generate object-aware neural Gaussians per object.",
            "Attach deterministic one-hot object ID semantics and use classification constraints during reconstruction.",
            "Render single objects or export object meshes via query_label_id.",
        ],
        "object_asset_role": "解决“指定物体”如何从整场景 3DGS 中分离出来，是 object-level asset pipeline 的前端。",
        "losses": "photometric reconstruction loss plus object-ID classification/semantic constraints; anchor grow/prune controls object geometry coverage.",
        "assumptions": "2D masks跨视角一致性足够；目标物体在多视角中有可见区域；dataset preprocessing 成本不低。",
        "failure_modes": "SAM/DEVA mask 错误会污染 object IDs；离散 ID 会遇到细小接触物体边界粘连；mesh export 质量仍受 3DGS surface quality 限制。",
        "directional_gap": "本身不补背面，但能把需要补齐的 object subset 精确抽出来再送 GaussianObject/Hunyuan3D/SuGaR。",
        "isaac_path": "adapter needed: object mesh export 后可进入 USD/collision，object Gaussians 可作 visual layer。",
        "recommended_role": "P0 object selection/extraction 工具；优先用于门、椅子、桌子等指定物体分离。",
        "next_experiment": "在现有 Go2 场景中标注/检测一个椅子或门，用 ObjectGS 输出 query object mesh 与 object-only Gaussians，再检查导入 Isaac 的可分离性。",
        "bib": "@inproceedings{zhu2025objectgs,title={ObjectGS: Object-aware Scene Reconstruction and Scene Understanding via Gaussian Splatting},author={Zhu, Ruijie and Yu, Mulin and Xu, Linning and Jiang, Lihan and Li, Yixuan and Zhang, Tianzhu and Pang, Jiangmiao and Dai, Bo},booktitle={ICCV},year={2025}}",
    },
    {
        "id": "gaussianobject",
        "slug": "gaussianobject",
        "title": "GaussianObject: High-Quality 3D Object Reconstruction from Four Views with Gaussian Splatting",
        "authors_year": "Yang et al., 2024",
        "type": "paper+repo+weights",
        "priority": "P0",
        "review_depth": "deep",
        "family": "sparse-view object 3DGS / diffusion repair",
        "pdf": "gaussianobject_2402_10259.pdf",
        "repo": "GaussianObject",
        "sources": ["https://github.com/chensjtu/GaussianObject", "https://gaussianobject.github.io/", "https://arxiv.org/abs/2402.10259"],
        "sub": {"object_match": 4.7, "isaac_transfer": 3.2, "geometry_collision": 3.5, "code_repro": 4.0, "view_completion": 4.6, "engineering_readiness": 3.5},
        "inputs": "as few as 4 object images, masks, optional camera parameters / COLMAP-free path, monocular depth.",
        "outputs": "object-level 3D Gaussian representation and repaired novel-view renderings; mesh requires downstream extraction.",
        "pipeline": [
            "Build a visual hull from masked sparse views and camera parameters.",
            "Initialize and optimize 3D Gaussians with reference photometric loss plus floater elimination.",
            "Train a Gaussian repair model with leave-one-out corrupted renderings and 3D Gaussian noise pairs.",
            "Use repaired images to refine missing/compressed object information.",
        ],
        "object_asset_role": "直接对应“单/少视角指定物体背面缺失”的补齐问题，是 object-level directional gap 的首选方法参考。",
        "losses": "L_gs photometric/ref reconstruction, L_tune for diffusion repair tuning, L_rep for repaired-view refinement.",
        "assumptions": "需要目标物体 mask；物体基本封闭且视觉 hull 有意义；diffusion repair 可能生成 plausible 但非真实背面。",
        "failure_modes": "薄结构、透明/反光、强遮挡会破坏 visual hull；修复模型可能改变真实几何；不输出物理参数。",
        "directional_gap": "强相关：把 scene-level 反向 yaw 问题收束为 object backside / missing surface completion。",
        "isaac_path": "adapter needed: 先用 SuGaR/2DGS/PGSR 或 mesh extraction 转 geometry，再做 collision proxy。",
        "recommended_role": "P0 object backside completion baseline；和 ObjectGS 输出的 object crop/mask 串联。",
        "next_experiment": "从 Go2 场景截取指定物体 4-8 个视角，跑 GaussianObject，比较背面 novel view 与 SuGaR mesh 是否优于普通 3DGS。",
        "bib": "@article{yang2024gaussianobject,title={GaussianObject: High-Quality 3D Object Reconstruction from Four Views with Gaussian Splatting},author={Yang, Chen and Li, Sikuang and Fang, Jiemin and Liang, Ruofan and Xie, Lingxi and Zhang, Xiaopeng and Shen, Wei and Tian, Qi},journal={ACM Transactions on Graphics},year={2024}}",
    },
    {
        "id": "scalable_real2sim",
        "slug": "scalable_real2sim",
        "title": "Scalable Real2Sim: Physics-Aware Asset Generation via Robotic Pick-and-Place Setups",
        "authors_year": "Pfaff et al., 2025",
        "type": "paper+repo",
        "priority": "P0",
        "review_depth": "deep",
        "family": "object visual geometry + collision geometry + inertial parameter estimation",
        "pdf": "scalable_real2sim_2503_00370.pdf",
        "repo": "scalable-real2sim",
        "sources": ["https://github.com/nepfaff/scalable-real2sim", "https://scalable-real2sim.github.io/", "https://arxiv.org/abs/2503.00370"],
        "sub": {"object_match": 4.8, "isaac_transfer": 4.4, "geometry_collision": 5.0, "code_repro": 3.8, "view_completion": 1.5, "engineering_readiness": 3.4},
        "inputs": "robot pick-and-place data, multi-view object observations, gripper masks, RGB/depth/video, robot torque/kinematic state.",
        "outputs": "textured visual mesh, convex collision geometry, mass, center of mass, rotational inertia.",
        "pipeline": [
            "Collect object observations with robot manipulation setup.",
            "Use alpha-transparent training and gripper masks to reconstruct object-centric visual geometry.",
            "Simplify visual geometry into convex collision geometry by approximate convex decomposition.",
            "Design excitation trajectories and solve physically feasible inertial parameters from robot measurements.",
        ],
        "object_asset_role": "最完整覆盖“完整几何层 + collision + physical parameters”的论文，补足 3DGS/mesh 方法通常缺失的物理属性层。",
        "losses": "photometric/geometry reconstruction losses; inertial parameter estimation uses constrained optimization / augmented Lagrangian / physically feasible constraints.",
        "assumptions": "需要机器人可抓取/搬运物体并采集运动数据；数据采集链路比单纯视觉方法复杂。",
        "failure_modes": "gripper mask 错误会破坏重建；薄/软/透明物体参数估计困难；对大型固定物体如门/桌子需要改造采集 protocol。",
        "directional_gap": "不补视角，但可以把视觉补齐后的 mesh 变成 simulatable object description。",
        "isaac_path": "direct conceptually: visual mesh + convex collision + inertial parameters 正是 Isaac asset 所需。",
        "recommended_role": "P0 物理层参考；用于建立 asset validation schema 和后续 physical parameter estimation 实验。",
        "next_experiment": "先对小型可搬动物体复现 visual/collision/inertia schema；门/桌椅这类大物体用 VLM/PhysX 估计默认物理属性并人工校验。",
        "bib": "@article{pfaff2025scalable,title={Scalable Real2Sim: Physics-Aware Asset Generation via Robotic Pick-and-Place Setups},journal={arXiv preprint arXiv:2503.00370},year={2025}}",
    },
    {
        "id": "re3sim",
        "slug": "re3sim",
        "title": "Re3Sim: Generating High-Fidelity Simulation Data via 3D-Photorealistic Real-to-Sim for Robotic Manipulation",
        "authors_year": "Han et al., 2025",
        "type": "paper+repo+dataset",
        "priority": "P0",
        "review_depth": "deep",
        "family": "IsaacLab real2sim manipulation pipeline / hybrid 3DGS+mesh",
        "pdf": "re3sim_2502_08645.pdf",
        "repo": "Re3Sim",
        "sources": ["https://github.com/InternRobotics/Re3Sim", "https://arxiv.org/abs/2502.08645", "https://xshenhan.github.io/Re3Sim/"],
        "sub": {"object_match": 4.4, "isaac_transfer": 4.8, "geometry_collision": 4.5, "code_repro": 4.0, "view_completion": 2.4, "engineering_readiness": 3.8},
        "inputs": "custom scene photos, alignment image/ArUco, OpenMVS background/object mesh, 3DGS background, IsaacLab resources.",
        "outputs": "USD/textured meshes, collision meshes, hybrid visual rendering, simulated manipulation data in IsaacLab.",
        "pipeline": [
            "Recover scene/object meshes separately for collision and simulation.",
            "Train 3DGS for background photorealistic rendering.",
            "Composite foreground mesh rendering and 3DGS background by Z-buffer/depth.",
            "Align real-world, simulator, and 3DGS coordinates with markers and ICP, then generate policy data.",
        ],
        "object_asset_role": "直接展示 IsaacLab 中 visual layer 与 collision/mesh layer 如何协同，适合做 Isaac 端工程模板。",
        "losses": "MVS/3DGS reconstruction losses; policy data generation relies privileged simulation information and task rewards.",
        "assumptions": "背景与前景物体可分开重建；物体 rendering 面积较小时不必 3DGS 渲染；需要 IsaacLab 环境和资源。",
        "failure_modes": "它选择 mesh 渲染前景物体，可能不足以满足师兄要求的 object 3DGS visual layer；OpenMVS mesh 对细节/遮挡敏感。",
        "directional_gap": "支持 cross-view camera simulation，但补 unseen surfaces 仍依赖补采集或外部 completion。",
        "isaac_path": "direct: 以 IsaacLab 为默认仿真后端，是本项目迁移路线的重要参考。",
        "recommended_role": "P0 Isaac integration baseline；对比 GSWorld 的 GSDF asset design。",
        "next_experiment": "用 Re3Sim 自定义场景流程导入一个简单对象，替换其 mesh foreground 为 ObjectGS/GaussianObject visual layer，测试 IsaacLab 渲染/碰撞一致性。",
        "bib": "@article{han2025re3sim,title={Re3Sim: Generating High-Fidelity Simulation Data via 3D-Photorealistic Real-to-Sim for Robotic Manipulation},journal={arXiv preprint arXiv:2502.08645},year={2025}}",
    },
    {
        "id": "robosimgs",
        "slug": "robosimgs",
        "title": "RoboSimGS: High-Fidelity Simulated Data Generation for Real-World Zero-Shot Robotic Manipulation Learning with Gaussian Splatting",
        "authors_year": "Zhao et al., 2025",
        "type": "paper+repo",
        "priority": "P0",
        "review_depth": "deep",
        "family": "R2S2R hybrid 3DGS background + mesh interactive objects",
        "pdf": "robosimgs_2510_10637.pdf",
        "repo": "RoboSimGS",
        "sources": ["https://github.com/Maxwell-Zhao/RoboSimGS", "https://robosimgs.github.io/", "https://arxiv.org/abs/2510.10637"],
        "sub": {"object_match": 4.2, "isaac_transfer": 4.1, "geometry_collision": 4.3, "code_repro": 3.7, "view_completion": 2.1, "engineering_readiness": 3.5},
        "inputs": "multi-view real-world images, segmentation, MLLM physical/articulation inference, simulator alignment.",
        "outputs": "photorealistic 3DGS static background, interactive mesh objects, inferred density/stiffness/hinge/rail parameters, simulated data.",
        "pipeline": [
            "Reconstruct a hybrid scene where 3DGS captures static photorealism and mesh primitives represent interactive objects.",
            "Use MLLM to infer physical properties and kinematic structure from visual data.",
            "Align hybrid scene with simulator and apply holistic augmentation over objects, cameras, lighting, and trajectories.",
            "Train manipulation policy on generated data for zero-shot sim-to-real.",
        ],
        "object_asset_role": "强化“可交互物体不应只用 3DGS”的结论：背景可 3DGS，物体必须有 mesh/physics/articulation。",
        "losses": "standard reconstruction/policy losses; MLLM-inferred physical properties are not directly supervised by real measurements in the paper pipeline.",
        "assumptions": "MLLM 能合理推断物体物理/运动结构；真实场景对齐可靠；代码成熟度需进一步核验。",
        "failure_modes": "VLM/MLLM 物理参数可能 plausible but wrong；对门/抽屉等 articulated object 需要强校验。",
        "directional_gap": "不以补视角为核心，但 hybrid design 能接收 GaussianObject/Hunyuan3D 生成的物体 mesh。",
        "isaac_path": "adapter needed; paper目标是 physics engine interactive environments，和 Isaac 资产需求高度一致。",
        "recommended_role": "P0/P1 之间的设计参考；用于物体 articulation/physical property 默认值生成。",
        "next_experiment": "让 VLM/LLM 为门、椅子生成候选 joint/material/mass schema，再和 Isaac 交互测试中的碰撞/关节行为对照。",
        "bib": "@article{zhao2025robosimgs,title={High-Fidelity Simulated Data Generation for Real-World Zero-Shot Robotic Manipulation Learning with Gaussian Splatting},journal={arXiv preprint arXiv:2510.10637},year={2025}}",
    },
    {
        "id": "robogsim",
        "slug": "robogsim",
        "title": "RoboGSim: A Real2Sim2Real Robotic Gaussian Splatting Simulator",
        "authors_year": "Yang et al., 2024/2025",
        "type": "paper",
        "priority": "P0",
        "review_depth": "deep",
        "family": "R2S2R Gaussian reconstructor + digital twins builder",
        "pdf": "robogsim_2411_11839.pdf",
        "repo": None,
        "sources": ["https://arxiv.org/abs/2411.11839", "https://robogsim.github.io/"],
        "sub": {"object_match": 4.1, "isaac_transfer": 4.5, "geometry_collision": 4.2, "code_repro": 2.0, "view_completion": 2.9, "engineering_readiness": 3.0},
        "inputs": "multi-view RGB image sequences, robotic arm MDH parameters, real layout measurements.",
        "outputs": "3DGS scene/object reconstruction, mesh reconstruction, layout-aligned digital twin in Isaac Sim, novel view/object/trajectory simulated data.",
        "pipeline": [
            "Gaussian Reconstructor builds 3DGS scene/objects and segments robotic arm.",
            "Digital Twins Builder reconstructs scene/object meshes and aligns real/sim/GS coordinate spaces.",
            "Scene Composer synthesizes novel objects, scenes and views.",
            "Interactive Engine connects Isaac Sim collision/kinematics with GS renderer feedback to policy.",
        ],
        "object_asset_role": "与师兄任务描述几乎同构，但代码证据弱于 GSWorld/Re3Sim；适合作为系统 taxonomy 和指标参考。",
        "losses": "3DGS reconstruction losses, mesh reconstruction objectives, policy/evaluation metrics for sim2real consistency.",
        "assumptions": "需要 MDH/robot setup 和 layout measurements；digital twin builder 的实现可用性需进一步核验。",
        "failure_modes": "如果没有代码，短期复现成本高；layout alignment 误差会直接导致 grasp/collision mismatch。",
        "directional_gap": "可以生成 novel views，但不是针对 unseen backside completion 的方法。",
        "isaac_path": "direct conceptually: 明确使用 Isaac Sim 做 digital twin；工程落地需找完整代码。",
        "recommended_role": "P0 方法论参考，工程优先级排在 GSWorld/Re3Sim 后。",
        "next_experiment": "抽取其四模块接口，映射到本项目：Gaussian Reconstructor/Object Extractor/Isaac Asset Builder/Interactive Evaluator。",
        "bib": "@article{yang2024robogsim,title={RoboGSim: A Real2Sim2Real Robotic Gaussian Splatting Simulator},journal={arXiv preprint arXiv:2411.11839},year={2024}}",
    },
    {
        "id": "gaussian_grouping",
        "slug": "gaussian_grouping_object_asset",
        "title": "Gaussian Grouping: Segment and Edit Anything in 3D Scenes",
        "authors_year": "Ye et al., 2024",
        "type": "paper+repo",
        "priority": "P1",
        "review_depth": "standard",
        "family": "3DGS instance grouping / object editing",
        "pdf": "gaussian_grouping_2312_00732.pdf",
        "repo": "gaussian-grouping",
        "sources": ["https://github.com/lkeab/gaussian-grouping", "https://arxiv.org/abs/2312.00732"],
        "sub": {"object_match": 4.1, "isaac_transfer": 3.0, "geometry_collision": 3.1, "code_repro": 4.0, "view_completion": 2.2, "engineering_readiness": 3.9},
        "inputs": "posed RGB images, SAM masks, DEVA/consistent 2D masks.",
        "outputs": "grouped Gaussians with Identity Encoding; object removal/inpainting/editing.",
        "pipeline": ["Train 3DGS while augmenting each Gaussian with Identity Encoding.", "Supervise identity features through differentiable rendering using 2D masks.", "Apply 3D spatial consistency regularization.", "Use grouped Gaussians for object removal, inpainting, colorization or recomposition."],
        "object_asset_role": "可作为 ObjectGS 之前的稳健 baseline，用于快速 object grouping 和局部编辑。",
        "losses": "photometric reconstruction, identity classification, 3D spatial consistency regularization.",
        "assumptions": "需要稳定多视角 masks；编辑/inpainting 更偏视觉，不保证物理几何正确。",
        "failure_modes": "物体边界粘连、mask ID 不一致、编辑后几何不可碰撞。",
        "directional_gap": "object inpainting 可补视觉空洞，但不是 metric backside completion。",
        "isaac_path": "visual-only / adapter needed: grouped Gaussians可分离 object visual layer，mesh/collision 需 SuGaR/2DGS。",
        "recommended_role": "P1 object grouping baseline；若 ObjectGS 环境难装，可先用它分离物体。",
        "next_experiment": "在当前场景上训练 grouped 3DGS，测试目标门/桌椅是否能独立 render/remove/export。",
        "bib": "@inproceedings{ye2024gaussian,title={Gaussian Grouping: Segment and Edit Anything in 3D Scenes},author={Ye, Mingqiao and Danelljan, Martin and Yu, Fisher and Ke, Lei},booktitle={ECCV},year={2024}}",
    },
    {
        "id": "saga",
        "slug": "saga_object_asset",
        "title": "SAGA: Segment Any 3D Gaussians",
        "authors_year": "Cen et al., 2023/2024",
        "type": "paper+repo",
        "priority": "P1",
        "review_depth": "standard",
        "family": "promptable 3D Gaussian segmentation",
        "pdf": "saga_2312_00860.pdf",
        "repo": "SegAnyGAussians",
        "sources": ["https://github.com/Jumpat/SegAnyGAussians", "https://arxiv.org/abs/2312.00860"],
        "sub": {"object_match": 3.8, "isaac_transfer": 2.7, "geometry_collision": 2.8, "code_repro": 4.0, "view_completion": 1.7, "engineering_readiness": 4.0},
        "inputs": "trained 3DGS, SAM-generated masks/features, 2D visual prompts, optional physical scale prompt.",
        "outputs": "prompted 3D Gaussian object/part segmentation in milliseconds.",
        "pipeline": ["Attach scale-gated affinity features to Gaussians.", "Distill SAM masks into 3D features with scale-aware contrastive learning.", "At inference, map 2D prompts to 3D queries and segment corresponding Gaussians.", "Use scale gate to handle multi-granularity ambiguity."],
        "object_asset_role": "适合作为交互式选择指定物体/部件的工具，不负责重建/补全。",
        "losses": "scale-aware contrastive loss over rendered affinity features and SAM-derived mask correspondences.",
        "assumptions": "已有较好 3DGS；prompt/mask质量足够；scale选择影响结果。",
        "failure_modes": "多粒度部件边界不稳定；不输出 mesh/collision。",
        "directional_gap": "不补视角；用于指定补齐对象的 selection layer。",
        "isaac_path": "adapter needed: segmented Gaussians 经 mesh extraction 后才可进入 Isaac。",
        "recommended_role": "P1 interactive object/part picking utility。",
        "next_experiment": "用 2D prompt 选门把手/椅腿等细部，测试后续 mesh extraction 是否保持部件边界。",
        "bib": "@article{cen2023saga,title={Segment Any 3D Gaussians},author={Cen, Jiazhong and Fang, Jiemin and Yang, Chen and Xie, Lingxi and Zhang, Xiaopeng and Shen, Wei and Tian, Qi},journal={arXiv preprint arXiv:2312.00860},year={2023}}",
    },
    {
        "id": "hunyuan3d_21",
        "slug": "hunyuan3d_21_object_asset",
        "title": "Hunyuan3D 2.1: From Images to High-Fidelity 3D Assets with Production-Ready PBR Material",
        "authors_year": "Tencent Hunyuan3D Team, 2025",
        "type": "tech-report+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "image-to-3D mesh + PBR texture generation",
        "pdf": "hunyuan3d_2_1_2506_15442.pdf",
        "repo": "Hunyuan3D-2.1",
        "sources": ["https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1", "https://arxiv.org/abs/2506.15442", "https://huggingface.co/tencent/Hunyuan3D-2.1"],
        "sub": {"object_match": 4.0, "isaac_transfer": 3.6, "geometry_collision": 3.7, "code_repro": 4.5, "view_completion": 4.0, "engineering_readiness": 3.5},
        "inputs": "single object image; optional custom mesh for Hunyuan3D-Paint texture synthesis.",
        "outputs": "high-resolution polygon mesh, PBR material maps/albedo/metallic/roughness textures.",
        "pipeline": ["Use Hunyuan3D-DiT and ShapeVAE for image-conditioned shape generation.", "Decode latent tokens into polygon mesh.", "Use Hunyuan3D-Paint multi-view PBR diffusion to synthesize light-free, view-consistent material maps.", "Export textured mesh for downstream asset pipeline."],
        "object_asset_role": "师兄提到的 Hunyuan3D 路线：适合作为物体背面/完整形状/PBR texture prior，而不是无约束替代真实扫描。",
        "losses": "flow matching/diffusion objective for shape; multi-view PBR texture diffusion losses and alignment modules.",
        "assumptions": "输入需是清晰单物体图；生成 mesh 未必 metric-aligned，需用真实 point cloud / bbox / scale 对齐。",
        "failure_modes": "会 hallucinate 与真实物体不一致的背面、尺寸或拓扑；collision 需要简化且物理参数缺失。",
        "directional_gap": "强 visual backside prior；必须通过 real depth/point cloud reject test。",
        "isaac_path": "adapter needed but promising: mesh + PBR maps 可转 USD/GLB，collision 和 scale 需后处理。",
        "recommended_role": "P1/P0 边界的 generative object prior；用于低覆盖面的补全候选。",
        "next_experiment": "对同一物体输入正面 crop 生成 mesh/PBR，再按真实点云 scale/ICP 对齐，和 GaussianObject 的 3DGS 补面结果比较。",
        "bib": "@article{hunyuan3d2025hunyuan3d21,title={Hunyuan3D 2.1: From Images to High-Fidelity 3D Assets with Production-Ready PBR Material},author={{Tencent Hunyuan3D Team}},journal={arXiv preprint arXiv:2506.15442},year={2025}}",
    },
    {
        "id": "hunyuan3d_omni",
        "slug": "hunyuan3d_omni_object_asset",
        "title": "Hunyuan3D-Omni: A Unified Framework for Controllable Generation of 3D Assets",
        "authors_year": "Tencent Hunyuan3D Team, 2025",
        "type": "tech-report+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "controllable 3D asset generation with point/bbox/voxel/skeleton controls",
        "pdf": "hunyuan3d_omni_2509_21245.pdf",
        "repo": "Hunyuan3D-Omni",
        "sources": ["https://github.com/Tencent-Hunyuan/Hunyuan3D-Omni", "https://arxiv.org/abs/2509.21245", "https://huggingface.co/tencent/Hunyuan3D-Omni"],
        "sub": {"object_match": 4.2, "isaac_transfer": 3.7, "geometry_collision": 3.9, "code_repro": 4.3, "view_completion": 4.2, "engineering_readiness": 3.4},
        "inputs": "image plus optional point cloud, voxel, bounding box, or skeleton controls.",
        "outputs": "controlled 3D mesh assets from Hunyuan3D 2.1-style latent diffusion.",
        "pipeline": ["Encode additional controls through unified control encoder.", "Fuse image and structured controls in DiT/VAE generation path.", "Generate geometry constrained by point cloud/bbox/voxel/skeleton.", "Use output mesh as completion prior subject to registration and rejection."],
        "object_asset_role": "比普通 image-to-3D 更适合 real2sim，因为可以用 point cloud/bbox 约束生成几何和比例。",
        "losses": "flow matching / diffusion objective conditioned on image and structured controls.",
        "assumptions": "控制信号质量高；生成结果仍是 prior 而非测量；weights/VRAM 需求高。",
        "failure_modes": "point cloud sparse/noisy 时生成偏差；bbox 只约束比例不约束细节；拓扑可能变化。",
        "directional_gap": "适合作为物体未观测面的 controlled completion，优先级高于纯 open world model。",
        "isaac_path": "adapter needed: mesh output 可转 USD/GLB，collision/physics 另接 PhysX/ScalableReal2Sim。",
        "recommended_role": "P1+ generative completion prior；若 Hunyuan3D-2.1 不够受约束，升级到 Omni。",
        "next_experiment": "用真实 object point cloud + bbox 作为 control，生成完整 mesh，做 ICP/reprojection/free-space reject test。",
        "bib": "@article{hunyuan3d2025omni,title={Hunyuan3D-Omni: A Unified Framework for Controllable Generation of 3D Assets},author={{Tencent Hunyuan3D Team}},journal={arXiv preprint arXiv:2509.21245},year={2025}}",
    },
    {
        "id": "hunyuan3d_part",
        "slug": "hunyuan3d_part_object_asset",
        "title": "Hunyuan3D-Part: P3-SAM and X-Part for 3D Part Segmentation and Shape Decomposition",
        "authors_year": "Ma et al.; Yan et al., 2025",
        "type": "papers+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "part-level mesh segmentation and decomposition",
        "pdf": "p3_sam_2509_06784.pdf",
        "supplementary_pdfs": ["xpart_2509_08643.pdf"],
        "repo": "Hunyuan3D-Part",
        "sources": ["https://github.com/Tencent-Hunyuan/Hunyuan3D-Part", "https://arxiv.org/abs/2509.06784", "https://arxiv.org/abs/2509.08643"],
        "sub": {"object_match": 3.9, "isaac_transfer": 3.6, "geometry_collision": 4.0, "code_repro": 4.2, "view_completion": 2.7, "engineering_readiness": 3.5},
        "inputs": "holistic scanned or generated mesh; optional point prompts/bounding boxes.",
        "outputs": "part segmentation, part bounding boxes, semantic features, complete part-level decomposed meshes.",
        "pipeline": ["P3-SAM segments arbitrary 3D objects into parts using point-promptable segmentation.", "Automatically sample prompts and merge masks into part instances.", "X-Part uses bounding boxes and semantic features to generate coherent parts.", "Outputs can support part-level editing, retopology, UV, and articulation preparation."],
        "object_asset_role": "对门把手、椅腿、抽屉、铰链等可交互部件很有价值，补足 object-level 资产中的 part decomposition。",
        "losses": "segmentation losses for P3-SAM; diffusion/generation objectives for X-Part part decomposition.",
        "assumptions": "输入 mesh 已有较完整 holistic geometry；当前 release 是 light version，完整能力可能在 studio。",
        "failure_modes": "分件语义不一定等于物理关节；细部件可能过分/欠分；不估计 mass/friction/joints。",
        "directional_gap": "不补视角；用于完成 mesh 后的 part-level asset structuring。",
        "isaac_path": "adapter needed: part meshes 可映射 USD hierarchy / articulation links，仍需 joint/physics 参数。",
        "recommended_role": "P1 part decomposition tool；在 Hunyuan3D/GaussianObject 生成完整 mesh 后使用。",
        "next_experiment": "对生成/扫描的门或椅子 mesh 跑 P3-SAM/X-Part，检查能否分离门板/把手/椅腿并转换为 USD prim hierarchy。",
        "bib": "@article{ma2025p3sam,title={P3-SAM: Native 3D Part Segmentation},journal={arXiv preprint arXiv:2509.06784},year={2025}}\n@article{yan2025xpart,title={X-Part: high fidelity and structure coherent shape decomposition},journal={arXiv preprint arXiv:2509.08643},year={2025}}",
    },
    {
        "id": "physx_3d",
        "slug": "physx_3d_object_asset",
        "title": "PhysX-3D: Physical-Grounded 3D Asset Generation",
        "authors_year": "Cao et al., 2025",
        "type": "paper+repo+dataset",
        "priority": "P1",
        "review_depth": "standard",
        "family": "physical-grounded 3D asset generation / URDF annotation",
        "pdf": "physx_3d_2507_12465.pdf",
        "repo": "PhysX-3D",
        "sources": ["https://github.com/ziangcao0312/PhysX-3D", "https://arxiv.org/abs/2507.12465", "https://physx-3d.github.io/"],
        "sub": {"object_match": 3.8, "isaac_transfer": 4.0, "geometry_collision": 4.1, "code_repro": 4.0, "view_completion": 2.8, "engineering_readiness": 3.6},
        "inputs": "image/object asset plus PhysXNet annotations; part-level material, affordance, kinematics, function descriptions.",
        "outputs": "physical-property annotated assets, generated geometry with scale/material/affordance/kinematic predictions, URDF conversion script.",
        "pipeline": ["Build PhysXNet with five properties: absolute scale, material, affordance, kinematics, function.", "Use human-in-the-loop/VLM annotation for part-level physics properties.", "Train PhysXGen dual-branch model to inject physical knowledge into 3D structural space.", "Convert JSON annotations into URDF via provided script."],
        "object_asset_role": "补上 Isaac 可交互资产最容易缺失的物理属性 schema，尤其 part-level material/affordance/kinematics。",
        "losses": "VAE/diffusion training plus property prediction losses; evaluation includes scale distance, PSNR for property maps, kinematic distance.",
        "assumptions": "物理属性是从数据/语言先验推断，非真实测量；需对关键交互对象人工校验。",
        "failure_modes": "mass/material/friction 推断不可靠；URDF 转换不等于 Isaac articulation 全部可用；几何质量受底层 3D generator 限制。",
        "directional_gap": "不是视角补齐方法，而是补物理语义和互动层。",
        "isaac_path": "adapter needed but useful: URDF/part-level annotations 可转 Isaac USD/PhysX schema。",
        "recommended_role": "P1 physical property prior；和 Scalable Real2Sim 的实测参数形成对照。",
        "next_experiment": "把一个门/椅子 mesh 的 part hierarchy 输入 PhysX annotation/URDF schema，导入 Isaac 检查关节和碰撞。",
        "bib": "@article{cao2025physx,title={PhysX-3D: Physical-Grounded 3D Asset Generation},author={Cao, Ziang and Chen, Zhaoxi and Pan, Liang and Liu, Ziwei},journal={arXiv preprint arXiv:2507.12465},year={2025}}",
    },
    {
        "id": "physforge",
        "slug": "physforge_object_asset",
        "title": "PhysForge: Generating Physics-Grounded 3D Assets for Interactive Virtual World",
        "authors_year": "Yang et al., 2026",
        "type": "paper+repo",
        "priority": "P1",
        "review_depth": "standard",
        "family": "physics-grounded part-aware asset generation",
        "pdf": "physforge_2605_05163.pdf",
        "repo": "PhysForge",
        "sources": ["https://github.com/HKU-MMLab/PhysForge", "https://arxiv.org/abs/2605.05163", "https://hku-mmlab.github.io/PhysForge/"],
        "sub": {"object_match": 3.7, "isaac_transfer": 3.8, "geometry_collision": 4.1, "code_repro": 2.2, "view_completion": 3.0, "engineering_readiness": 2.8},
        "inputs": "single image plus VLM-generated Hierarchical Physical Blueprint.",
        "outputs": "functionally plausible simulation-ready 3D assets with part materials, masses, joint types, affordances, kinematic parameters.",
        "pipeline": ["VLM planner acts as physical architect and generates hierarchical physical blueprint.", "Blueprint defines part layout, materials, mass, function, joint type, affordances.", "Diffusion stage uses KineVoxel Injection to jointly synthesize geometry and kinematic parameters.", "Assets are demonstrated in physics simulator/game virtual world."],
        "object_asset_role": "长期非常相关：直接面向可交互资产而非静态 mesh，但当前代码成熟度和真实场景锚定弱。",
        "losses": "diffusion generation objective conditioned on blueprint and KineVoxel; VLM planning is prompt/annotation-driven.",
        "assumptions": "VLM blueprint 正确；生成资产不需要和真实扫描严格一致。",
        "failure_modes": "容易生成 plausible interactive object 但不是当前真实物体；repo 目前较轻，短期复现风险高。",
        "directional_gap": "可补未观测部件/关节，但不是 real-scene anchored completion。",
        "isaac_path": "adapter needed: blueprint 可映射 USD/URDF/PhysX，但需实际 exporter。",
        "recommended_role": "P1 long-term prior；不作为短期主线。",
        "next_experiment": "抽取其 blueprint schema，用于给 Hunyuan3D/GaussianObject mesh 自动生成 Isaac 物理默认值。",
        "bib": "@article{yang2026physforge,title={PhysForge: Generating Physics-Grounded 3D Assets for Interactive Virtual World},journal={arXiv preprint arXiv:2605.05163},year={2026}}",
    },
    {
        "id": "openreal2sim_object_asset",
        "slug": "openreal2sim_object_asset",
        "title": "OpenReal2Sim: Toolbox for Real-to-Sim Reconstruction and Robotic Simulation",
        "authors_year": "OpenReal2Sim project, 2025/2026",
        "type": "repo",
        "priority": "P0",
        "review_depth": "deep",
        "family": "real2sim toolbox / GLB scene.json USD conversion",
        "pdf": "",
        "repo": "OpenReal2Sim",
        "sources": ["https://github.com/IntelLabs/OpenReal2Sim"],
        "sub": {"object_match": 4.1, "isaac_transfer": 4.7, "geometry_collision": 4.0, "code_repro": 4.4, "view_completion": 2.0, "engineering_readiness": 4.0},
        "inputs": "single image / monocular video / depth / camera preprocessing outputs.",
        "outputs": "background/object meshes, scene.json, GLB assets, IsaacLab USD conversion demos.",
        "pipeline": ["Preprocess input to metric depth/camera assets.", "Generate background/object mesh assets and scene config.", "Convert assets through GLB/scene.json path.", "Run IsaacLab demos and manipulation/planning examples."],
        "object_asset_role": "最接近本地 Isaac asset glue code 的工具箱；适合作为我们最终 exporter/interface 的代码参考。",
        "losses": "工程 pipeline 而非单篇论文；重建模块各自有对应 losses。",
        "assumptions": "需要适配我们的 Go2/RGB-D/3DGS 输入；默认 object extraction 可能偏单图/局部。",
        "failure_modes": "不解决高质量物体 3DGS visual layer；depth/inpainting 错误会污染 mesh。",
        "directional_gap": "把补齐模块放在 preprocess 和 reconstruction 之间。",
        "isaac_path": "direct: GLB/scene.json/USD conversion 是当前最实用的 Isaac path。",
        "recommended_role": "P0 Isaac exporter scaffold；和 GSWorld asset contract 结合。",
        "next_experiment": "用一个 ObjectGS/GaussianObject/SuGaR 输出物体，包装成 OpenReal2Sim-style scene.json + GLB/USD。",
        "bib": "",
    },
    {
        "id": "pgsr_object_asset",
        "slug": "pgsr_object_asset",
        "title": "PGSR: Planar-based Gaussian Splatting for Efficient and High-Fidelity Surface Reconstruction",
        "authors_year": "Chen et al., 2024",
        "type": "paper+repo",
        "priority": "P0",
        "review_depth": "deep",
        "family": "surface-aware 3DGS / mesh reconstruction",
        "pdf": "pgsr_2406_06521.pdf",
        "repo": "PGSR",
        "sources": ["https://github.com/zju3dv/PGSR", "https://arxiv.org/abs/2406.06521"],
        "sub": {"object_match": 3.8, "isaac_transfer": 4.1, "geometry_collision": 4.5, "code_repro": 4.0, "view_completion": 1.6, "engineering_readiness": 3.9},
        "inputs": "multi-view RGB / SfM poses; no pretrained depth/normal prior required.",
        "outputs": "planar-regularized 3DGS and mesh/surface reconstruction.",
        "pipeline": ["Train 3DGS with planar-based constraints.", "Use geometry regularization to improve surface fidelity.", "Extract mesh/surface for downstream use.", "Combine with pseudo/completed views to reduce holes."],
        "object_asset_role": "适合室内门、墙、桌面等 planar objects 的 geometry layer；对 collision proxy 很实用。",
        "losses": "photometric loss plus planar/surface regularization losses.",
        "assumptions": "目标表面具有平面/局部平滑结构；缺失背面仍需补齐。",
        "failure_modes": "错误 pseudo views 会被几何正则固化；非平面复杂物体优势下降。",
        "directional_gap": "后端修复，不直接补视角。",
        "isaac_path": "adapter needed: mesh output可转 USD/collision。",
        "recommended_role": "P0 几何后端，尤其针对门/桌面/墙体。",
        "next_experiment": "对门和桌面对象跑 PGSR，与 SuGaR/2DGS 输出 mesh 做 collision proxy 对比。",
        "bib": "@article{chen2024pgsr,title={PGSR: Planar-based Gaussian Splatting for Efficient and High-Fidelity Surface Reconstruction},journal={arXiv preprint arXiv:2406.06521},year={2024}}",
    },
    {
        "id": "2dgs_object_asset",
        "slug": "2dgs_object_asset",
        "title": "2D Gaussian Splatting for Geometrically Accurate Radiance Fields",
        "authors_year": "Huang et al., 2024",
        "type": "paper+repo",
        "priority": "P0",
        "review_depth": "deep",
        "family": "surfel Gaussian representation / mesh extraction",
        "pdf": "2d_gaussian_splatting_2403_17888.pdf",
        "repo": "2d-gaussian-splatting",
        "sources": ["https://github.com/hbb1/2d-gaussian-splatting", "https://arxiv.org/abs/2403.17888"],
        "sub": {"object_match": 3.7, "isaac_transfer": 4.1, "geometry_collision": 4.4, "code_repro": 4.2, "view_completion": 1.7, "engineering_readiness": 4.0},
        "inputs": "posed images / COLMAP dataset.",
        "outputs": "2D surfel Gaussians, rendered RGB/depth, mesh extraction.",
        "pipeline": ["Represent scene/object with 2D surfel-like Gaussians.", "Optimize photometric rendering with geometry-aware representation.", "Render depth and extract mesh.", "Use mesh as Isaac geometry candidate."],
        "object_asset_role": "把视觉层从 volumetric blobs 推向 surface-like representation，对碰撞层更友好。",
        "losses": "photometric reconstruction plus geometry/depth/surface regularizers depending implementation.",
        "assumptions": "多视角覆盖足够；thin objects 和 unseen surfaces 仍需补齐。",
        "failure_modes": "input sparse 时会过拟合已见面；mesh may have holes。",
        "directional_gap": "后端，不生成 unseen content。",
        "isaac_path": "adapter needed: mesh/depth output利于 USD/collision proxy。",
        "recommended_role": "P0 几何后端，与 SuGaR/PGSR 并列比较。",
        "next_experiment": "用同一 object crop 对比 3DGS+SuGaR、PGSR、2DGS 三条 mesh extraction 的 holes/collision 质量。",
        "bib": "@article{huang20242dgs,title={2D Gaussian Splatting for Geometrically Accurate Radiance Fields},journal={arXiv preprint arXiv:2403.17888},year={2024}}",
    },
    {
        "id": "gsdf",
        "slug": "gsdf_object_asset",
        "title": "GSDF: 3DGS Meets SDF for Improved Neural Rendering and Reconstruction",
        "authors_year": "Yu et al., 2024",
        "type": "paper+repo",
        "priority": "P1",
        "review_depth": "standard",
        "family": "3DGS + SDF surface constraint",
        "pdf": "gsdf_2403_16964.pdf",
        "repo": "GSDF",
        "sources": ["https://github.com/city-super/GSDF", "https://arxiv.org/abs/2403.16964"],
        "sub": {"object_match": 3.5, "isaac_transfer": 3.8, "geometry_collision": 4.2, "code_repro": 3.8, "view_completion": 1.6, "engineering_readiness": 3.4},
        "inputs": "posed RGB images, 3DGS/SDF reconstruction setup.",
        "outputs": "SDF-improved neural rendering/reconstruction with better surfaces.",
        "pipeline": ["Combine Gaussian representation with SDF-inspired geometry constraints.", "Optimize radiance and surface fields jointly.", "Use SDF signal to improve surface reconstruction.", "Extract geometry for mesh-like downstream use."],
        "object_asset_role": "和 SuGaR/PGSR/2DGS 同属 geometry repair 后端，可作为 SDF-based 对照。",
        "losses": "photometric rendering losses plus SDF/eikonal/surface related constraints.",
        "assumptions": "适合表面可由 SDF 表达的对象；训练复杂度高于纯 3DGS。",
        "failure_modes": "对透明/薄结构和未观测面仍有限；代码集成成本较高。",
        "directional_gap": "不补视角。",
        "isaac_path": "adapter needed: SDF/mesh extraction 后用于 collision proxy。",
        "recommended_role": "P1 SDF geometry baseline。",
        "next_experiment": "若 SuGaR/PGSR mesh 对门边/桌腿不稳定，再测试 GSDF surface extraction。",
        "bib": "@article{yu2024gsdf,title={GSDF: 3DGS Meets SDF for Improved Neural Rendering and Reconstruction},journal={arXiv preprint arXiv:2403.16964},year={2024}}",
    },
    {
        "id": "3dgrut_nurec",
        "slug": "3dgrut_nurec_object_asset",
        "title": "3DGRT/3DGUT/3DGRUT and NVIDIA NuRec-oriented Gaussian Rendering",
        "authors_year": "Moenne-Loccoz et al.; Wu et al., 2024/2025",
        "type": "papers+repo",
        "priority": "P0",
        "review_depth": "deep",
        "family": "production-ready Gaussian rendering / USD export / distorted cameras",
        "pdf": "3dgrut_2412_12507.pdf",
        "repo": "3DGRUT",
        "sources": ["https://github.com/nv-tlabs/3DGRUT", "https://research.nvidia.com/labs/toronto-ai/3DGUT", "https://developer.nvidia.com/omniverse/nurec"],
        "sub": {"object_match": 3.4, "isaac_transfer": 4.7, "geometry_collision": 2.8, "code_repro": 4.2, "view_completion": 2.2, "engineering_readiness": 4.0},
        "inputs": "3DGS/3DGRT/3DGUT scenes, COLMAP/NCore datasets, masks, complex camera models.",
        "outputs": "trained Gaussian scenes, USD/PLY/NuRec export, rendering with distorted cameras, rolling shutter, secondary rays.",
        "pipeline": ["Replace 3DGS projection linearization with Unscented Transform to support nonlinear camera projection.", "Unify rasterization and ray tracing formulation for primary/secondary rays.", "Train/export scenes in a production-oriented pipeline.", "Use USD/NuRec path for Omniverse/Isaac rendering integration."],
        "object_asset_role": "不解决 object geometry/collision，但非常重要：Isaac Sim 5.0/Omniverse 的 Gaussian visual layer 可能走 NuRec/USDZ/3DGRUT 生态。",
        "losses": "standard 3DGS reconstruction losses with 3DGUT projection/rendering changes.",
        "assumptions": "主要关心渲染而非物理；collision 仍需 mesh。",
        "failure_modes": "视觉层接入成功不代表可交互；复杂 camera 支持不补 missing geometry。",
        "directional_gap": "可更准确支持 Go2/广角/畸变相机训练与渲染，但不生成 unseen view。",
        "isaac_path": "direct for visual layer: USD/NuRec/Omniverse 方向最值得关注。",
        "recommended_role": "P0 visual layer integration path；和 SuGaR/OpenReal2Sim 的 geometry layer 并行。",
        "next_experiment": "把现有 3DGS/3DGRUT 输出转 NuRec/USDZ，在 Isaac Sim 5.0 中测试 RGB camera rendering 与 mesh collision 同步。",
        "bib": "@inproceedings{wu20253dgut,title={3DGUT: Enabling Distorted Cameras and Secondary Rays in Gaussian Splatting},booktitle={CVPR},year={2025}}",
    },
    {
        "id": "sage_3d",
        "slug": "sage_3d_object_asset",
        "title": "SAGE-3D: Towards Physically Executable 3D Gaussian for Embodied Navigation",
        "authors_year": "Miao et al., 2025",
        "type": "paper+repo+dataset",
        "priority": "P0",
        "review_depth": "deep",
        "family": "semantically and physically aligned 3DGS environment",
        "pdf": "sage_3d_2510_21307.pdf",
        "repo": "SAGE-3D_Official",
        "sources": ["https://github.com/Galery23/SAGE-3D_Official", "https://arxiv.org/abs/2510.21307", "https://sage-3d.github.io/"],
        "sub": {"object_match": 3.6, "isaac_transfer": 4.6, "geometry_collision": 4.2, "code_repro": 4.0, "view_completion": 2.0, "engineering_readiness": 3.8},
        "inputs": "3DGS indoor scenes, object annotations, mesh scenes/collision bodies, Isaac Sim 5.0+.",
        "outputs": "InteriorGS object-annotated 3DGS scenes, collision meshes, USDZ assets, VLN benchmark.",
        "pipeline": ["Ground object-level semantics into 3DGS scenes.", "Extract collision bodies for each object from mesh sources.", "Use 3DGS-Mesh hybrid representation: 3DGS for appearance, mesh collision for physics.", "Run embodied navigation benchmark in Isaac Sim 5.0+."],
        "object_asset_role": "虽是导航而非 manipulation，但它系统化验证了 object-level semantics + collision bodies + 3DGS visual layer 的必要性。",
        "losses": "dataset/benchmark construction; policy training uses VLN losses/rewards; not a reconstruction-loss paper.",
        "assumptions": "数据来自 artist-created mesh scenes rather than real scans；对真实 Go2 场景需构建 equivalent asset pipeline。",
        "failure_modes": "可执行性来自已有 mesh，不是从坏 3DGS 自动恢复；navigation collision 简化不等于 manipulation contact 精度。",
        "directional_gap": "不补视角，但证明 3DGS 必须和 object/collision layer 对齐才能用于 embodied tasks。",
        "isaac_path": "direct: README 明确 Isaac Sim 5.0+，并有 USDZ/Collision Mesh datasets。",
        "recommended_role": "P0 Isaac 5.0 视觉/物理混合环境参考；对 Go2 导航平台非常相关。",
        "next_experiment": "参考 InteriorGS 数据格式，为一个 Go2 room scene 生成 object annotation + collision body + 3DGS visual package。",
        "bib": "@article{miao2025sage3d,title={Towards Physically Executable 3D Gaussian for Embodied Navigation},journal={arXiv preprint arXiv:2510.21307},year={2025}}",
    },
    {
        "id": "splat_mover",
        "slug": "splat_mover_object_asset",
        "title": "Splat-MOVER: Robotic Manipulation via Editable Gaussian Splatting",
        "authors_year": "Stanford MSL et al., 2024",
        "type": "paper+repo",
        "priority": "P1",
        "review_depth": "standard",
        "family": "editable semantic/affordance GS for manipulation",
        "pdf": "splat_mover_2405_04378.pdf",
        "repo": "Splat-MOVER",
        "sources": ["https://github.com/StanfordMSL/Splat-MOVER", "https://splatmover.github.io/", "https://arxiv.org/abs/2405.04378"],
        "sub": {"object_match": 3.7, "isaac_transfer": 2.6, "geometry_collision": 2.8, "code_repro": 3.7, "view_completion": 2.1, "engineering_readiness": 3.7},
        "inputs": "brief pre-scan RGB images, language prompt, pretrained semantic/grasp affordance features.",
        "outputs": "ASK-Splat semantic/affordance Gaussians, SEE-Splat scene edits, Grasp-Splat grasp proposals.",
        "pipeline": ["Train ASK-Splat from posed RGB images with CLIP and grasp affordance features.", "Localize objects from open-vocabulary prompt.", "SEE-Splat edits object pose/scene state after manipulation.", "Grasp-Splat proposes affordance-aligned grasps."],
        "object_asset_role": "不是资产导出主线，但给出 object asset 是否支持 semantic/affordance/manipulation 的评价维度。",
        "losses": "Gaussian reconstruction losses plus feature/affordance distillation; grasp ranking uses affordance scores.",
        "assumptions": "workspace小、预扫描短、动作后对象可通过编辑更新；不追求 Isaac asset fidelity。",
        "failure_modes": "视觉编辑不等于物理仿真；collision/mesh/physics 参数缺失。",
        "directional_gap": "局部 object infilling 仅视觉。",
        "isaac_path": "not direct; 可迁移 semantic/affordance features 到 Isaac asset metadata。",
        "recommended_role": "P1 interaction evaluation reference。",
        "next_experiment": "把 ObjectGS 生成的 object Gaussians 加上语言/affordance tags，测试是否能服务 grasp planning。",
        "bib": "@article{splatmover2024,title={Robotic Manipulation via Editable Gaussian Splatting},journal={arXiv preprint arXiv:2405.04378},year={2024}}",
    },
    {
        "id": "graspsplats",
        "slug": "graspsplats_object_asset",
        "title": "GraspSplats: Efficient Manipulation with 3D Feature Splatting",
        "authors_year": "Ji et al., 2024",
        "type": "paper+repo",
        "priority": "P1",
        "review_depth": "standard",
        "family": "feature-enhanced 3DGS for part-level grasping",
        "pdf": "graspsplats_2409_02084.pdf",
        "repo": "GraspSplats",
        "sources": ["https://github.com/jimazeyu/GraspSplats", "https://graspsplats.github.io/", "https://arxiv.org/abs/2409.02084"],
        "sub": {"object_match": 3.6, "isaac_transfer": 2.5, "geometry_collision": 3.0, "code_repro": 3.5, "view_completion": 1.8, "engineering_readiness": 3.6},
        "inputs": "posed RGB-D frames from calibrated camera, MobileSAM/MaskCLIP features.",
        "outputs": "feature-enhanced explicit Gaussians, part-level affordance, grasp proposals, dynamic object updates.",
        "pipeline": ["Initialize Gaussians from depth frames.", "Compute 2D reference features and optimize geometry/texture/semantics by differentiable rasterization.", "Use object/part language queries to predict affordance.", "Generate grasp proposals from explicit Gaussian primitives and update under object motion."],
        "object_asset_role": "给出 part-level interaction/grasp 的下游验证方式；适合评价生成的门把手/椅子部件是否能被定位和操作。",
        "losses": "depth/photometric/feature supervision and grasp proposal scoring.",
        "assumptions": "有 RGB-D 且目标工作空间较小；任务是抓取而非完整 digital twin export。",
        "failure_modes": "不输出 collision/physical parameters；动态更新依赖 tracking。",
        "directional_gap": "不补视角。",
        "isaac_path": "not direct; 可作为 Isaac asset 的 affordance metadata generator。",
        "recommended_role": "P1 manipulation evaluation tool。",
        "next_experiment": "对生成/重建的桌椅部件跑 GraspSplats-style feature distillation，测试 part query localization。",
        "bib": "@article{ji2024graspsplats,title={GraspSplats: Efficient Manipulation with 3D Feature Splatting},journal={arXiv preprint arXiv:2409.02084},year={2024}}",
    },
    {
        "id": "gaussian_grasper",
        "slug": "gaussian_grasper_object_asset",
        "title": "GaussianGrasper: 3D Language Gaussian Splatting for Open-vocabulary Robotic Grasping",
        "authors_year": "Zheng et al., 2024",
        "type": "paper+repo",
        "priority": "P1",
        "review_depth": "standard",
        "family": "language Gaussian field + grasping",
        "pdf": "gaussiangrasper_2403_09637.pdf",
        "repo": "GaussianGrasper",
        "sources": ["https://github.com/MrSecant/GaussianGrasper", "https://arxiv.org/abs/2403.09637"],
        "sub": {"object_match": 3.5, "isaac_transfer": 2.4, "geometry_collision": 3.0, "code_repro": 3.2, "view_completion": 1.7, "engineering_readiness": 3.3},
        "inputs": "limited RGB-D views, SAM/CLIP features, pretrained grasping model.",
        "outputs": "language-embedded Gaussian feature field, rendered depth/normal, collision-free grasp pose candidates.",
        "pipeline": ["Initialize 3DGS from RGB-D scans.", "Distill dense language features using SAM and CLIP with contrastive learning.", "Locate target from open-vocabulary query.", "Use rendered normals and geometry to filter grasp candidates, then update scene after manipulation."],
        "object_asset_role": "交互层参考：object asset 不仅要能看，还应提供 language query 和 grasp geometry。",
        "losses": "contrastive feature distillation, photometric/geometric reconstruction, normal-guided grasp filtering.",
        "assumptions": "RGB-D 质量可靠；open-vocabulary features定位足够精准。",
        "failure_modes": "feature 边界和 grasp 质量受 3DGS geometry 影响；不生成完整 mesh/collision asset。",
        "directional_gap": "不补视角。",
        "isaac_path": "not direct; metadata/affordance path only。",
        "recommended_role": "P1 interaction evaluation baseline。",
        "next_experiment": "用它的 language feature field 检查重建资产是否能定位“door handle/table leg/chair back”。",
        "bib": "@article{zheng2024gaussiangrasper,title={GaussianGrasper: 3D Language Gaussian Splatting for Open-vocabulary Robotic Grasping},journal={arXiv preprint arXiv:2403.09637},year={2024}}",
    },
    {
        "id": "object_aware_gaussian_robotics",
        "slug": "object_aware_gaussian_robotics",
        "title": "Object-Aware Gaussian Splatting for Robotic Manipulation",
        "authors_year": "Li and Pathak, 2024",
        "type": "paper",
        "priority": "P1",
        "review_depth": "standard",
        "family": "dynamic object-aware Gaussians for manipulation",
        "pdf": "object_aware_gaussian_splatting_robotic_manipulation_2024_openreview.pdf",
        "repo": None,
        "sources": ["https://object-aware-gaussian.github.io/", "https://openreview.net/forum?id=t46z5MslkU"],
        "sub": {"object_match": 3.6, "isaac_transfer": 2.1, "geometry_collision": 2.6, "code_repro": 1.8, "view_completion": 2.0, "engineering_readiness": 2.8},
        "inputs": "three RGB-D camera views, object-wise segmentation, pretrained foundation model semantics.",
        "outputs": "dynamic object-aware Gaussian representation updated at about 30 Hz; language-conditioned dynamic grasping.",
        "pipeline": ["Initialize dense point cloud and object-wise Gaussians from few RGB-D cameras.", "Inject objectness/semantic labels at initialization.", "Update Gaussians object-wise rather than per-Gaussian for speed.", "Use representation for dynamic language-conditioned grasping and visuomotor policy training."],
        "object_asset_role": "强调 objectness 对实时交互的重要性，可启发资产运行时更新模块。",
        "losses": "dynamic 3DGS reconstruction/update objectives; policy imitation/behavior cloning in downstream usage.",
        "assumptions": "多 RGB-D 相机固定覆盖 workspace；不是离线高保真 Isaac asset pipeline。",
        "failure_modes": "无开源代码；碰撞/mesh/physical parameters 缺失。",
        "directional_gap": "通过多 RGB-D 视角减少缺失，但不是生成式补齐。",
        "isaac_path": "not direct。",
        "recommended_role": "P1 runtime object update idea，不作为短期复现。",
        "next_experiment": "借鉴 object-wise update 思路，为 Isaac 中可移动物体维护 object ID 和 visual layer transform。",
        "bib": "@inproceedings{li2024objectaware,title={Object-Aware Gaussian Splatting for Robotic Manipulation},author={Li, Yulong and Pathak, Deepak},booktitle={CoRL Workshop / OpenReview},year={2024}}",
    },
    {
        "id": "instantmesh",
        "slug": "instantmesh_object_asset",
        "title": "InstantMesh: Efficient 3D Mesh Generation from a Single Image with Sparse-view Large Reconstruction Models",
        "authors_year": "Xu et al., 2024",
        "type": "paper+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "single-image mesh generation baseline",
        "pdf": "instantmesh_2404_07191.pdf",
        "repo": "InstantMesh",
        "sources": ["https://github.com/TencentARC/InstantMesh", "https://arxiv.org/abs/2404.07191", "https://huggingface.co/TencentARC/InstantMesh"],
        "sub": {"object_match": 3.6, "isaac_transfer": 3.5, "geometry_collision": 3.4, "code_repro": 4.5, "view_completion": 3.7, "engineering_readiness": 4.2},
        "inputs": "single object image / alpha mask.",
        "outputs": "textured mesh / OBJ with vertex colors or texture map.",
        "pipeline": ["Generate 3D-consistent sparse multi-view images using diffusion.", "Feed sparse views into LRM-style reconstruction model.", "Use differentiable iso-surface extraction/FlexiCubes for direct mesh output.", "Export OBJ/textured mesh within seconds."],
        "object_asset_role": "快速 single-image mesh baseline，适合做 Hunyuan3D 的轻量替代或 ablation。",
        "losses": "multi-view diffusion objectives and reconstruction losses over mesh/depth/normal supervision.",
        "assumptions": "输入是干净单物体；输出未保证真实场景对齐。",
        "failure_modes": "生成背面可能错误；mesh 细节/scale/collision 需后处理。",
        "directional_gap": "可补单物体背面，需 reject test。",
        "isaac_path": "adapter needed: OBJ/mesh 可导入但需 scale/material/collision。",
        "recommended_role": "P1 quick generative mesh baseline。",
        "next_experiment": "同一 object crop 跑 InstantMesh/Hunyuan3D/GaussianObject，比较 mesh vs 3DGS visual layer。",
        "bib": "@article{xu2024instantmesh,title={InstantMesh: Efficient 3D Mesh Generation from a Single Image with Sparse-view Large Reconstruction Models},journal={arXiv preprint arXiv:2404.07191},year={2024}}",
    },
    {
        "id": "triposr",
        "slug": "triposr_object_asset",
        "title": "TripoSR: Fast 3D Object Reconstruction from a Single Image",
        "authors_year": "Tochilkin et al., 2024",
        "type": "tech-report+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "ultra-fast single-image object mesh reconstruction",
        "pdf": "triposr_2403_02151.pdf",
        "repo": "TripoSR",
        "sources": ["https://github.com/VAST-AI-Research/TripoSR", "https://arxiv.org/abs/2403.02151", "https://huggingface.co/stabilityai/TripoSR"],
        "sub": {"object_match": 3.3, "isaac_transfer": 3.2, "geometry_collision": 3.0, "code_repro": 4.3, "view_completion": 3.3, "engineering_readiness": 4.5},
        "inputs": "single object image.",
        "outputs": "mesh from feed-forward triplane/LRM-style reconstruction in under 0.5s on A100.",
        "pipeline": ["Encode image with transformer model.", "Decode image tokens into triplane-NeRF representation.", "Extract mesh with texture/vertex color.", "Use as fast object shape prior."],
        "object_asset_role": "速度极快，适合当 sanity check baseline，而非高保真主线。",
        "losses": "mask/color/rendering reconstruction losses in LRM training.",
        "assumptions": "物体居中干净；几何细节/真实对齐要求不高。",
        "failure_modes": "shape oversmoothing, scale unknown, physical/collision absent。",
        "directional_gap": "粗略背面先验。",
        "isaac_path": "adapter needed; mesh需后处理。",
        "recommended_role": "P1/P2 快速 baseline。",
        "next_experiment": "把 TripoSR 作为 1 秒级低成本对照，判断复杂方法是否真正提升。",
        "bib": "@article{tochilkin2024triposr,title={TripoSR: Fast 3D Object Reconstruction from a Single Image},journal={arXiv preprint arXiv:2403.02151},year={2024}}",
    },
    {
        "id": "crm_object_asset",
        "slug": "crm_object_asset",
        "title": "CRM: Single Image to 3D Textured Mesh with Convolutional Reconstruction Model",
        "authors_year": "Wang et al., 2024",
        "type": "paper+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "single-image textured mesh generation",
        "pdf": "crm_2403_05034.pdf",
        "repo": "CRM",
        "sources": ["https://github.com/thu-ml/CRM", "https://arxiv.org/abs/2403.05034"],
        "sub": {"object_match": 3.3, "isaac_transfer": 3.4, "geometry_collision": 3.2, "code_repro": 3.8, "view_completion": 3.5, "engineering_readiness": 3.6},
        "inputs": "single image; foreground preprocessing/grey background recommended.",
        "outputs": "textured OBJ mesh, multi-view generated images, canonical coordinate maps.",
        "pipeline": ["Generate six orthographic views with multi-view diffusion.", "Generate canonical coordinate maps.", "Feed views and CCMs into convolutional reconstruction model.", "Optimize/export textured mesh with UV texture."],
        "object_asset_role": "和 InstantMesh 同类，但直接 textured mesh，适合作为 asset generation baseline。",
        "losses": "multi-view diffusion and mesh reconstruction objectives with FlexiCubes.",
        "assumptions": "clean object crop; no real metric scale。",
        "failure_modes": "background preprocessing敏感；背面 hallucination；collision需重建。",
        "directional_gap": "可补单物体未见面但须验证。",
        "isaac_path": "adapter needed。",
        "recommended_role": "P1 generative mesh baseline。",
        "next_experiment": "对 Hunyuan3D/InstantMesh/CRM 输出进行 ICP+collision proxy 比较。",
        "bib": "@article{wang2024crm,title={CRM: Single Image to 3D Textured Mesh with Convolutional Reconstruction Model},journal={arXiv preprint arXiv:2403.05034},year={2024}}",
    },
    {
        "id": "lgm_object_asset",
        "slug": "lgm_object_asset",
        "title": "LGM: Large Multi-View Gaussian Model for High-Resolution 3D Content Creation",
        "authors_year": "Tang et al., 2024",
        "type": "paper+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "single/text-to-3D Gaussian generation + mesh conversion",
        "pdf": "lgm_2402_05054.pdf",
        "repo": "LGM",
        "sources": ["https://github.com/3DTopia/LGM", "https://arxiv.org/abs/2402.05054"],
        "sub": {"object_match": 3.4, "isaac_transfer": 3.2, "geometry_collision": 3.2, "code_repro": 4.0, "view_completion": 3.6, "engineering_readiness": 3.6},
        "inputs": "text prompt or single-view image; multi-view diffusion generated views.",
        "outputs": "high-resolution 3D Gaussians, optional smooth textured mesh.",
        "pipeline": ["Generate multi-view images from image/text.", "Use asymmetric U-Net to predict multi-view Gaussian features.", "Fuse features into 3D Gaussians.", "Convert generated Gaussians to textured mesh if needed."],
        "object_asset_role": "少数直接生成 3D Gaussians 的 object content model，可补 visual layer；mesh/collision仍需后处理。",
        "losses": "regression objectives on multi-view Gaussian reconstruction and rendering supervision.",
        "assumptions": "generated object prior may not match real object; scale/pose unknown。",
        "failure_modes": "mesh conversion耗时且可能不稳定；背面细节 hallucination。",
        "directional_gap": "可作为 object backside/visual layer prior。",
        "isaac_path": "adapter needed: Gaussian visual + mesh conversion。",
        "recommended_role": "P1 3DGS object generation baseline。",
        "next_experiment": "比较 LGM 直接生成 Gaussians 与 Hunyuan3D mesh+PBR 的 visual fidelity/mesh usability。",
        "bib": "@article{tang2024lgm,title={LGM: Large Multi-View Gaussian Model for High-Resolution 3D Content Creation},journal={arXiv preprint arXiv:2402.05054},year={2024}}",
    },
    {
        "id": "wonder3d_object_asset",
        "slug": "wonder3d_object_asset",
        "title": "Wonder3D: Single Image to 3D using Cross-Domain Diffusion",
        "authors_year": "Long et al., 2023",
        "type": "paper+repo+weights",
        "priority": "P1",
        "review_depth": "standard",
        "family": "multi-view normal/color generation + mesh reconstruction",
        "pdf": "wonder3d_2310_15008.pdf",
        "repo": "Wonder3D",
        "sources": ["https://github.com/xxlong0/Wonder3D", "https://arxiv.org/abs/2310.15008"],
        "sub": {"object_match": 3.2, "isaac_transfer": 3.2, "geometry_collision": 3.3, "code_repro": 3.8, "view_completion": 3.7, "engineering_readiness": 3.4},
        "inputs": "single object image.",
        "outputs": "consistent multi-view normal maps/color images and textured mesh.",
        "pipeline": ["Generate multi-view normals and colors with cross-domain diffusion.", "Use cross-domain attention for view/modality consistency.", "Fuse normals geometry-aware to extract surface.", "Texture reconstructed mesh."],
        "object_asset_role": "normal maps对几何补全有帮助，可作为 object mesh generation baseline。",
        "losses": "diffusion losses over normal/color domains; surface fusion postprocess。",
        "assumptions": "single clean object image; generated normals may diverge from真实测量。",
        "failure_modes": "thin/reflective objects难；scale/collision absent。",
        "directional_gap": "背面 normal/color prior。",
        "isaac_path": "adapter needed。",
        "recommended_role": "P1 mesh generation baseline，优先级低于 Hunyuan3D/InstantMesh。",
        "next_experiment": "仅在 Hunyuan3D/InstantMesh 失败时做替补测试。",
        "bib": "@article{long2023wonder3d,title={Wonder3D: Single Image to 3D using Cross-Domain Diffusion},journal={arXiv preprint arXiv:2310.15008},year={2023}}",
    },
    {
        "id": "rialto",
        "slug": "rialto_object_asset",
        "title": "RialTo: A Real-to-Sim-to-Real Approach for Robust Manipulation",
        "authors_year": "Torne et al., 2024",
        "type": "paper+repo",
        "priority": "P1",
        "review_depth": "standard",
        "family": "real-to-sim-to-real manipulation loop / digital twin evaluation",
        "pdf": "rialto_2403_03949.pdf",
        "repo": "RialToPolicyLearning",
        "sources": ["https://real-to-sim-to-real.github.io/RialTo/", "https://github.com/real-to-sim-to-real/RialToPolicyLearning", "https://arxiv.org/abs/2403.03949"],
        "sub": {"object_match": 3.2, "isaac_transfer": 3.8, "geometry_collision": 3.5, "code_repro": 3.2, "view_completion": 1.2, "engineering_readiness": 3.5},
        "inputs": "scanned real scene/digital twin, user corrections, demonstrations/policies.",
        "outputs": "real-to-sim-to-real manipulation policies and evaluation loop.",
        "pipeline": ["Create digital twin from real setup.", "Use simulation to train/robustify policy.", "Deploy policy to real robot and collect failures.", "Iteratively improve digital twin/policy."],
        "object_asset_role": "不是 3DGS asset 方法，但给出老师关心的闭环：资产不是终点，要能提升 manipulation/navigation 任务。",
        "losses": "policy learning/reinforcement/imitation objectives depending task.",
        "assumptions": "digital twin 足够可编辑且用户能修正；不自动解决 asset generation。",
        "failure_modes": "人工参与较多；visual fidelity 不一定等于 3DGS 质量。",
        "directional_gap": "无直接关系。",
        "isaac_path": "conceptual adapter; 可作为 evaluation loop。",
        "recommended_role": "P1 evaluation/process reference。",
        "next_experiment": "把 object asset 质量最终和 Go2 navigation/manipulation rollout 成功率挂钩，不只看 PSNR/LPIPS。",
        "bib": "@article{torne2024rialto,title={RialTo: A Real-to-Sim-to-Real Approach for Robust Manipulation},journal={arXiv preprint arXiv:2403.03949},year={2024}}",
    },
    {
        "id": "embodiedgen",
        "slug": "embodiedgen_object_asset",
        "title": "EmbodiedGen: Towards a Generative 3D World Engine for Embodied AI",
        "authors_year": "Horizon Robotics et al., 2025",
        "type": "paper+repo",
        "priority": "P1",
        "review_depth": "standard",
        "family": "generative embodied 3D world / asset prior",
        "pdf": "embodiedgen_2506_10600.pdf",
        "repo": "EmbodiedGen",
        "sources": ["https://github.com/HorizonRobotics/EmbodiedGen", "https://arxiv.org/abs/2506.10600"],
        "sub": {"object_match": 2.8, "isaac_transfer": 3.0, "geometry_collision": 3.0, "code_repro": 3.0, "view_completion": 3.6, "engineering_readiness": 2.8},
        "inputs": "generative prompts/conditions for embodied scenes/assets.",
        "outputs": "3D worlds/assets for embodied AI; varies by release.",
        "pipeline": ["Use generative models to create embodied 3D assets/worlds.", "Provide assets/scene priors for simulation data scaling.", "Potentially combine mesh/3DGS/physics outputs depending module.", "Requires registration to real scenes for real2sim use."],
        "object_asset_role": "长期方向：帮助扩充资产库和低置信区域先验，不替代真实指定物体。",
        "losses": "generative model training objectives; not tightly tied to our real scene.",
        "assumptions": "需要生成而非忠实重建；真实对齐弱。",
        "failure_modes": "可能生成好看但不真实的场景/物体；physics correctness 不确定。",
        "directional_gap": "作为 semantic/visual prior。",
        "isaac_path": "adapter needed。",
        "recommended_role": "P1/P2 long-term generative prior。",
        "next_experiment": "仅用于补默认资产库或低置信候选，不纳入短期闭环。",
        "bib": "@article{embodiedgen2025,title={EmbodiedGen: Towards a Generative 3D World Engine for Embodied AI},journal={arXiv preprint arXiv:2506.10600},year={2025}}",
    },
    {
        "id": "robosplat",
        "slug": "robosplat_object_asset",
        "title": "RoboSplat: 3DGS-based Robotic Demonstration Generation",
        "authors_year": "InternRobotics et al., 2025",
        "type": "paper+repo",
        "priority": "P1",
        "review_depth": "standard",
        "family": "robot data generation with 3DGS",
        "pdf": "robosplat_2504_13175.pdf",
        "repo": "RoboSplat",
        "sources": ["https://github.com/InternRobotics/RoboSplat", "https://arxiv.org/abs/2504.13175"],
        "sub": {"object_match": 2.9, "isaac_transfer": 3.1, "geometry_collision": 2.8, "code_repro": 3.7, "view_completion": 2.2, "engineering_readiness": 3.4},
        "inputs": "robot demonstrations and 3DGS scene representation.",
        "outputs": "augmented/synthetic robotic demonstrations.",
        "pipeline": ["Build 3DGS scene/robot representation.", "Transform/recompose demonstrations in 3D.", "Render synthetic observations.", "Use generated demos for policy learning."],
        "object_asset_role": "数据生成与 policy augmentation 参考，不是资产生成核心。",
        "losses": "reconstruction and policy/demonstration learning objectives.",
        "assumptions": "已有可用 3DGS asset；不解决物体 mesh/collision。",
        "failure_modes": "输入 asset 坏则输出数据也坏。",
        "directional_gap": "不补视角。",
        "isaac_path": "indirect。",
        "recommended_role": "P1 后续 data scaling 参考。",
        "next_experiment": "在 asset pipeline 稳定后再考虑用其生成 Go2/robot policy data。",
        "bib": "@article{robosplat2025,title={RoboSplat: 3DGS-based Robotic Demonstration Generation},journal={arXiv preprint arXiv:2504.13175},year={2025}}",
    },
    {
        "id": "gen2sim",
        "slug": "gen2sim_object_asset",
        "title": "Gen2Sim: Scaling up Robot Learning in Simulation with Generative Models",
        "authors_year": "Tung et al., 2023",
        "type": "paper",
        "priority": "P2",
        "review_depth": "skim",
        "family": "generative simulation asset/data scaling",
        "pdf": "gen2sim_2310_18308.pdf",
        "repo": None,
        "sources": ["https://arxiv.org/abs/2310.18308"],
        "sub": {"object_match": 2.5, "isaac_transfer": 3.0, "geometry_collision": 2.6, "code_repro": 1.5, "view_completion": 2.5, "engineering_readiness": 2.4},
        "inputs": "generative model-created objects/scenes/tasks.",
        "outputs": "simulation assets/tasks for robot learning.",
        "pipeline": ["Use generative models to create diverse simulation objects/scenes.", "Train robot policies in generated simulation.", "Evaluate sim-to-real/task generalization.", "Iterate generation/evaluation."],
        "object_asset_role": "概念上支持生成式资产库，但与真实指定物体 fidelity 不匹配。",
        "losses": "policy learning objectives; generative losses outside focus.",
        "assumptions": "目标是 diversity 而非 real2sim accuracy。",
        "failure_modes": "不保证 Isaac-ready object/collision。",
        "directional_gap": "无直接关系。",
        "isaac_path": "indirect。",
        "recommended_role": "P2 背景参考。",
        "next_experiment": "不投入短期复现。",
        "bib": "@article{tung2023gen2sim,title={Gen2Sim: Scaling up Robot Learning in Simulation with Generative Models},journal={arXiv preprint arXiv:2310.18308},year={2023}}",
    },
    {
        "id": "r2g_repo_only",
        "slug": "r2g_repo_only_object_asset",
        "title": "R2G: Real-to-Generative Robot Simulation Repository",
        "authors_year": "BigCiLeng project, 2025",
        "type": "repo",
        "priority": "P2",
        "review_depth": "skim",
        "family": "repo-only real-to-generative simulation",
        "pdf": "",
        "repo": "R2G",
        "sources": ["https://github.com/BigCiLeng/R2G"],
        "sub": {"object_match": 2.4, "isaac_transfer": 2.6, "geometry_collision": 2.2, "code_repro": 3.0, "view_completion": 2.6, "engineering_readiness": 2.7},
        "inputs": "repo-specific robot simulation/generation inputs.",
        "outputs": "repo-specific generated simulation resources.",
        "pipeline": ["Repo cloned for monitoring.", "No stable paper metadata found in this round.", "Treat as watchlist item only.", "Upgrade if technical report/weights/Isaac path become clear."],
        "object_asset_role": "资料不完整，不能支撑当前主线。",
        "losses": "not verified.",
        "assumptions": "repo may evolve.",
        "failure_modes": "evidence insufficient.",
        "directional_gap": "unknown.",
        "isaac_path": "unverified.",
        "recommended_role": "P2 watchlist.",
        "next_experiment": "暂不实验。",
        "bib": "",
    },
    {
        "id": "3dgen4robot",
        "slug": "3dgen4robot_object_asset",
        "title": "3DGen4Robot: Survey/Collection for 3D Generation in Robot Learning",
        "authors_year": "project repo, 2025/2026",
        "type": "repo",
        "priority": "P2",
        "review_depth": "skim",
        "family": "survey / awesome list / robot 3D generation resources",
        "pdf": "",
        "repo": "3DGen4Robot",
        "sources": ["https://github.com/hitcslj/3DGen4Robot"],
        "sub": {"object_match": 2.5, "isaac_transfer": 2.5, "geometry_collision": 2.2, "code_repro": 3.0, "view_completion": 2.5, "engineering_readiness": 3.0},
        "inputs": "curated links.",
        "outputs": "taxonomy/reference list.",
        "pipeline": ["Use as discovery list.", "Do not use as evidence for implementation claims.", "Promote individual papers only after PDF/repo verification.", "Maintain watchlist."],
        "object_asset_role": "帮助后续拓展，不进入实现排序。",
        "losses": "not applicable.",
        "assumptions": "curation quality may vary.",
        "failure_modes": "link rot / unverified claims.",
        "directional_gap": "not applicable.",
        "isaac_path": "not applicable.",
        "recommended_role": "P2 survey/watchlist.",
        "next_experiment": "只用来发现遗漏工作。",
        "bib": "",
    },
]


def enrich_entries() -> None:
    for e in ENTRIES:
        e["score"] = weighted_score(e["sub"])
        e["repo_meta"] = repo_meta(e.get("repo"))
        pdfs = []
        if e.get("pdf", ""):
            pdfs.append(e["pdf"])
        pdfs.extend(e.get("supplementary_pdfs", []))
        local_pdfs = []
        for part in [p.strip() for p in pdfs if p.strip()]:
            path = REF / part
            if path.exists():
                local_pdfs.append(str(path.relative_to(ROOT)).replace("\\", "/"))
        e["local_pdf"] = local_pdfs[0] if local_pdfs else ""
        e["local_supplementary_pdfs"] = local_pdfs[1:]
        if e.get("repo"):
            repo_path = REPOS / e["repo"]
            e["local_repo"] = str(repo_path.relative_to(ROOT)).replace("\\", "/") if repo_path.exists() else ""
        else:
            e["local_repo"] = ""


def report_md(e: dict) -> str:
    meta = e["repo_meta"]
    rows = [
        ["字段", "内容"],
        ["priority / score", f"{e['priority']} / {e['score']}/5"],
        ["family", e["family"]],
        ["sources", "<br>".join(e["sources"])],
        ["local_pdf", e["local_pdf"] or "无"],
        ["local_supplementary_pdfs", "<br>".join(e.get("local_supplementary_pdfs", [])) or "无"],
        ["local_repo", e["local_repo"] or "无"],
        ["commit / license", f"{meta['commit'] or 'n/a'} / {meta['license_file'] or 'n/a'} ({meta['status']})"],
    ]
    bullets = lambda xs: "\n".join(f"- {x}" for x in xs)
    return f"""# {e['title']}

## 定位
{e['object_asset_role']}

{md_table(rows)}

## Inputs / Outputs
- Inputs: {e['inputs']}
- Outputs: {e['outputs']}

## Full Method Pipeline
{bullets(e['pipeline'])}

## Losses / Objectives
{e['losses']}

## Assumptions
{e['assumptions']}

## Failure Modes
{e['failure_modes']}

## 对 Directional View Gap 的关系
{e['directional_gap']}

## Isaac Sim Transfer
{e['isaac_path']}

## 可迁移模块
- scene/object representation: {e['family']}
- view/object completion: {e['directional_gap']}
- geometry/collision: {e['outputs']}
- simulator integration: {e['isaac_path']}
- evaluation metrics: mesh watertightness, collision proxy validity, object-level novel-view consistency, task success / collision rate.

## Recommended Role
{e['recommended_role']}

## Next Experiment
{e['next_experiment']}
"""


def write_entry_reports() -> None:
    NOTES.mkdir(exist_ok=True)
    for e in ENTRIES:
        md = report_md(e)
        md_path = NOTES / f"{e['slug']}_object_asset_digest.md"
        html_path = NOTES / f"{e['slug']}.html"
        md_path.write_text(md, encoding="utf-8")
        html_path.write_text(simple_md_to_html(md, e["title"]), encoding="utf-8")
        e["note_paths"] = [
            str(md_path.relative_to(ROOT)).replace("\\", "/"),
            str(html_path.relative_to(ROOT)).replace("\\", "/"),
        ]


def transfer_matrix_md() -> str:
    rows = [[
        "rank",
        "method",
        "family",
        "input requirement",
        "output asset",
        "object selection",
        "view/backside completion",
        "geometry/collision",
        "Isaac Sim path",
        "code/weights",
        "risk",
        "score",
        "recommended role",
    ]]
    for idx, e in enumerate(sorted(ENTRIES, key=lambda x: x["score"], reverse=True), start=1):
        meta = e["repo_meta"]
        code = f"{meta['status']}; {e['local_repo'] or 'no repo'}; commit {meta['commit'] or 'n/a'}"
        rows.append([
            str(idx),
            f"[{e['title']}]({e['slug']}.html)",
            e["family"],
            e["inputs"],
            e["outputs"],
            "direct" if any(k in e["family"].lower() for k in ["object-aware", "grouping", "segmentation"]) or "object" in e["inputs"].lower() else "adapter needed",
            e["directional_gap"],
            e["outputs"],
            e["isaac_path"],
            code,
            e["failure_modes"],
            str(e["score"]),
            e["recommended_role"],
        ])
    return "# Object-Centric Isaac Asset Transfer Matrix\n\n" + md_table(rows) + "\n"


def index_md() -> str:
    rows = [["priority", "score", "method", "depth", "local notes"]]
    for e in sorted(ENTRIES, key=lambda x: (x["priority"], -x["score"])):
        rows.append([
            e["priority"],
            str(e["score"]),
            e["title"],
            e["review_depth"],
            "<br>".join(e["note_paths"]),
        ])
    return f"""# Object-Centric Isaac Asset Research Index

## 更新后的调研问题
给定单视角或多视角 RGB/RGB-D、camera poses、point cloud / depth / 3DGS 等真实观测，针对指定可交互物体生成 Isaac Sim 可用的 dual-layer asset：**3DGS visual layer + geometry/collision/physics layer**。原来的 directional view completion 仍保留，但定位为“补齐指定物体未观测面/反向视角”的子模块。

## Scoring Weights
- object-level match: 25%
- Isaac / simulator transfer: 25%
- geometry / collision / physics output: 20%
- code / weights reproducibility: 15%
- view or backside completion ability: 10%
- engineering readiness: 5%

{md_table(rows)}
"""


def final_report_md() -> str:
    sorted_entries = sorted(ENTRIES, key=lambda x: x["score"], reverse=True)
    top = "\n".join(f"{i}. **{e['title']}** ({e['score']}/5, {e['priority']}): {e['recommended_role']}" for i, e in enumerate(sorted_entries[:15], start=1))
    family_rows = [
        ["layer", "role", "preferred methods", "why"],
        ["1 object selection", "从整场景中得到指定物体 visual subset", "ObjectGS, Gaussian Grouping, SAGA", "没有 object identity，就无法输出指定物体资产，也无法给门/桌椅做独立 collision。"],
        ["2 object view/backside completion", "补齐稀疏视角下物体背面和压缩区域", "GaussianObject, Hunyuan3D-Omni/2.1, InstantMesh/CRM/LGM", "把原 directional view gap 从 scene-level 收束到 object-level missing surfaces。"],
        ["3 visual layer", "保持照片级观察输入", "GSWorld, ObjectGS, LGM, 3DGRUT/NuRec", "3DGS 负责 photorealistic rendering，但不承担物理碰撞。"],
        ["4 geometry/collision layer", "输出可导入模拟器的 mesh/collision proxy", "SuGaR, PGSR, 2DGS, GSDF, Scalable Real2Sim", "Isaac 交互依赖稳定几何、凸分解、质量/惯量。"],
        ["5 simulator integration", "导入 Isaac / IsaacLab 并验证任务", "OpenReal2Sim, Re3Sim, SAGE-3D, GSWorld", "最终验收不是只看图像，而是 USD/GLB/URDF/collision 在 Isaac 中可运行。"],
        ["6 physical semantics", "补 part/material/affordance/kinematics", "Scalable Real2Sim, PhysX-3D, PhysForge, Hunyuan3D-Part", "门、抽屉、桌椅等可交互对象需要 part hierarchy 和物理属性。"],
    ]
    experiment_rows = [
        ["phase", "experiment", "success criteria"],
        ["E0", "复现 GSWorld/SuGaR 最小对象：一个小物体或门/椅子局部", "得到 metric 3DGS + mesh + collision proxy，并能在 Isaac/IsaacLab 中渲染和碰撞。"],
        ["E1", "ObjectGS/Gaussian Grouping 提取指定物体", "object-only rendering/mesh export 成功；物体边界不粘连背景。"],
        ["E2", "GaussianObject/Hunyuan3D-Omni 补物体未观测面", "背面 novel view 可用，且与真实 point cloud/depth 不冲突。"],
        ["E3", "SuGaR/PGSR/2DGS mesh extraction 对比", "holes/free-space violation 降低；collision proxy 不封死可通行/可操作空间。"],
        ["E4", "OpenReal2Sim/Re3Sim-style Isaac adapter", "导出 GLB/USD/URDF/scene.json；Isaac camera RGB 与 collision body 坐标一致。"],
        ["E5", "Physical property schema", "小物体用 Scalable Real2Sim；大物体用 PhysX/PhysForge prior + 手工校验；mass/friction/joint 可追溯。"],
    ]
    reject_rows = [
        ["test", "reject condition"],
        ["visual consistency", "补齐视角在相邻 camera sweep 中出现跳变、结构漂移或 brightness hole。"],
        ["metric geometry", "生成 mesh 与已有 depth/point cloud reprojection error 过大。"],
        ["free space", "补全物体侵入已知可通行/可操作 free space。"],
        ["collision", "convex decomposition 后封死门口、桌下空间或生成不稳定 contact。"],
        ["object identity", "ObjectGS/Grouping 输出物体和背景/机器人 link 粘连。"],
        ["task utility", "Isaac rollout 的 collision rate、navigation/manipulation success 不升反降。"],
    ]
    return f"""# Final Report: Object-Centric Isaac Asset Reconstruction for Real2Sim

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
{top}

## 3. 新 Taxonomy：从视角补齐到物体资产
{md_table(family_rows)}

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
{md_table(experiment_rows)}

## 7. Reject Tests
{md_table(reject_rows)}

## 8. 对老师汇报时的简洁定位
本周调研需要表述为：我们在原先 directional view gap 的基础上，进一步对齐师兄交接中的 object-centric Isaac asset 目标，明确了后续主线不是“开放世界模型生成场景”，而是 **指定物体的双层资产生成**：3DGS 负责高保真视觉，mesh/collision/physics 负责 Isaac 可交互性。开放世界/3D 生成模型只作为受真实几何约束的补全先验。
"""


def write_matrix_index_final() -> None:
    files = {
        "object_asset_transfer_matrix.md": transfer_matrix_md(),
        "object_centric_isaac_asset_research_index.md": index_md(),
        "final_object_centric_isaac_asset_report.md": final_report_md(),
    }
    for name, md in files.items():
        path = NOTES / name
        path.write_text(md, encoding="utf-8")
        html_path = path.with_suffix(".html")
        html_path.write_text(simple_md_to_html(md, name[:-3]), encoding="utf-8")


def update_registry() -> None:
    existing: list[dict] = []
    if REGISTRY.exists():
        for line in REGISTRY.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    existing.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    new_ids = {e["id"] for e in ENTRIES}
    kept = [row for row in existing if row.get("id") not in new_ids]
    additions = []
    for e in ENTRIES:
        meta = e["repo_meta"]
        additions.append({
            "id": e["id"],
            "title": e["title"],
            "type": e["type"],
            "priority": e["priority"],
            "sources": e["sources"],
            "local_pdf": e["local_pdf"],
            "local_supplementary_pdfs": e.get("local_supplementary_pdfs", []),
            "local_repo": e["local_repo"],
            "commit": meta["commit"],
            "license": meta["license_file"],
            "status": "reviewed-object-centric",
            "note_paths": e["note_paths"],
            "review_depth": e["review_depth"],
            "score": e["score"],
            "research_thread": "object_centric_isaac_asset",
        })
    REGISTRY.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in kept + additions) + "\n",
        encoding="utf-8",
    )


def update_bib() -> None:
    items = [e["bib"].strip() for e in ENTRIES if e.get("bib", "").strip()]
    object_text = "\n\n".join(items) + "\n"
    OBJECT_BIB.write_text(object_text, encoding="utf-8")
    existing = BIB.read_text(encoding="utf-8") if BIB.exists() else ""
    marker = "\n% --- Object-centric Isaac asset supplement ---\n"
    base = existing.split(marker)[0].rstrip()
    BIB.write_text(base + marker + object_text, encoding="utf-8")


def main() -> None:
    enrich_entries()
    write_entry_reports()
    write_matrix_index_final()
    update_registry()
    update_bib()
    print(f"entries={len(ENTRIES)}")
    print(f"top={sorted(ENTRIES, key=lambda x: x['score'], reverse=True)[0]['title']}")


if __name__ == "__main__":
    main()
