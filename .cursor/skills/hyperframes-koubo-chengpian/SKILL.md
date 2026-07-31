---
name: hyperframes-koubo-chengpian
description: >
  用 HyperFrames 把竖版口播母片做成可交付成片：检测黑场空白并用内容契合的
  B-roll 填补（源片不重复）、用准确台词做语义字幕（不拆词、可跳过指定段）、
  片尾重点展示型字幕、本地音效库存点缀并对峰值，对齐音轨后本地渲染。
  在用户说 HyperFrames 口播成片、填空白、补 B-roll、字幕对不上音频、字幕断句有问题、
  加音效、结尾重点字幕、以某 mov/mp4 为基础重做成片时使用。不替代 ChatCut 剪辑；不做平台发布。
license: MIT
metadata:
  author: harvested
  version: "1.1"
  verified: "2026-07-31 · 65旧改六成超预算成片.mp4（结尾18% + 音效峰值适配）"
---

# HyperFrames 口播成片（空白填画 + 语义字幕）

把「口播 A-roll + 黑场空白 + 旁白台词」做成 9:16 成片：B-roll 按台词语义匹配，字幕按语义断句并对齐**当前母片音轨**，可选片尾重点板与稀疏音效。

**Failure pattern:** 字幕早/晚于说话；断句拆词；空白段素材与台词无关或同源复用；换母片却用旧 wav；数钱等象征画面挂错语义窗；结尾重点挡脸或过高；音效抢口播峰值。  
**Verified by:** `65旧改六成超预算` 成片（约 58s / 1080×1920）：语义字幕 + 不重复 B-roll + 音效峰值适配 + 结尾重点 `top=346px`（18%）。

## When to use

- 用户给出口播母片路径，要求 HyperFrames 成片 / 填空白 / 加字幕
- 已有成片但「字幕和音频没对上」「断句有问题」
- 更换基础视频后要求按新母片重做（必须重抽音轨）
- 加片尾区域/业务重点字、或从 `音效库存` 配稀疏音效

## Procedure

### 0. 项目骨架

- 工作目录示例：`项目/<片名>/hyperframes-成片/`
- 画布固定 **1080×1920 / 30fps**；`index.html` 为唯一根 composition（封面放 `compositions/`，避免 lint/render 抢根）
- 本机用**项目内** CLI：`./node_modules/.bin/hyperframes`（先 `npm i hyperframes`）；全局 `npx` 易缺 manifest
- **成品交付**：`成品/<片名>/` 下放成片 + 封面（同目录），勿散落

### 1. 母片与音轨（同源）

```bash
# 画面（无声）
ffmpeg -y -i "$BASE" -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -pix_fmt yuv420p -r 30 -an assets/base.mp4

# 音轨必须从「当前」母片抽，勿复用旧 wav
ffmpeg -y -i "$BASE" -vn -acodec pcm_s16le -ar 44100 -ac 1 assets/vo.wav
```

- `base`：`muted` + `data-track-index="0"`
- `vo`：`data-track-index="10"`，`data-start="0"`
- **禁止**在脚本里 `audio.currentTime` / `play()`（HyperFrames 接管播控）

### 2. 检测黑场空白

```bash
ffmpeg -i assets/base.mp4 -vf "blackdetect=d=0.25:pix_th=0.10:pic_th=0.95" -an -f null -
```

记下每段 `black_start/end`，作为 B-roll 窗口。

### 3. B-roll：按台词内容匹配，不按「有素材就塞」

**素材画面分析（抽帧粗分时间段）默认用便宜模型**：Task 子 agent 指定 `model: composer-2.5-fast`（或当前列表里同等价位/更快档）。只需「时间段 + 一句话描述 + 标签」，相近画面合并即可；结果落盘到 `素材分析/` 避免重复。成片匹配、字幕语义、最终验收仍用主会话模型。

对每个空白窗，先读该时段旁白在说什么，再选素材：

| 旁白语义 | 优先素材类型 |
|----------|--------------|
| 空鼓 / 墙雷 / 基层 | 空鼓脱落、铲墙 |
| 锈水管 | 锈管剖面、换管 |
| 乱接线 | 弱电井、乱线施工 |
| 方案不清 / 踩坑 | 乱现场、返工、飘窗坑 |
| **加预算 / 给你加预算** | **数钱**（勿提前挂到「乱/坑」窗） |
| 深度勘验 / 巡检 | 量房、水电巡检 |
| 合同锁价 | 图纸、设计师沟通 |

裁切为 1080×1920，时长 ≤ 空白窗；源片短于窗则缩短 `data-duration`，勿硬拉。叠在 `data-track-index="1"`。**同一源视频在成片里只出现一次**（可换不同素材，勿复用同一文件的不同时段当两段填空）。

### 4. 字幕：准确台词 → 语义行 → 挂到时间窗

1. **台词以用户提供的准确稿为准**（方言口播 ASR 文本不可信）。
2. **先人工语义断句**，再写时间：
   - 单行尽量 ≤7 字，完整词组可到 8
   - **禁止**拆词：`公司` `一直` `提前` `设计师` `墙体` `30%以上`
   - **禁止**标点
   - 指定段（如「2025 家装报告…」）整段不加字幕
3. **时间轴**：对 `assets/vo.wav` 跑带时间戳的 ASR（仅借 segment 边界）或 `silencedetect`，把语义行挂进对应窗；窗内按字数比例分配，最短可见约 0.30s。
4. HTML：`class="clip cue"` + `data-start/duration`；GSAP 仅做短淡入（≤50ms）+ **硬 kill**；**勿对 `.clip` 动画 `visibility`**。
5. 样式经验值（竖版口播行）：约 `top:1280px`（下十分之三）、`font-size:88px`、左右边距 ≥88px、`white-space:nowrap`、描边+阴影保证可读。
6. **结尾重点展示型字幕**（区域+业务导流）：
   - 位置 **画面高度 18%**（`top:346px` @1920）
   - 两行：上行金约 70px、下行白约 84px（下行更大）
   - 左右 ≥80px 留白
   - 标准见 `references/ending-focus-caption.md`；Rule：`.cursor/rules/learned/koubo-ending-focus-caption.mdc`

### 5. 音效（优先本地音效库存）

1. **先分析再加**：哪些结构点该加、密还是疏——默认稀疏（详见 `references/sfx-koubo.md`）。
2. **首选**仓库根目录 `音效库存/`；不够再走 `hyperframes-media`。
3. 挂成 `<audio class="clip">`，对齐 B-roll/关键词；音轨 `11+`；口播成片默认不加 BGM。
4. **峰值适配**：SFX 峰值约低于口播 6–11 dB；偏弱上调 `data-volume`，偏冲下调。计划可写 `sfx-koubo-plan.json`。

### 6. 渲染与抽检

```bash
./node_modules/.bin/hyperframes render -c . -o "/绝对路径/成品/<名>/成片.mp4" -q high
```

抽检：开场句、空白段中点、片尾 CTA + 结尾重点板；确认无拆词、报告段无字幕、B-roll 与旁白同义、**源片不重复**、重点字不挡脸、音效不抢话。成品与封面同目录。

## Gotchas

- **换母片 = 换音轨**。重导出的 mov 与旧 wav 能量相关可能接近 0，字幕会整段漂。
- **跳过报告段时**，不要把报告时长还算进「全局比例分配」，否则后续句会被挤到错误窗。
- 方言口播：`mlx-whisper` / small 模型文本错字多，只可用其 **时间边界**，不可用其字面做字幕。
- `stable-ts` / openai-whisper 权重下载可能遇 SSL；本机已有 `mlx-community/whisper-small-mlx` 时可走 mlx。
- **象征画面跟语义走**：数钱挂「加预算」，不要挂在更早的乱房/隐患窗。
- **结尾位置用比例说话**：用户说「18%处」= `1920×0.18`；勿把「十分之八」和「上八成」混用。
- GSAP 对 `#end-focus` 等 `.clip` **禁止**改 `visibility`（StaticGuard）。
- 封面：真人用母片抽帧，勿用 AI 换人；风格可参考 douyin-cover（顶标题、关键词醒目、人物右下）。

## What didn't work

- 仅靠 Whisper 词级时间戳切字幕 → 方言错字 + 时间漂。
- 按字数贪心 `MAX=7` 硬切 → `旧改公|司`、`一|直给你`、`30%以|上`。
- 静音段比例映射含「跳过段」→ 跳过后半句丢失或挤进报告窗。
- 全局 `npx hyperframes render --out` → 参数应为 `-o`；且易缺本地 runtime manifest。
- 多个根 HTML（根目录 `cover.html`）→ lint/render 异常；封面移到 `compositions/`。
- 数钱挂在隐患/乱房窗 → 用户要求挪到「加预算」。
- 结尾重点顶到 48px / 误放到十分之八底部 → 挡脸或位置反直觉；确认标准为 **18%**。

## 与其它 skill 的边界

| 需求 | 用 |
|------|----|
| ChatCut 里剪口播 / MG | `majia-chatcut-koubo` / `edit-talking-head-videos` |
| HyperFrames 通用作者契约 | `hyperframes` / `hyperframes-core` |
| 音效库拆条入库 | `sfx-library-extract` |
| 本流程（空白+语义字幕+重点板+音效+本地渲） | **本 skill** |

更细断句/B-roll 见 `references/caption-and-broll.md`；结尾重点见 `references/ending-focus-caption.md`；音效见 `references/sfx-koubo.md`。
