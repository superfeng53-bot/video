# Learnings

会话纠正与可复用洞察。

## [LRN-20260731-003] 口播成片：结尾重点18% + 数钱对齐加预算 + 音效峰值
**Date:** 2026-07-31
**Category:** best_practice
**Priority:** high
**Status:** promoted
**Recurrence-Count:** 1
**Pattern-Key:** koubo-endfocus-broll-sfx-v11
**Scope:** project:短视频

### Summary
65旧改会话后半段确认：结尾重点字幕最终位置 18%；数钱 B-roll 挂「加预算」；音效先稀疏规划再峰值适配。已写入 `hyperframes-koubo-chengpian` v1.1。

### Details
- 结尾重点：`top=346px`（18%），上行 70px 金 / 下行 84px 白，左右 ≥80px；多轮试过 48px、十分之八、2.5/10 后定稿
- B-roll：数钱从隐患窗挪到「加预算」；同源素材不成片复用
- 音效：结构点密口播疏；SFX 峰值低于 VO 约 6–11 dB；弱效上调 volume
- Skill：`.cursor/skills/hyperframes-koubo-chengpian/`（含 `ending-focus-caption.md` / `sfx-koubo.md`）
- Rule：`.cursor/rules/learned/koubo-ending-focus-caption.mdc`

### Suggested Action
none（已 promoted）

## [LRN-20260731-002] 口播音效合集拆条：合并/空轨/错位级联修
**Date:** 2026-07-31
**Category:** correction
**Priority:** high
**Status:** promoted
**Recurrence-Count:** 6
**Pattern-Key:** sfx-library-merge-split-cascade
**Scope:** project:短视频

### Summary
用户多轮纠正：相邻短音效被合并、尾条多相位被拆空、空槽借邻居导致整列名字错位。已固化为项目 Skill + Rule。

### Details
- 典型纠正：开场咚+水滴、咚咚+系统音、5+6、9/10 错拆；字幕缺 1/空 7；画面 1+2、3+4、假空 9、10 被拆
- 修法：静音谷拆合并；合并假拆分；拆+1 并−1 后中间整体改名；禁 ASR 人声
- Skill: `.cursor/skills/sfx-library-extract/SKILL.md`
- Rule: `.cursor/rules/learned/sfx-library-split-gates.mdc`
- 产出：`音效库存/` 三类×10 + `manifest.json`

### Suggested Action
none（已 promoted）

## [LRN-20260731-001] 视频素材画面分析用便宜模型
**Date:** 2026-07-31
**Category:** cost_optimization
**Priority:** medium
**Status:** promoted
**Pattern-Key:** video-asset-analysis-cheap-model
**Scope:** project:短视频

### Summary
用户明确：以后分析视频素材（抽帧看画面、按时间段粗分内容）用便宜大模型，不必上主会话高价模型。

### Details
- Task 子 agent：`model: composer-2.5-fast`（或当时可用的同等便宜/快档）
- 粒度：时间段 + 简述 + 标签；结果写入 `素材分析/` 复用
- 已写入：`hyperframes-koubo-chengpian` §3

### Suggested Action
none（已 promoted）

## [LRN-20260730-001] HyperFrames 口播成片 golden path 已晋升
**Date:** 2026-07-30
**Category:** best_practice
**Priority:** high
**Status:** promoted
**Recurrence-Count:** 1
**Pattern-Key:** hyperframes-koubo-blank-caption-sync
**Scope:** project:短视频

### Summary
65旧改六成超预算会话：空白填 B-roll + 语义字幕对齐已验证成片，晋升为项目 Skill。

### Details
- Skill: `.cursor/skills/hyperframes-koubo-chengpian/SKILL.md`
- Rule: `.cursor/rules/learned/hyperframes-koubo-captions.mdc`
- 关键坑：方言 ASR 不可作文案；贪心字数切会拆词；换母片必须重抽音轨；跳过段勿参与全局比例分配。

### Suggested Action
none（已 promoted）
