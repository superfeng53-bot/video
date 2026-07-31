# 口播成片音效（按需读）

何时再读：要规划音效点位、调音量、或对齐 B-roll 切入时。

## 密度原则

- **结构点密、口播段疏**：约 9–11 个点（可含 1 处叠层），不要句句配效。
- 优先落点：开场钩子、B-roll 切入、悬念转折、合同/确认、片尾 CTA。
- 纯口播连续讲解段保持安静。

## 音源优先级

1. 仓库根目录 `音效库存/`（`manifest.json` + 三类短效）
2. 不够再走 `hyperframes-media`（HeyGen / bundled）

## 挂载

```html
<audio class="clip" src="./assets/sfx-koubo/….mp3"
  data-start="…" data-duration="…" data-track-index="11+" data-volume="0.28–0.40"></audio>
```

- 与对应 B-roll / 关键词 `data-start` 对齐（例如数钱切 + `k-ding`）。
- 口播成片默认不加 BGM。

## 峰值适配（必做一次）

对 `vo.wav` 与各 SFX 跑 peak / loudnorm：

- 目标：SFX 峰值约低于口播 **6–11 dB**（点缀可闻，不抢话）。
- 偏弱（差 >11 dB）→ 上调 `data-volume`（本片例：`k-sou-xiu` 0.28→0.38，`k-huiyi-shua` 0.30→0.36）。
- 偏冲（差 <4 dB）→ 下调。

计划可落盘 `sfx-koubo-plan.json`（`t` / `file` / `vol` / `note`），便于改点位后重渲。

## 本片参考点位（65旧改 · 约 58s）

| t | 效 | 作用 |
|---|----|------|
| 开场钩子 | k-yingshi-dong | 超预算重锤 |
| B-roll 切入 | k-shua / k-dong-kong / k-sou-xiu / k-xunsu | 砸墙/空鼓/乱线 |
| 悬念 | k-peng | 「更吓人」 |
| 加预算 | k-ding | **对齐数钱画面** |
| 勘验 / 合同 | k-kaiqi / k-zhengque | 开门、确认 |
| CTA | k-dingding | 片尾 |
