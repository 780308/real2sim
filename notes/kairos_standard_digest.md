# Kairos: Native World Model Stack for Physical AI

优先级：**P1** | 阅读深度：**standard** | 类别：**general physical-AI world model stack** | 综合分：**2.7/5**

## 资料状态
- 类型：paper+repo+weights
- 本地 PDF：ref/kairos_2606_16533.pdf
- 本地 repo：repos/kairos-sensenova
- commit：40d3fcb
- license 文件：LICENSE
- Sources:
- https://github.com/kairos-agi/kairos-sensenova
- https://huggingface.co/collections/kairos-agi/kairos30
- https://arxiv.org/abs/2606.16533

## 对 directional view coverage gap 的定位
P1 低位。作为 long-term world prior，不作为近期解决方案。

## Inputs / Outputs
- Inputs：open-world videos, human behavior data, robot interactions。
- Outputs：video/world-model predictions for physical AI reasoning and robot tasks。

## Method Pipeline
- Native pre-training paradigm + cross-embodiment data curriculum。
- README 提供 multiple model weights for robot/general generation。

## Objectives / Losses
large world model pretraining and downstream task objectives。

## Assumptions
范围太大，不是针对 view completion；资料多但工程迁移路径不短。

## Failure Modes
可能给出漂亮预测但不 metric align；无 direct Isaac asset。

## Isaac Sim / 平台迁移判断
visual/model prior only。

## Transfer Matrix 摘要
| Dimension | Judgment |
|---|---|
| method family | general physical-AI world model stack |
| camera-pose conditioning | 中/弱 |
| large-angle support | 需验证 |
| 3D consistency | 3.2/5 |
| Isaac Sim path | visual/model prior only。 |
| code/weights | 3.5/5 |
| priority score | 2.7/5 |
