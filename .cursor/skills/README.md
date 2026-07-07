# 短视频项目 · Cursor Skills

本仓库 `.cursor/skills/` 仅保留两套 skill 体系。

## Cheat on Content（内容校准循环）

| 入口 | 路径 | 职责 |
| --- | --- | --- |
| **cheat-on-content** | `.cursor/skills/cheat-on-content/SKILL.md` | 打分 → 盲预测 → 发布 → T+3d 复盘 → 进化 rubric |
| 子 skill | `.cursor/skills/cheat-*/SKILL.md` | init / score / predict / retro / bump / trends 等 15 个子流程 |

**源码目录**（junction 指向）：`AI工具/cheat-on-content/`

**更新**：在 `AI工具/cheat-on-content` 里 `git pull`，本仓库 skill 自动同步。

**首次使用**（在本仓库根目录对 Agent 说）：

```
初始化 cheat-on-content
```

**日常触发词**：`打分这篇` · `启动预测` · `已发布` · `复盘` · `升级 rubric` · `状态` · `抓热点` · `找对标`

---

## OpenMontage（代理化视频制作）

| 入口 | 路径 | 职责 |
| --- | --- | --- |
| **open-montage** | `.cursor/skills/open-montage/SKILL.md` | 流水线入口 · 必读 AGENT_GUIDE |
| Layer 3 工具 skill | `.cursor/skills/<name>/SKILL.md` | remotion、seedance-2-0、ffmpeg 等 78 个（junction → OpenMontage） |

**源码目录**：`AI工具/OpenMontage/`

**更新**：在 `AI工具/OpenMontage` 里 `git pull`，junction skill 自动同步。

**首次环境**：

```powershell
cd AI工具/OpenMontage
make setup
```

**日常触发词**：`做一个 60 秒解说视频` · `参考这个视频做一版` · `用 Remotion 合成`

### AI 生视频提示词（本仓库默认流程）

写 / 改 / 审 `*-生视频提示词.md` 或方案里的 Seedance 段时，**一律走 OpenMontage**，不走全局 `seedance-2.0-temp` 或已删的旧 skill。

| 步骤 | 读什么 |
| --- | --- |
| 1 通用规范 | `AI工具/OpenMontage/skills/creative/video-gen-prompting.md` |
| 2 模型专项 | `AI工具/OpenMontage/skills/creative/prompting/seedance-prompting.md`（默认 Seedance 2.0） |
| 3 工具 skill | `.cursor/skills/seedance-2-0/SKILL.md` |
| 4 验收 | CHAI 5 维自检 + `seedance-2-0` Verification checklist + **口播 ≤93 字/15s（6 字/秒含标点，超限拆轨）** |

Cursor 规则：`.cursor/rules/open-montage-video-prompts.mdc`（匹配 `*生视频*` / `*故事板*` / `*提示词*` 等文件时自动生效）
