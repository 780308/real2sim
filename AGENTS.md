# Real2Sim Literature Workspace

Purpose: research directional view completion for a Go2 real2sim pipeline that will move from Habitat-GS diagnostics toward Isaac Sim assets.

Folder rules:
- Keep existing PDFs and downloaded papers in `ref/`.
- Clone project repositories under `repos/` with shallow clones when possible.
- Write per-paper/project notes under `notes/`; put note assets under `notes/assets/`.
- Use `references/source_registry.jsonl` for source tracking and `references/bibliography.bib` only for verified metadata.

Reading priorities:
- Focus on implementable method pipelines: inputs, outputs, intermediate representations, losses/objectives, training/inference flow, assumptions, and failure modes.
- Always judge relevance to the directional view coverage gap: large-angle/reverse-yaw novel view completion anchored to real RGB/RGB-D, poses, 3DGS, point cloud, or depth.
- Always judge Isaac Sim transfer: visual-only, adapter needed, direct geometry/USD/collision path, or not suitable.
- Do not re-research Vid2Sim, Habitat-GS, or ReaDy-Go; use existing notes only as context.

Output contract:
- Use Chinese notes with key technical terms in English.
- For each selected paper/project, create one Markdown digest and one standalone HTML note.
- Final outputs must include a transfer matrix and a synthesis report with ranked recommendations.
