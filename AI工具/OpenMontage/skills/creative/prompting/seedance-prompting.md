# Seedance 2.0 — Prompting Guide

> Layer 3 authority: `.agents/skills/seedance-2-0/SKILL.md`
> For universal vocabulary, see: `skills/creative/video-gen-prompting.md`

## When to pick Seedance 2.0

Seedance 2.0 (ByteDance Seed team, released Feb 2026) is OpenMontage's **preferred premium default for cinematic, trailer, teaser, hype-edit, and motion-led clip work** whenever a paid gateway is configured (`FAL_KEY` via `seedance_video`, or HeyGen Video Agent / Avatar Shots). It is the only model in the fleet that delivers all of:

- single-pass native synchronized audio (speech + SFX + ambience together, not post-sync),
- multi-shot generation inside a single prompt,
- director-level camera control,
- lip-sync from quoted dialogue,
- reference-conditioned generation with up to 9 images + 3 video clips + 3 audio clips,
- consistent character identity across shots.

Elo 1269 on Artificial Analysis as of release — ahead of Veo 3, Sora 2, Runway Gen-4.5.

Switch off Seedance 2.0 only when there is a real reason: strict budget (use the `fast` variant or LTX), explicit user preference (VEO/Sora/Kling), or a stylistic fit another model does better (VEO for photoreal landscape, Kling for anime).

## Seedance 2.0 8-Component Prompt Structure

Seedance is unusually literal about camera language, multi-shot cuts, and quoted dialogue. Use this structure — include what matters, omit what doesn't:

1. **Shot / framing** — wide establishing, medium, close-up, Dutch angle, etc.
2. **Camera movement** — static, slow push-in, aerial, handheld, arc, dolly zoom
3. **Subject description** — the physical detail that must persist across shots (identity anchor)
4. **Action beats** — one beat per sentence, use `→` or explicit `Shot 1 / Shot 2` for multi-shot
5. **Setting / environment** — location, era, weather, time of day
6. **Lighting / palette** — one lighting idea, pick and commit
7. **Style / grade / era** — "anamorphic lens, teal-orange grade, 35mm film grain"
8. **Audio** — ambient, diegetic, music direction (textural only), quoted dialogue for lip-sync

## Seedance-specific strengths

| Capability | How to invoke it |
|---|---|
| **Native synced audio** | Describe the soundscape in the prompt. Leave `generate_audio=true`. |
| **Multi-shot in one generation** | Use `Shot 1 (...)`, `Shot 2 (...)` etc. Keep subject description consistent across shots. |
| **Director-level camera** | Use unambiguous terms: `slow dolly-in`, `arc shot`, `Dutch tilt`, `aerial push-in`, `handheld with micro-shake` |
| **Lip-sync from quoted dialogue** | `Character says: "line."` — each line ≤ ~6 words on fast cuts |
| **Reference-to-video** | Use the `reference-to-video` endpoint; name each asset in the prompt (`Reference 1: hero character — ...`) |
| **Character identity consistency** | Describe the same physical details in every shot — Seedance uses those as the identity anchor |

### Audio reference slots — per-track, per-speaker

When using reference audio (up to 3 clips on reference-to-video), **attach each clip only on tracks where that speaker's voice is actually generated**:

- **Speaker has dialogue in this track** → upload + bind the voice reference in that track's prompt block (e.g. `@音频1 = 强哥四川话音色参考`).
- **Speaker is on-screen but mouth closed / no VO in this track** → do **not** upload or cite their voice reference on that track; other speakers use independent generated voices.
- **Never spread one voice reference across speakers** — e.g. do not cite 强哥 audio on an aunt-only track; it pulls non-主角 voices toward the reference timbre.
- **强哥 dialogue = Sichuanese (四川话)** — default **成都温江本地口音**. When 强哥 has lip-sync lines: bind `@音频1 = 强哥四川话音色参考`; add delivery line `强哥口播：四川话男声`; tag 强哥 beats with `——四川话`; include `禁止普通话念稿` in the `@音频1` binding. See `.cursor/rules/seedance-delivery-block.mdc` § **强哥口播 · 四川话铁律**.

Split-track prompts (`talk-multi`): list upload assets **per track**; a global asset table must mark `仅轨 N` when shared image refs apply to all tracks but audio refs do not.

**Handheld continuation (track 2):** When both tracks are 业主阿姨 handheld selfie POV, generate track 1 first, capture its **last frame**, upload as track-2 `@图片N` (e.g. `@图片5`) with `@图片N = 作为首帧` + **以参考图为准**. Track 2 **does not** re-upload the aunt portrait ref. **Optional:** re-upload the environment ref (e.g. `@图片1 = 背景环境参考`) alongside the first-frame screenshot — **roles must differ**: screenshot = **作为首帧** (composition/camera/positions); environment ref = **背景环境参考** only (kitchen/cabinet detail), never also「作为首帧」. Keep 强哥 `@图片2` on track 2.

**Track-2 copy block must stand alone:** Pasted into Seedance **without** track 1 or `[H]` context. **No**「轨1」「上一段」「末帧截图来源」. **Do not** spell out aunt appearance/pose — track 1 output may drift; trust the screenshot.

**Handheld selfie spatial logic:** Camera is in the aunt's hand (fixed arm-length rig). 强哥 does **not**「占自拍前景 / 占主画面」. Write: **自画面后方景深向镜头方向走来，至中近景正对镜头口播** — subject gets larger via perspective, camera does not hand off.

**Handheld selfie camera logic:** Allowed: 微晃、不推近、不变焦、机位固定手臂长度. **Forbidden** in same block: 缓慢推近/拉远、dolly、变焦 — those imply tripod/camera crew, not phone selfie.

**Generalize:** Any continuation frame (I2V chain, video extend, last-frame-as-first-frame) → trust uploaded frame, describe **only new motion/dialogue**; run **standalone paste test** per track.

See `.cursor/rules/seedance-delivery-block.mdc` § **交付块逻辑自检** for full checklist.

**Delivery text vs spec:** Audio mount rules (which track gets `@音频1`) belong in the `[H]` upload table — not as negation lines inside the copy block. The copy block states positive bindings only (track 2: `@音频1 = 强哥四川话音色参考；强哥口播对口型，成都温江四川话…`; track 1: omit `@音频` and describe `阿姨口播：四川话女声`). **Any track with 强哥 lip-sync** must also include `强哥口播：四川话男声` and mark 强哥 beats `——四川话`. **Speech-rate planning** (`6字/秒含标点`, word-count ÷6) stays in `[H]` only — not in the copy block.

**15s 口播字数铁律（与 `.cursor/rules/seedance-delivery-block.mdc` 同步）：** 单轨 **15 秒** 定稿台词必须 **90～93 字（含标点）** —— 铺满 15 秒；**少于 90 字不行**，**多于 93 字必须拆轨**。其他时长按「字数 ÷ 6 ≈ 秒数」换算，单轨仍 ≤15 秒 · ≤93 字。

**禁止叠说 · 动作预留时间（与 `.cursor/rules/seedance-delivery-block.mdc` § 口播 · 禁止叠说 · 动作预留时间 同步）：**

1. **零叠说（人）**：同一时刻仅一人出声；交接秒其他人嘴闭。
2. **零叠说（动作）**：禁止同一 `X至Y秒` 内既写大动作又写开口（「转身冲上扶住」+「说：」同段 = 翻车）。
3. **动作窗必留**：滑倒 / 碰头 / 扶人到位 / 出画 / 拨号贴耳 / 听对方 等必须单独 `无口播` 秒段，完成后再开口。
4. **预算**：口播秒 = 字数÷6；**动作空窗预算 = 轨时长 − 口播秒**；先锁动作窗再排口播。动作不够 → 加时长或拆轨，禁止挤进口播段。
5. **伴随手势可同段**（点头、指一下、轻拍胸口）；**大位移不可同段**。
6. **口播段写法**：起句写完成态（「已扶住」「手机已贴耳」）再 `说：`。

**Reference tags once:** Each `@图片` / `@音频` line appears **only in the top binding section** — **no `【参考绑定】` header row**. After binding, describe subjects by **role name** — no repeated `@` or "consistent with @图片N".

**Identity once, then name:** Appearance anchors (e.g. `五官脸型短发工服男`, supporting cast wardrobe) appear **once** in the binding line and/or overview / first entrance (`强哥（五官脸型短发工服男）…`). Later beats use **only the role name** (`强哥` / `大哥` / `大姐`). Do **not** paste the full appearance string every beat. Prefer role names over「他 / 同一人」when multiple people share the frame. Same for supporting cast: full look on first beat, then short names + short constraints (`嘴闭`).

**Copy block structure (Chinese repo `-生视频提示词.md`):**

- No `【】` section headers; beats start with `X.XX至X.XX秒，`.
- Micro-motion: `自然眨眼每3～5秒` inline in overview or beats — not a `【微动·A线】` block.
- Lip-sync lock: `以上口型与台词一字不改：「…」` as one closing sentence.
- Final line after lip-sync lock: `禁止字幕，禁止背景音乐，禁止水印。` (only these three negations belong in the copy block; place at the end, not the top).
- **Cast / who is on screen — positive only:** Write who *is* in frame (`画中是阿姨与老头两人` / `画中是强哥一人`). Do **not** put exclusion lines in the copy block (`无强哥入画` / `无工人` / `无其他人物入画` / `禁止路人入画`). Those constraints belong in `[H]` (upload table, failure fixes) plus simply not mounting unused character refs. Naming absent roles distracts the model.

See `.cursor/rules/seedance-delivery-block.mdc` § **人数 / 入画 · 只写有谁** for the full rule.

## Background / environment reference (`@图片1`)

When the project supplies an environment reference image, **bind it — do not transcribe the photo** in the delivery copy block.

| Allowed in `@图片1` binding | Forbidden in binding + beats |
| --- | --- |
| `翻新厨房背景，全程不换景。` | 白色橱柜、灰色墙砖、暖黄灯带、马桶/台盆位置… |
| `厕所背景，全程不换景。` | `与参考图几何一致` · `墙地柜体与参考图一致` |
| Named community gate / building sign: scene name + `大门招牌「小区名」字型稳定可读` | Materials, colors, brick texture, light strips, geometry catalogs |
| `[H]` upload table may list filename for humans | Repeating reference materials, colors, fixtures, lighting strips |

**Named gate / sign readability (required):** When the shot is a **named community gate** or a **named building/mall sign** that must stay readable on camera, `@图片1` **must** lock the sign text — same idea as `@图片3` requiring readable「大改造家」. Writing only `XX大门背景，全程不换景` is **not enough**.

```text
@图片1 = 友谊花园大门背景，大门招牌「友谊花园」字型稳定可读，全程不换景。
```

Indoor kitchen/bath/stair scenes with no readable sign still use scene name + 不换景 only.

**Narrative blocking is fine** (e.g. 强哥在淋浴隔间内、推开玻璃门) — that is action/staging, not a reference-image catalog. If layout must stay locked, rely on the uploaded `@图片1`; do not substitute a prose floor plan.

**No faces from the reference photo:** `@图片1` locks environment only; do not inherit any person visible in the reference image.

## Workwear / Logo reference (`@图片3`)

When the project supplies a brand Logo image for 强哥's workwear, bind color + chest mark and **require readable brand text**:

```text
@图片3 = 仅作工服颜色与左胸Logo参考，「大改造家」字体稳定可读。
```

| Layer | Wording |
| --- | --- |
| `[H]` upload table | `Logo 图 · 仅作工服颜色与左胸 Logo 参考，「大改造家」字体稳定可读` |
| Delivery binding | `@图片3 = 仅作工服颜色与左胸Logo参考，「大改造家」字体稳定可读。` |
| QC | Left-chest「大改造家」stable and readable — not blurry / missing glyphs |

Longer bindings that also lock workwear fill to the Logo background color are fine (e.g. `短袖工服颜色参考logo背景色，工服左胸有logo，「大改造家」字型稳定可读`), but **do not drop** the readable「大改造家」requirement. See `.cursor/rules/seedance-delivery-block.mdc` § **工服 Logo · 绑定铁律**.

## Multi-shot pattern

> **Repeat identity verbatim across every shot.** "the same character" / pronouns / "Aang again" do not work. Repeat the 3–6 disambiguating visual attributes verbatim in every shot block. Seedance treats each shot as if you said it cold.

Seedance honors explicit shot lists:

```
Shot 1 (wide aerial establishing, slow push-in):
Snow-covered Air Temple at dawn, spires catching first orange light.
Wind lifting prayer flags.

Shot 2 (medium, low angle, handheld):
Aang — bald, blue arrow tattoo, orange robes — plants his staff on stone.
He squints into the rising sun.

Shot 3 (extreme close-up, rack focus):
Rack focus from the glowing arrow tattoo on his forehead to the distant peaks.
Aang says: "It's time."

Style: anamorphic lens, teal-orange cinematic grade, 35mm film grain.
Audio: rising orchestral swell with low taiko pulse, wind, distant wingbeats.
```

### Subject transition primitives in multi-shot

Seedance handles four distinct ways a subject can enter or exit a shot. Naming the primitive explicitly helps the model build the right transition between shots.

- **Subject revealing** (by camera move OR subject move) — the subject becomes visible mid-shot.
  Example: `Shot 2 (slow truck right): empty corridor at first; the camera trucks right to reveal Aang — bald, blue arrow tattoo, orange robes — pressed flat against the wall.`

- **Subject disappearing** — the subject leaves frame, by motion or occlusion.
  Example: `Shot 4 (static wide): Aang — bald, blue arrow tattoo, orange robes — sprints into the temple doorway and is swallowed by shadow; camera holds on the empty threshold.`

- **Subject switching** (rack focus / camera move) — focus or framing transfers from one subject to another.
  Example: `Shot 5 (close-up, rack focus): rack focus from Aang's glowing arrow tattoo in foreground to Sokka — dark hair, blue tunic, boomerang on back — emerging from the mist behind.`

- **Complex alternating focus** — focus oscillates between two subjects within one shot.
  Example: `Shot 7 (medium two-shot, alternating rack focus): focus on Aang — bald, blue arrow tattoo, orange robes — as he speaks, then pulls to Katara — long brown hair, blue water-tribe parka — as she answers, then back to Aang on the final beat.`

## Lip-sync pattern

```
Aang says: "I won't run anymore."
Sokka, half a step behind, replies: "Then we fight."
```

- Use `Character says: "..."` / `Character replies: "..."` exactly — mouth shapes key off the quoted strings.
- Keep lines short (≤ 6 words on fast-cut shots) to avoid drift.
- For a single-speaker monologue, keep the camera close and static on the speaker's shot.

## Parameter cheat sheet

| Parameter | Guidance |
|---|---|
| `duration` | `5`–`8` s hero, `10`–`12` s multi-shot scenes, `4` s inserts. `auto` when unsure. |
| `aspect_ratio` | `21:9` trailers, `16:9` broadcast, `9:16` Reels/Shorts/TikTok |
| `resolution` | `720p` default. `480p` for cost-capped previews only. |
| `generate_audio` | Keep `true` — sync audio is the moat. Strip in compose if unused. |
| `model_variant` | `standard` for hero + multi-shot + camera-heavy. `fast` for b-roll, previews, latency-capped jobs. |
| `seed` | Lock once a shot composition reads; iterate variants with the same seed. |
| `prompt length` | 200–400 words for hero shots; 80–150 for inserts. Seedance is one of the few models that rewards long, structured 5-aspect prompts. |

## Iteration strategy

1. **Block out shape** — `duration=5`, `fast`, one shot. Confirm composition.
2. **Lock the seed** — record it in the per-clip README.
3. **Upgrade to `standard`** — same seed, tighten camera + lighting language.
4. **Extend or multi-shot** — only after the single-shot version is clean.
5. **Promote to final** — write the prompt, seed, variant, and duration into the asset manifest so compose can re-render consistent retakes.

## What to avoid

| Don't | Why |
|---|---|
| Four-plus simultaneous actions in one shot | Motion coherence collapses. Split to multi-shot. |
| Readable text / logos inside the clip | Text rendering is unreliable. Handle text in Remotion overlay. |
| Conflicting lighting (`bright noon` + `neon night`) | Model picks one and ignores the other. |
| Long dialogue on fast-cut shots | Lip-sync drifts. |
| `fast` variant for slow-mo, multi-shot, or complex camera | Routinely misses on first try. Route to `standard`. |
| Request a full multi-instrument score from Seedance | Keep audio direction textural; real scoring belongs in `music` / `pixabay_music` / `elevenlabs` and mixes in compose. |
| Bypass `video_selector` without a reason | Loses scoring, fallback, and cost handling. |

## Integration notes

- **Cinematic pipeline:** Seedance 2.0 is the default. 21:9, multi-shot for montage, reference-to-video when the brief has a visual bible.
- **Animated explainer:** Use Seedance 2.0 only for establishing / mood / cold-open clips — core motion graphics stay in Remotion.
- **Screen demo / podcast / clip factory:** Not the right default. Only for stylized cold-opens.
- **Cost check:** `standard` at 10 s ≈ $3.03 / clip on fal.ai. `fast` at 5 s ≈ $1.21. Budget in the proposal stage.

## Example — Airbender trailer hero beat (60 s total trailer, this is shot 3 of 7)

```
Shot 1 (wide aerial, slow push-in, 3s):
Snow-covered Air Temple at dawn, spires catching orange light,
prayer flags lifting in wind.

Shot 2 (low angle medium, handheld, 3s):
Aang — bald, blue arrow tattoo on forehead, orange and yellow robes —
plants his staff on weathered stone, squints into the rising sun.

Shot 3 (extreme close-up, rack focus, 3s):
Rack focus from the glowing arrow on his forehead to distant peaks.
Aang says: "It's time."

Lighting: cold blue ambient with warm break on the horizon,
rim light from rising sun.
Style: anamorphic 2.39:1, teal-orange cinematic grade, 35mm film grain,
halation on speculars.
Audio: low taiko drums rising to orchestral swell on Shot 3,
wind through temple, distant wingbeats, leather staff-grip creak.
```

Parameters: `duration=10`, `aspect_ratio=21:9`, `resolution=720p`, `model_variant=standard`, `generate_audio=true`, seed locked after shot 2.
