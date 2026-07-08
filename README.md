# Real2Sim Literature Workspace

This repository is a literature and source-tracking workspace for a Real2Sim research project. The current focus is **object-centric Isaac asset reconstruction**: turning real observations of target objects into simulator-ready assets with both a photorealistic visual layer and a geometry/collision/physics layer.

本项目的主要输出不是代码实现，而是可复用的论文调研资产：PDF、结构化阅读笔记、技术路线矩阵、source registry 和阶段性综合报告。

## Current Research Question

Given single-view or multi-view RGB/RGB-D observations, camera poses, point clouds, depth maps or 3D Gaussian Splatting representations, how can we generate an Isaac Sim / IsaacLab-ready asset for a specified interactive object?

The target asset is treated as a dual-layer object:

```text
target object
-> object identity / segmentation
-> object view or backside completion
-> 3DGS visual layer
-> mesh / geometry extraction
-> collision proxy and physical parameters
-> Isaac Sim / IsaacLab import and validation
```

The older **directional view completion** thread is still useful, but it is now treated as a subproblem: completing unseen object backsides or large-angle views before geometry and collision export.

## Repository Layout

```text
real2sim/
├── AGENTS.md
├── README.md
├── notes/
├── ref/
└── references/
```

### `AGENTS.md`

Workspace rules for Codex / LLM agents. Read this before asking an agent to add papers, write digests, or update reports.

### `notes/`

Human-readable research notes.

Common file types:

- `*_digest.md`: structured paper or project digest.
- `*.html`: standalone browser-openable note.
- `final_object_centric_isaac_asset_report.md`: current main synthesis report.
- `object_centric_isaac_asset_research_index.md`: ranked index for the object-centric Isaac asset thread.
- `object_asset_transfer_matrix.md`: method-to-pipeline transfer matrix.
- `final_directional_view_completion_report.md`: earlier directional view completion synthesis, now a submodule reference.

### `ref/`

Local PDFs and downloaded paper files. Many files are large, and this directory dominates repository size.

### `references/`

Machine-readable support files:

- `source_registry.jsonl`: source registry mapping papers/projects to URLs, local PDFs, repos, commits, licenses and note paths.
- `paper_index.jsonl`: local paper index.
- `bibliography*.bib`: verified bibliography metadata.
- `extracted_text/`: extracted text from PDFs for local search and claim checking.
- `build_*_reports.py`: scripts used to build report-style outputs from the registry and notes.

## Recommended Entry Points

Start here:

1. `notes/final_object_centric_isaac_asset_report.md`
2. `notes/object_centric_isaac_asset_research_index.md`
3. `notes/object_asset_transfer_matrix.md`
4. `notes/final_directional_view_completion_report.md`
5. `references/source_registry.jsonl`

For agent behavior and workspace conventions, read:

1. `AGENTS.md`
2. this `README.md`

## Current Mainline

The current project direction is:

```text
ObjectGS / Gaussian Grouping / SAGA
-> GaussianObject / Hunyuan3D-style object completion
-> GSWorld / object-level 3DGS visual asset
-> SuGaR / PGSR / 2DGS geometry extraction
-> Scalable Real2Sim / PhysX-style physical parameters
-> Re3Sim / OpenReal2Sim / IsaacLab integration
```

High-priority anchor papers and projects:

- **GSWorld**: system-level asset contract for photorealistic real2sim simulation.
- **Re3Sim**: IsaacLab integration baseline.
- **SuGaR**: 3DGS-to-mesh geometry backend.
- **Scalable Real2Sim**: collision geometry and physical parameter reference.
- **ObjectGS**: object identity and object-aware Gaussian reconstruction.
- **GaussianObject**: sparse-view object completion and missing-surface repair.
- **OpenReal2Sim**: simulator export and real-to-sim toolbox reference.
- **PGSR / 2DGS**: surface-aware Gaussian geometry backends.

## Research Taxonomy

| Layer | Role | Representative methods |
|---|---|---|
| Object selection | Extract the target object from a scene-level representation. | ObjectGS, Gaussian Grouping, SAGA |
| Object view / backside completion | Fill unseen object surfaces or reverse-yaw views. | GaussianObject, Hunyuan3D-Omni, InstantMesh, CRM |
| Visual layer | Preserve photorealistic observation. | GSWorld, ObjectGS, 3DGS variants |
| Geometry / collision layer | Produce mesh and collision candidates. | SuGaR, PGSR, 2DGS, GSDF |
| Simulator integration | Import and validate assets in Isaac Sim / IsaacLab. | Re3Sim, OpenReal2Sim, GSWorld |
| Physical semantics | Estimate mass, inertia, material, affordance or parts. | Scalable Real2Sim, PhysX-3D, PhysForge, Hunyuan3D-Part |

## How To Work In This Repository

### Add a new paper

1. Put the PDF in `ref/`.
2. Add or update one registry entry in `references/source_registry.jsonl`.
3. Add bibliography metadata to `references/bibliography.bib` or `references/bibliography_object_asset.bib` only when verified.
4. Create a Markdown digest in `notes/`.
5. Optionally create a standalone HTML note in `notes/`.
6. If the paper changes the ranking or taxonomy, update the relevant index/report files.

### Write a useful digest

Each digest should prioritize implementation-relevant details:

- problem and why it matters for Real2Sim
- inputs and outputs
- method pipeline
- intermediate representations
- assumptions and failure modes
- Isaac Sim / IsaacLab transfer relevance
- whether the paper helps object identity, completion, visual rendering, mesh extraction, collision, physics or validation

### Search locally

Useful examples:

```powershell
rg "Isaac" notes references
rg "collision" notes references
rg "GaussianObject|ObjectGS|SuGaR|Re3Sim|GSWorld" notes references
```

## Git And Upload Policy

Only the collaboration-critical literature workspace should be uploaded.

Tracked / uploadable:

- `README.md`
- `AGENTS.md`
- `notes/`
- `ref/`
- `references/`

Local-only:

- `repos/`
- root scratch files such as drafts, screenshots, handoff images or temporary notes
- downloaded code repositories, model weights and experiment artifacts unless explicitly approved

Important: `ref/` contains many PDFs and the first push can be slow. This is expected because the tracked data is close to 1 GB even though the folder looks small by file count. Keep the GitHub repository private unless paper redistribution rights are explicitly checked.

## Collaboration Notes

- Treat `notes/final_object_centric_isaac_asset_report.md` as the current main report.
- Treat `notes/final_directional_view_completion_report.md` as historical context and a submodule reference.
- Do not overwrite source PDFs or downloaded references unless intentionally replacing bad data.
- Do not make ungrounded claims about a paper. If a conclusion is inferred across papers, mark it as an inference.
- For future work, the most valuable next additions are Isaac validation protocol notes, visual-collision alignment checks and object-level physical parameter provenance.

