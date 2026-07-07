# Server Codex Handoff: Object-Centric Isaac Sim Asset Experiments

更新时间：2026-07-04  
本地调研工作区：`D:\desktop\real2sim`  
目标服务器：RTX 5090 x 8，Docker + TurboVNC，Isaac Sim 5.0.0 GUI 已能通过远程桌面打开  
服务器项目目录名：`object2isaac_asset`  
服务器状态：尚未 clone 本轮 object-centric 相关项目；已有一部分前期 `r2s-habitat-gs` 使用过的实验数据

## 0. 给服务器 Codex 的最高优先级指令

你不是来直接开跑实验的。你的第一任务是和用户一起把服务器环境、已有数据、第一实验对象、repo clone 范围、输出目录和验收标准确认清楚。

在用户明确确认之前，不要执行以下操作：

- 不要开始长时间训练、重建、渲染或 batch conversion。
- 不要下载大模型权重、大数据集或多个大型 repo。
- 不要修改已有实验数据目录。

- 不要删除、覆盖或移动 `r2s-habitat-gs` 既有数据和输出。
- 不要假设 Isaac Sim 安装路径、Docker 容器名、数据路径或 Python 环境。

每一阶段开始前，先向用户汇报：

```text
我已经确认了什么？
还缺什么？
我准备执行哪些命令？
这些命令会写入哪些目录？
预计耗时和风险是什么？
是否需要用户确认？
```

如果某一步需要超过 30 分钟、占用多张 GPU、下载超过 5GB、或可能修改已有数据，必须先暂停并征得用户确认。

## 1. 项目任务重新定位

本项目当前主线不是简单的 scene-level novel view synthesis，也不是无约束 open world generation。根据本地文献调研和师兄早期交接，当前更准确的目标是：

> 给定真实采集的 RGB/RGB-D、camera poses、point cloud、depth、已有 3DGS 或相关重建结果，针对指定可交互物体生成 Isaac Sim 可用的 dual-layer asset：`3DGS visual layer + geometry/collision/physics layer`。

其中，directional view completion 仍然有价值，但它现在是子模块，负责补齐指定物体的未观测面、背面或大偏角视角，而不是总主线。

推荐的最小实验闭环是：

```text
已有真实数据 / 3DGS / point cloud
-> 选择一个简单指定物体
-> object extraction / object mask / object-only Gaussians
-> 3DGS-to-mesh 或 object mesh extraction
-> collision proxy / scale alignment
-> Isaac Sim import
-> RGB rendering + contact/collision validation
```

## 2. `object2isaac_asset` 项目目录组织

用户已在服务器创建 `object2isaac_asset` 项目目录。服务器 Codex 不需要再重新命名项目，也不要把实验文件散落到 home、Isaac Sim 安装目录或旧 `r2s-habitat-gs` 项目目录中。

服务器 Codex 启动后，第一步是定位这个目录的绝对路径，并把它记录为：

```bash
export PROJECT_ROOT=<absolute_path_to_object2isaac_asset>
```

如果用户已经在该目录中启动 Codex，可用：

```bash
pwd
export PROJECT_ROOT="$(pwd)"
```

如果尚未进入该目录，先让用户确认路径，不要猜。后续文档中的 `<PROJECT_ROOT>` 均指服务器上已经创建好的 `object2isaac_asset` 目录。

建议把项目目录组织为：

```text
object2isaac_asset/
  README_SERVER_STATE.md
  AGENTS.md
  env_logs/
    000_host_check.txt
    001_docker_check.txt
    002_isaac_check.txt
    003_python_cuda_check.txt
    010_repo_commits.txt
  notes/
    local_research/
      server_codex_handoff_isaac_object_asset.md
      final_object_centric_isaac_asset_report.md
      object_asset_transfer_matrix.md
      object_centric_isaac_asset_research_index.md
      source_registry.jsonl
      bibliography_object_asset.bib
    server_run_logs/
      000_startup_discussion.md
      001_environment_summary.md
      002_data_inventory.md
      003_first_object_decision.md
  repos/
    SuGaR/
    ObjectGS/
    OpenReal2Sim/
    gaussian-grouping/        # optional fallback, only after user confirms
    Re3Sim/                   # optional fallback, only after user confirms
  data/
    external_readonly/
      r2s_habitat_gs_link_or_manifest.txt
    selected_object_001/
      raw_views/
      masks/
      poses/
      point_cloud/
      gs_checkpoint/
      metadata/
  outputs/
    E0_isaac_import_smoke/
    E1_object_selection/
    E2_sugar_mesh_extraction/
    E3_isaac_collision_asset/
    E4_backside_completion_optional/
  scripts/
    inspect_environment.sh
    inspect_dataset.py
    isaac_import_smoke_test.py
  manifests/
    repo_manifest.tsv
    data_manifest.tsv
    experiment_manifest.tsv
```

各目录职责：

| path | 用途 | 规则 |
| --- | --- | --- |
| `<PROJECT_ROOT>/notes/local_research/` | 存放从本地拷贝来的调研结论和交接文件 | 只读参考，不在服务器上改写这些本地调研结论 |
| `<PROJECT_ROOT>/notes/server_run_logs/` | 存放服务器 Codex 每轮讨论、检查、实验的记录 | 每次关键操作后更新 |
| `<PROJECT_ROOT>/repos/` | clone 外部开源项目 | 每个 repo 单独目录，记录 commit hash，不把实验输出写进 repo 内 |
| `<PROJECT_ROOT>/data/external_readonly/` | 指向旧 `r2s-habitat-gs` 数据的只读说明、软链接或 manifest | 不复制大数据，除非用户确认 |
| `<PROJECT_ROOT>/data/selected_object_001/` | 第一轮简单对象的整理后输入 | 只放当前实验对象所需的最小子集 |
| `<PROJECT_ROOT>/outputs/` | 所有实验输出 | 按 E0-E4 分阶段保存，禁止覆盖旧输出 |
| `<PROJECT_ROOT>/scripts/` | 本项目自写的小工具脚本 | 不放第三方 repo 源码 |
| `<PROJECT_ROOT>/manifests/` | repo、数据、实验索引 | 便于回溯和汇报 |

服务器 Codex 应先创建空目录和日志文件，不要复制或移动已有数据。对已有 `r2s-habitat-gs` 数据只做只读检查，除非用户明确要求整理。

建议第一批目录初始化命令如下。执行前仍需向用户确认 `<PROJECT_ROOT>`：

```bash
cd <PROJECT_ROOT>
mkdir -p env_logs notes/local_research notes/server_run_logs repos \
  data/external_readonly data/selected_object_001/{raw_views,masks,poses,point_cloud,gs_checkpoint,metadata} \
  outputs/{E0_isaac_import_smoke,E1_object_selection,E2_sugar_mesh_extraction,E3_isaac_collision_asset,E4_backside_completion_optional} \
  scripts manifests
touch README_SERVER_STATE.md
touch manifests/repo_manifest.tsv manifests/data_manifest.tsv manifests/experiment_manifest.tsv
```

### 2.1 建议写入服务器项目根目录的 `AGENTS.md`

建议在 `<PROJECT_ROOT>/AGENTS.md` 写入以下内容，供服务器 Codex 每次启动时读取：

```markdown
# object2isaac_asset Workspace Instructions

Purpose: object-centric real2sim experiments for completing selected object views and generating Isaac Sim 5.0.0 interactive assets.

Core task:
- Build a minimal pipeline from real RGB/RGB-D / camera poses / point cloud / 3DGS to a selected object asset.
- Target output is a dual-layer Isaac asset: 3DGS or high-fidelity visual layer plus mesh/collision/physics layer.
- Directional view completion is a submodule for completing unseen object surfaces, not the first experiment.

Conversation-first rule:
- Do not start long training, large downloads, GPU-heavy jobs, or destructive file operations without user confirmation.
- Before each stage, report intended commands, write paths, expected runtime, and risks.

Folder rules:
- Keep external repos under repos/.
- Keep local research notes under notes/local_research/.
- Keep server run logs under notes/server_run_logs/.
- Keep raw external data read-only; use data/external_readonly/ for links/manifests.
- Put selected-object working data under data/selected_object_001/.
- Put experiment outputs under outputs/E*_*/.
- Record repo commits in manifests/repo_manifest.tsv.
- Record data sources in manifests/data_manifest.tsv.
- Record experiment commands/results in manifests/experiment_manifest.tsv.

First repo set:
- Default clone set: SuGaR, ObjectGS, OpenReal2Sim.
- Optional fallback only after user confirmation: gaussian-grouping, Re3Sim.
- Do not clone Hunyuan3D, GaussianObject, GSWorld, PGSR, 2DGS, Scalable Real2Sim, PhysX-3D, or PhysForge until the minimal pipeline is validated.

First experiment sequence:
1. Environment and Isaac import smoke test.
2. Data inventory of r2s-habitat-gs outputs.
3. Select one simple object.
4. Object extraction or existing mask validation.
5. SuGaR mesh extraction.
6. Isaac import with visual mesh and simple collision proxy.

Quality gates:
- Keep scale, pose, object identity, mesh quality, collision stability, and Isaac render output traceable.
- Do not accept generated/completed geometry that violates known depth, point cloud, or free space.
```

## 3. 本地 notes 如何放到服务器，以及 Codex 必读哪些文件

建议拷贝轻量 notes，不建议第一轮拷贝全部 PDF 和 repo。

理由：

- 服务器能联网，可以按需 clone repo。
- 第一轮实验主要需要本地调研结论和优先级，不需要服务器重新做文献调研。
- 拷贝全部 `ref/` 和 `repos/` 会占空间，也容易和服务器重新 clone 的 commit 混在一起。

### 3.1 推荐拷贝到服务器的位置

从本地 `D:\desktop\real2sim` 拷贝到服务器：

```text
<PROJECT_ROOT>/notes/local_research/
```

推荐文件布局：

```text
<PROJECT_ROOT>/notes/local_research/
  server_codex_handoff_isaac_object_asset.md
  final_object_centric_isaac_asset_report.md
  object_asset_transfer_matrix.md
  object_centric_isaac_asset_research_index.md
  source_registry.jsonl
  bibliography_object_asset.bib
  per_method/
    sugar_object_asset_object_asset_digest.md
    objectgs_object_asset_digest.md
    gaussian_grouping_object_asset_object_asset_digest.md
    openreal2sim_object_asset_object_asset_digest.md
    re3sim_object_asset_digest.md
```

本地对应源文件：

```text
D:\desktop\real2sim\notes\server_codex_handoff_isaac_object_asset.md
D:\desktop\real2sim\notes\final_object_centric_isaac_asset_report.md
D:\desktop\real2sim\notes\object_asset_transfer_matrix.md
D:\desktop\real2sim\notes\object_centric_isaac_asset_research_index.md
D:\desktop\real2sim\references\source_registry.jsonl
D:\desktop\real2sim\references\bibliography_object_asset.bib
D:\desktop\real2sim\notes\sugar_object_asset_object_asset_digest.md
D:\desktop\real2sim\notes\objectgs_object_asset_digest.md
D:\desktop\real2sim\notes\gaussian_grouping_object_asset_object_asset_digest.md
D:\desktop\real2sim\notes\openreal2sim_object_asset_object_asset_digest.md
D:\desktop\real2sim\notes\re3sim_object_asset_digest.md
```

如果不想建 `per_method/` 子目录，也可以全部平铺在 `notes/local_research/`。但服务器 Codex 必须知道这些是本地调研资料，不是服务器实验输出。

### 3.2 服务器 Codex 必读文件顺序

服务器 Codex 在做任何环境安装、clone 或实验前，必须先读：

1. `<PROJECT_ROOT>/notes/local_research/server_codex_handoff_isaac_object_asset.md`  
   作用：了解服务器实验行为准则、目录结构、讨论优先约束和第一阶段实验路线。

2. `<PROJECT_ROOT>/notes/local_research/final_object_centric_isaac_asset_report.md`  
   作用：了解为什么主线是 object-centric Isaac asset，而不是泛化 world model 或 scene-level view completion。

3. `<PROJECT_ROOT>/notes/local_research/object_asset_transfer_matrix.md`  
   作用：了解各方法的输入、输出、Isaac path、风险和优先级。

4. `<PROJECT_ROOT>/notes/local_research/object_centric_isaac_asset_research_index.md`  
   作用：了解本地已调研条目和阅读深度，避免重复调研。

5. `<PROJECT_ROOT>/notes/local_research/source_registry.jsonl`  
   作用：核对 repo URL、PDF、本地笔记、priority、score 和本地 commit 参考。

然后按当前阶段读 per-method digest：

| 当前阶段 | 必读 digest |
| --- | --- |
| 准备 clone / 安装 SuGaR | `per_method/sugar_object_asset_object_asset_digest.md` |
| 准备 object extraction | `per_method/objectgs_object_asset_digest.md` |
| ObjectGS 不适配或需要 fallback | `per_method/gaussian_grouping_object_asset_object_asset_digest.md` |
| 准备 Isaac/asset organization | `per_method/openreal2sim_object_asset_object_asset_digest.md` |
| OpenReal2Sim 不适配或需要 IsaacLab 参考 | `per_method/re3sim_object_asset_digest.md` |

### 3.3 是否需要拷贝 PDF

默认不需要。服务器 Codex 可以先依靠 notes 和 repo README 推进实验。

如果用户希望服务器 Codex 离线查看论文，再额外拷贝少量 PDF 到：

```text
<PROJECT_ROOT>/notes/local_research/papers/
```

建议只拷贝：

```text
ref/sugar_2311_12775.pdf
ref/objectgs_2507_15454.pdf
ref/gaussian_grouping_2312_00732.pdf
ref/re3sim_2502_08645.pdf
```

不要一开始拷贝所有 `ref/`、`repos/` 和生成文件。

## 4. 服务器 Codex 启动后第一轮对话要问用户的问题

服务器 Codex 启动后，先问用户以下问题，并等待回答：

1. 我现在是否已经位于服务器上的 `object2isaac_asset` 项目目录？如果不是，请提供该目录的绝对路径，我会设置为 `<PROJECT_ROOT>`。
2. 是否已经把本地 notes 拷贝到 `<PROJECT_ROOT>/notes/local_research/`？如果还没有，是否需要我先等待你上传？
3. Isaac Sim 5.0.0 当前是宿主机安装，还是主要在 Docker 容器内运行？常用启动命令是什么？
4. 前期 `r2s-habitat-gs` 数据位于哪个目录？是否允许只读访问？是否允许在 `<PROJECT_ROOT>/data/external_readonly/` 放软链接或 manifest？
5. 已有数据包括哪些内容：RGB、depth、camera poses、COLMAP、point cloud、3DGS checkpoint、mesh、mask？
6. 第一实验对象选择哪个简单物体？若用户还没定，先选一个刚体小物体或椅子/桌子局部，不要直接从门/门把手开始。
7. 本轮是否允许 clone 第一批 3 个 repo 到 `<PROJECT_ROOT>/repos/`：`SuGaR`、`ObjectGS`、`OpenReal2Sim`？
8. 如果 `ObjectGS` 安装失败，是否允许改用 `Gaussian Grouping` 作为 object extraction fallback？
9. 本轮是否禁止下载大模型权重？默认禁止，除非用户明确同意。

只有得到用户确认后，才进入环境检查和配置检查。

## 5. 环境检查阶段

目标：确认宿主机、Docker、GPU、Isaac Sim、Python/CUDA 环境是否满足最小实验。此阶段不安装复杂依赖，不 clone repo，不跑训练。

### 5.1 宿主机检查

建议执行并保存到 `env_logs/000_host_check.txt`：

```bash
set -x
date
hostname
whoami
pwd
uname -a
lsb_release -a || cat /etc/os-release
df -h
free -h
ulimit -a
echo "DISPLAY=$DISPLAY"
echo "XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR"
```

GPU 检查：

```bash
nvidia-smi
nvidia-smi -L
nvidia-smi --query-gpu=index,name,memory.total,driver_version --format=csv
```

注意：RTX 5090 对老版本 PyTorch、CUDA extension、3DGS CUDA kernels 可能不友好。不要直接复用老项目的旧 torch wheel。后续安装前必须确认 PyTorch/CUDA 支持当前 GPU 和驱动。

### 5.2 Docker 检查

保存到 `env_logs/001_docker_check.txt`：

```bash
docker --version
docker compose version || true
docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}"
```

如果 Isaac Sim 在容器里运行，继续检查：

```bash
docker exec -it <container_name> bash -lc "pwd && whoami && nvidia-smi && python3 --version"
```

不要猜容器名。先让用户确认或从 `docker ps` 中识别后汇报。

### 5.3 Isaac Sim 检查

用户已确认 Isaac Sim 5.0.0 GUI 可通过 TurboVNC 打开。服务器 Codex 仍需确认脚本路径和 Python API。

先定位 Isaac Sim 安装路径：

```bash
find / -maxdepth 4 \( -name "isaac-sim.sh" -o -name "python.sh" -o -name "isaacsim" \) 2>/dev/null | head -50
```

常见路径可能类似：

```text
/isaac-sim
/opt/nvidia/isaac-sim
~/isaacsim
```

找到后保存：

```bash
cd <ISAAC_SIM_ROOT>
ls -lah
./python.sh -c "import sys; print(sys.version)"
./python.sh -c "import carb; import omni; print('isaac python import ok')"
```

如需 headless smoke test，先向用户确认，再尝试短时运行：

```bash
cd <ISAAC_SIM_ROOT>
timeout 90 ./isaac-sim.sh --no-window --/app/quitAfter=60
```

如果 GUI 已开着，不要随意启动第二个重型 Isaac 实例。先问用户当前实例是否可以关闭或是否使用 headless 检查。

### 5.4 Python / CUDA / PyTorch 检查

不要直接污染系统 Python。先确认服务器已有 conda/mamba/venv 状态：

```bash
which python3
python3 --version
which conda || true
conda env list || true
which nvcc || true
nvcc --version || true
```

如果已有项目环境，先只读检查：

```bash
python3 - <<'PY'
import sys
print("python", sys.version)
try:
    import torch
    print("torch", torch.__version__)
    print("cuda", torch.version.cuda)
    print("available", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("device", torch.cuda.get_device_name(0))
except Exception as e:
    print("torch import failed:", repr(e))
PY
```

服务器 Codex 应把检查结果汇报给用户，并给出是否建议新建独立环境。不要直接安装。

## 6. 数据检查阶段

目标：识别已有 `r2s-habitat-gs` 数据能否支持 object-centric 实验。

服务器 Codex 应向用户确认前期数据目录，然后只读检查：

```bash
find <DATA_ROOT> -maxdepth 3 -type f | sed 's#^#/#' | head -200
find <DATA_ROOT> -maxdepth 3 -type d | head -100
du -sh <DATA_ROOT>
```

重点寻找：

```text
RGB images: images/, rgb/, color/
Depth: depth/, depths/, depth_png/
Camera poses: transforms.json, cameras.json, poses.txt, COLMAP sparse/
COLMAP: sparse/0/cameras.bin, images.bin, points3D.bin
Point cloud: .ply, .pcd, .npz
3DGS checkpoint: point_cloud/iteration_*/point_cloud.ply, cfg_args, cameras.json
Mesh: .obj, .ply, .glb, .usd, .usda
Masks: masks/, sam_masks/, object_masks/
Previous diagnostics: black frame logs, trajectory renderings, A* views
```

建议生成一个只读 inventory：

```bash
python3 - <<'PY'
from pathlib import Path
root = Path("<DATA_ROOT>")
exts = [".png", ".jpg", ".jpeg", ".json", ".txt", ".bin", ".ply", ".pcd", ".obj", ".glb", ".usd", ".usda", ".npz", ".pt", ".pth"]
counts = {}
for p in root.rglob("*"):
    if p.is_file():
        counts[p.suffix.lower()] = counts.get(p.suffix.lower(), 0) + 1
print("root:", root)
for k, v in sorted(counts.items()):
    if k in exts or v > 10:
        print(k or "<no_ext>", v)
PY
```

数据检查后必须向用户汇报：

```text
我找到了哪些可用输入？
是否已有 object masks？
是否已有 3DGS checkpoint？
是否已有 COLMAP poses？
是否已有 depth/point cloud？
是否可以先做 SuGaR mesh extraction？
第一实验对象建议是什么？
```

## 7. 第一批 repo clone 策略

不要一次 clone 很多项目。第一批默认只 clone 3 个 repo：

| repo | URL | 作用 | 为什么第一批需要 |
| --- | --- | --- | --- |
| SuGaR | `https://github.com/Anttwo/SuGaR` | 3DGS-to-mesh / surface extraction | 没有 mesh，就很难做 Isaac collision proxy。 |
| ObjectGS | `https://github.com/RuijieZhu94/ObjectGS` | object-aware Gaussian reconstruction / instance extraction | 用于从整场景中分离指定物体。若已有高质量 masks，可降低优先级。 |
| OpenReal2Sim | `https://github.com/IntelLabs/OpenReal2Sim` | real2sim toolbox / GLB scene.json USD conversion | 参考 Isaac/IsaacLab asset organization 和 exporter 思路。 |

可选 fallback，只有在用户确认后 clone：

| repo | URL | 使用条件 |
| --- | --- | --- |
| Gaussian Grouping | `https://github.com/lkeab/gaussian-grouping` | 如果 ObjectGS 环境难装、数据格式不适配，或只需要较快 object grouping baseline。 |
| Re3Sim | `https://github.com/InternRobotics/Re3Sim` | 如果 OpenReal2Sim 不适合当前 Isaac 5.0.0 环境，或需要 IsaacLab manipulation-style pipeline 参考。 |

暂不 clone：

```text
GaussianObject
Hunyuan3D-2.1 / Hunyuan3D-Omni
GSWorld
PGSR / 2DGS
Scalable Real2Sim
PhysX-3D / PhysForge
InstantMesh / TripoSR / CRM / LGM / Wonder3D
```

这些不是不重要，而是不应在第一天把环境复杂度拉满。等最小闭环跑通后再逐个引入。

### 7.1 clone 命令模板

所有开源项目都 clone 到：

```text
<PROJECT_ROOT>/repos/
```

不要 clone 到 Isaac Sim 安装目录、旧 `r2s-habitat-gs` 目录、home 根目录或 `notes/` 目录。`notes/` 只放调研资料和实验记录，`repos/` 只放第三方源码。

在用户确认 clone 范围后执行：

```bash
export PROJECT_ROOT=<absolute_path_to_object2isaac_asset>
mkdir -p "$PROJECT_ROOT/repos"
cd "$PROJECT_ROOT/repos"

git clone --depth 1 https://github.com/Anttwo/SuGaR.git
git clone --depth 1 https://github.com/RuijieZhu94/ObjectGS.git
git clone --depth 1 https://github.com/IntelLabs/OpenReal2Sim.git
```

记录 commit：

```bash
mkdir -p "$PROJECT_ROOT/env_logs" "$PROJECT_ROOT/manifests"
for d in SuGaR ObjectGS OpenReal2Sim; do
  echo "==== $d ===="
  git -C "$d" remote -v
  git -C "$d" rev-parse HEAD
  git -C "$d" status --short
done | tee "$PROJECT_ROOT/env_logs/010_repo_commits.txt"
```

同时写入 `<PROJECT_ROOT>/manifests/repo_manifest.tsv`：

```bash
{
  echo -e "name\turl\tcommit\tlocal_path\trole\tstatus"
  for d in SuGaR ObjectGS OpenReal2Sim; do
    url="$(git -C "$PROJECT_ROOT/repos/$d" remote get-url origin)"
    commit="$(git -C "$PROJECT_ROOT/repos/$d" rev-parse HEAD)"
    case "$d" in
      SuGaR) role="3DGS-to-mesh / surface extraction" ;;
      ObjectGS) role="object extraction / object-aware Gaussian reconstruction" ;;
      OpenReal2Sim) role="Isaac asset organization / GLB scene.json USD conversion reference" ;;
    esac
    echo -e "$d\t$url\t$commit\t$PROJECT_ROOT/repos/$d\t$role\tcloned"
  done
} > "$PROJECT_ROOT/manifests/repo_manifest.tsv"
```

如果 clone 可选 fallback：

```bash
export PROJECT_ROOT=<absolute_path_to_object2isaac_asset>
cd "$PROJECT_ROOT/repos"
git clone --depth 1 https://github.com/lkeab/gaussian-grouping.git
git clone --depth 1 https://github.com/InternRobotics/Re3Sim.git
```

fallback repo 也必须追加到 `repo_manifest.tsv`，并在 `status` 中标注 `fallback-cloned-after-user-confirmation`。

## 8. 安装策略

不要把所有 repo 装到一个环境里。3DGS/SuGaR/ObjectGS 可能都有 CUDA extension，依赖容易冲突。

建议策略：

```text
env_sugar      -> SuGaR mesh extraction
env_objectgs   -> ObjectGS / object extraction
env_adapter    -> OpenReal2Sim / Isaac asset conversion scripts
Isaac Python   -> 只用于 Isaac Sim API/import smoke test，不随意 pip install 外部重包
```

安装前必须先读每个 repo 的 README / install scripts，并向用户汇报：

```text
repo 需要的 Python 版本
repo 需要的 CUDA/PyTorch 版本
是否需要编译 CUDA extension
是否支持当前 RTX 5090
是否需要下载权重或 demo data
预计占用空间
```

如果 README 要求旧版 torch 或旧 CUDA，先不要安装，先评估是否需要 patch 或使用容器隔离。

## 9. 第一阶段实验：不做生成补全的最小闭环

目标：先证明真实观测能否生成一个可导入 Isaac 的指定物体资产。不要一开始做 Hunyuan3D 或 GaussianObject。

### 9.1 输入要求

最小输入之一：

```text
方案 A：已有 3DGS checkpoint + camera poses + images
方案 B：COLMAP posed images，可先训练/复用 3DGS 后再 SuGaR
方案 C：已有 object mesh / point cloud，可先绕过 object extraction 做 Isaac import smoke test
```

如果没有 object mask：

```text
先尝试 ObjectGS 或 Gaussian Grouping
```

如果已有 object mask：

```text
先跳过 ObjectGS，直接 object crop / object-only reconstruction / SuGaR mesh extraction
```

### 9.2 实验 E0：已有资产导入 Isaac smoke test

目的：先验证 Isaac import path，不要被上游重建问题卡住。

输入可以是已有 `.obj`、`.ply`、`.glb`、`.usd` 中任意一个简单资产。

检查项：

```text
能否导入 Isaac stage
尺度是否合理
坐标轴是否正确
材质是否可见
是否能添加简单 collision
是否能用 Isaac camera 渲染一张 RGB
```

输出：

```text
outputs/000_smoke_tests/import_test.usd
outputs/000_smoke_tests/render_rgb.png
outputs/000_smoke_tests/import_log.txt
```

若这个测试失败，先修 Isaac/import path，不要继续上游重建。

### 9.3 实验 E1：指定物体分离

目的：从已有场景数据中得到 object-level visual subset。

优先路线：

```text
已有 masks -> 直接使用
无 masks -> ObjectGS
ObjectGS 不适配 -> Gaussian Grouping fallback
```

输出：

```text
outputs/001_object_selection/object_masks/
outputs/001_object_selection/object_only_views/
outputs/001_object_selection/object_selection_report.md
```

验收标准：

```text
物体边界不明显粘连背景
物体主要可见面被覆盖
不要包含机器人 link / 地面 / 墙面
能回溯到原始 camera poses
```

### 9.4 实验 E2：SuGaR mesh extraction

目的：从 3DGS 或 posed images 得到 object mesh / scene mesh。

执行前确认：

```text
SuGaR 是否需要 vanilla 3DGS checkpoint
输入格式是否能从 r2s-habitat-gs 数据转换
是否已有 COLMAP sparse
是否需要先跑原始 3DGS training
```

输出：

```text
outputs/002_mesh_extraction/object_mesh_raw.ply
outputs/002_mesh_extraction/object_mesh_cleaned.obj
outputs/002_mesh_extraction/mesh_extraction_report.md
```

验收标准：

```text
mesh 能打开
尺度可解释
没有灾难性 holes / floaters
主要表面和真实 RGB-D/point cloud 一致
能进一步简化为 collision proxy
```

### 9.5 实验 E3：Isaac import + collision proxy

目的：把 mesh 变成 Isaac 可交互资产的第一版。

可以先使用简单 collision：

```text
bounding box
convex hull
VHACD / convex decomposition
manual simplified collision mesh
```

输出：

```text
outputs/003_isaac_import/object_asset.usd
outputs/003_isaac_import/object_visual_mesh.*
outputs/003_isaac_import/object_collision_mesh.*
outputs/003_isaac_import/isaac_render_rgb.png
outputs/003_isaac_import/isaac_collision_test_log.txt
```

验收标准：

```text
Isaac 中可见
位置和尺度合理
collision body 与 visual mesh 基本对齐
简单刚体或机器人接触不发生明显穿模/爆炸
camera RGB 可渲染
```

## 10. 第二阶段：物体未观测面补齐

只有当第一阶段闭环完成后，才进入第二阶段。

优先候选：

```text
GaussianObject -> sparse-view object 3DGS / backside completion
Hunyuan3D-2.1 / Hunyuan3D-Omni -> image-to-3D / controlled mesh prior
PGSR / 2DGS -> SuGaR 后端对照
```

进入第二阶段前，服务器 Codex 需要先和用户确认：

```text
是否允许下载模型权重？
是否有足够空间？
是否要把生成式补全限制在 bbox / scale / point cloud 内？
如何做 reject tests？
```

不要让生成式模型直接替换真实资产。它只能作为低覆盖面或背面的 candidate prior，必须经过 depth/point cloud/free-space/collision 检查。

## 11. Reject Tests

每个资产都要过以下检查。任何一项明显失败，都应暂停并向用户汇报。

| test | reject condition |
| --- | --- |
| visual consistency | novel view 或 Isaac render 出现明显黑洞、漂移、纹理错乱 |
| object identity | object mask / object-only Gaussians 粘连背景、地面、墙、机器人 link |
| metric geometry | mesh 和已有 depth / point cloud reprojection error 过大 |
| free space | 补全或 mesh 侵入已知可通行/可操作 free space |
| collision | collision proxy 封死通道、穿模、接触爆炸或与 visual mesh 严重不对齐 |
| scale | 物体尺寸与真实尺度、Go2/机械臂尺度或场景尺度明显不符 |
| task utility | Isaac 中渲染或交互变差，不能服务导航/交互实验 |

## 12. 服务器 Codex 每次实验必须记录的内容

每个实验创建一个 `experiment_log.md`，至少包括：

```text
日期时间
执行人 / Codex session
服务器 hostname
GPU 状态
repo URL and commit hash
conda/venv 名称
Python / torch / CUDA 版本
输入数据路径
输出路径
实际执行命令
运行耗时
关键 stdout/stderr
生成文件列表
截图或 render 输出
是否通过验收标准
失败原因和下一步建议
```

建议实验编号：

```text
E0_isaac_import_smoke
E1_object_selection
E2_sugar_mesh_extraction
E3_isaac_collision_asset
E4_backside_completion_optional
```

## 13. 常见风险和处理方式

### 13.1 RTX 5090 / CUDA extension 不兼容

症状：

```text
no kernel image is available for execution on the device
unsupported gpu architecture
torch cuda is not available
CUDA extension build failed
```

处理：

```text
不要反复盲装。
记录 torch/cuda/nvcc/driver。
检查 repo 的 setup.py / CMakeLists / CUDA arch flags。
向用户汇报是否需要新 PyTorch、源码编译或容器隔离。
```

### 13.2 Isaac Python 和普通 Python 混用

不要把所有 pip 包塞进 Isaac Python。Isaac Python 用于 Isaac API 和 USD import smoke test；3DGS/SuGaR/ObjectGS 使用独立 conda/venv。

### 13.3 数据格式不清楚

不要猜。先生成 inventory，再让用户确认哪个目录是 RGB、poses、3DGS checkpoint、COLMAP、point cloud。

### 13.4 repo 安装链条太长

第一轮目标是最小闭环，不是完美复现所有论文。若 ObjectGS 卡住，可以用已有 masks 或 Gaussian Grouping fallback；若 OpenReal2Sim 不适配，可以先用 Isaac 原生 USD/mesh import smoke test。

### 13.5 生成式模型诱惑

不要一开始上 Hunyuan3D/GaussianObject。先得到真实观测驱动的 baseline，再用生成式方法补背面。否则无法判断生成内容是否真的改善 real2sim。

## 14. 建议服务器 Codex 第一条回复模板

服务器 Codex 接到本交接文档后，可以这样回复用户：

```text
我会先做讨论和只读检查，不会直接开始训练或下载大模型。

我需要先确认 6 件事：
1. 我现在是否已经位于服务器上的 object2isaac_asset 项目目录？如果不是，请提供该目录绝对路径。
2. 本地调研 notes 是否已经上传到 <PROJECT_ROOT>/notes/local_research/？
3. r2s-habitat-gs 既有数据目录在哪里？我是否可以只读检查？
4. Isaac Sim 5.0.0 的常用启动方式是在宿主机还是容器内？当前是否已有 GUI 实例在运行？
5. 第一轮简单对象是否已有候选？如果没有，我会先根据数据 inventory 建议一个。
6. 第一批是否允许 clone 3 个 repo 到 <PROJECT_ROOT>/repos/：SuGaR、ObjectGS、OpenReal2Sim？

确认后，我会先输出环境检查日志和数据 inventory，再向你建议第一轮实验命令。
```

## 15. 建议第一周目标

不要把第一周目标定为“完整复现某篇论文”。更合适的目标是：

```text
目标 1：完成服务器环境和 Isaac import smoke test。
目标 2：确认 r2s-habitat-gs 数据中一个可用于 object-centric 实验的简单物体。
目标 3：完成 object selection 或确认已有 mask 可用。
目标 4：完成 SuGaR mesh extraction 或明确数据格式缺口。
目标 5：把一个 visual mesh + simple collision proxy 导入 Isaac Sim 5.0.0，并保存 render/collision 测试结果。
```

如果这 5 个目标完成，后续再进入：

```text
GaussianObject / Hunyuan3D object backside completion
PGSR / 2DGS geometry backend comparison
Scalable Real2Sim physical parameter estimation
GSWorld-style full asset contract
```

## 16. 与本地调研产物的对应关系

本交接文档基于本地以下结论：

```text
notes/final_object_centric_isaac_asset_report.md
notes/object_asset_transfer_matrix.md
notes/object_centric_isaac_asset_research_index.md
references/source_registry.jsonl
```

核心排序：

```text
1. GSWorld: 系统设计锚点，不建议第一天完整复现
2. Re3Sim: Isaac/IsaacLab integration 参考，可作为 OpenReal2Sim fallback
3. SuGaR: 第一阶段 mesh extraction 必需后端
4. Scalable Real2Sim: 第二阶段 physical parameter estimation 参考
5. OpenReal2Sim: 第一阶段 Isaac exporter / scene organization 参考
6. ObjectGS: 第一阶段 object selection / object-aware Gaussian 工具
7. GaussianObject: 第二阶段 object backside completion
```

第一阶段只 clone 3 个 repo，是为了让服务器实验从小闭环开始，而不是把调研目录机械搬运到服务器。
