---
name: open-montage
description: >-
  OpenMontage 代理化视频制作：流水线驱动、阶段导演 skill、工具注册表。
  用户提到做视频、剪辑、解说、动画、Seedance、Remotion、OpenMontage 时使用。
  必须先读 AGENT_GUIDE.md，所有制作走 pipeline_defs/ 流水线。
---

# OpenMontage · 入口

> **源码目录**：`AI工具/OpenMontage/`  
> **契约（必读）**：[`AGENT_GUIDE.md`](../../AI工具/OpenMontage/AGENT_GUIDE.md)  
> **项目上下文**：[`PROJECT_CONTEXT.md`](../../AI工具/OpenMontage/PROJECT_CONTEXT.md)  
> **Layer 3 工具 skill**：`.cursor/skills/<tool-name>/`（junction → `OpenMontage/.agents/skills/`）

## 硬规则

1. **任何视频制作请求必须先读 `AGENT_GUIDE.md`**，再选流水线
2. **禁止跳过 pipeline**：读 `pipeline_defs/<name>.yaml` + 各阶段 `skills/pipelines/<name>/*-director.md`
3. **调用工具前**读对应 Layer 3 skill（本目录下 remotion、seedance-2-0、ffmpeg 等）
4. **preflight**：`tools.tool_registry` 发现可用工具后再报价/执行

## 快速路径

| 用户意图 | 先读 |
| --- | --- |
| 写 / 改 AI 生视频提示词 | 同上 skill 链 + **交付块全中文** + **无【】小标题** + **语速仅 `[H]`** + **强哥口播必四川话** + **每轨单独粘贴自洽** + **续拍以图为准** + **handheld 空间/运镜自检**（见 `.cursor/rules/open-montage-video-prompts.mdc` § 交付块逻辑自检 · § 强哥口播 · 四川话铁律） |
| 模糊探索 / 第一次用 | `AI工具/OpenMontage/skills/meta/onboarding.md` |
| 参考视频复刻 | `AI工具/OpenMontage/skills/meta/video-reference-analyst.md` |
| 具体片型 | `AI工具/OpenMontage/pipeline_defs/` 匹配流水线 |

## 环境

```powershell
cd AI工具/OpenMontage
make setup   # 或见 README_zh-CN.md Windows 手动步骤
```
