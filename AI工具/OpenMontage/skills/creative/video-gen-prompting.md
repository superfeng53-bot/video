# Video Generation Prompting — Universal Guide

## When to Use

When writing prompts for the video generation family (`video_selector`, `seedance_video`,
`heygen_video`, `wan_video`, `hunyuan_video`, `ltx_video_local`, `ltx_video_modal`,
`cogvideo_video`). This skill covers the universal prompt vocabulary that works across all
video generation models. For the **preferred premium default**, see the Seedance 2.0 row
in the table below.

For model-specific tips, see the linked guides below.

## Model-Specific Guides

| Model | Guide | Key Insight |
|-------|-------|-------------|
| **Seedance 2.0 (standard / fast)** | `creative/prompting/seedance-prompting.md` + Layer 3 `.agents/skills/seedance-2-0/` | **Preferred premium default** when `FAL_KEY` or HeyGen is configured. Single-pass synced audio, multi-shot generation, director-level camera, lip-sync from quoted dialogue, reference-to-video (9 img + 3 vid + 3 audio). Elo 1269 (#1 on Artificial Analysis). |
| **Sora 2 / Sora 2 Pro** | [OpenAI Sora 2 Cookbook](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide) | Richest structured template. Advanced fields: lenses, filtration, grade, diegetic sound, wardrobe, finishing. |
| **VEO 3.1 / VEO 3** | [Vertex AI Prompt Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide) | Best vocabulary reference tables. 14-component prompt structure. |
| **Grok Imagine Video** | `creative/prompting/grok-prompting.md` | Best when prompts need reference-image placeholders like `<IMAGE_1>` and identity/product carryover. |
| **LTX-2** | [LTX Prompting Guide](https://docs.ltx.video/api-documentation/prompting-guide) | 6-element structure. Audio/voice prompting. Strong "what to avoid" section. |
| **HunyuanVideo 1.5** | [Tencent Prompt Handbook](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/assets/HunyuanVideo_1_5_Prompt_Handbook_EN.md) | Formula: Subject + Motion + Scene + [Shot] + [Camera] + [Lighting] + [Style] + [Atmosphere]. |
| **Runway Gen-4** | [Runway Prompting Guide](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide) | "Focus on motion, not appearance." One scene per clip. Simplicity wins. |
| **Kling 2.6** | [Kling Prompt Guide](https://fal.ai/learn/devs/kling-2-6-pro-prompt-guide) | 4-part structure. Supports `++emphasis++` syntax for key elements. |
| **Wan 2.1 / CogVideoX** | Use this generic guide | No official prompt guide. Standard cinematographic vocabulary works well. |

## Order Matters

When listing multiple subjects or events:

- **Temporal order** when events unfold over time ("First X enters, then Y reacts").
- **Prominence order** when temporal isn't relevant — humans before objects, largest/most-centered first, then secondary subjects.

## Self-Contained Prompt

> Write the prompt so that someone who has never seen the intended video could picture the subjects, scene, motion, and camera work from your text alone. If a reader could not picture it, a generation model will not render it.

## Universal Prompt Formula

Prior work (CMU/Harvard, "Building a Precise Video Language with Human-AI Oversight") shows VLMs reliably describe subject + scene but fail on motion, spatial, and camera. **Forcing prompts to fill all five slots is the highest-leverage change.**

The OpenMontage canonical 5-aspect skeleton:

```
[Subject]        type + key visual attributes + how to disambiguate when multiple
[Subject Motion] actions in temporal order; subject↔object and subject↔subject interactions; group action
[Scene]          overlays (separately!) + POV + setting + time of day + scene dynamics
[Spatial]        shot size + position-in-frame + depth (FG/MG/BG) + camera-height-relative
                 — and how those CHANGE during the clip
[Camera]         playback speed → lens distortion → height → angle → focus/DoF → steadiness → movement
```

**Shorter prompts = more creative freedom. Longer prompts = more control.**

### Prompt Length by Model

Empirical sweet spots from the paper's Section 6 findings — different models reward different prompt densities:

| Model | Sweet Spot | Notes |
|---|---|---|
| Seedance 2.0 | 200–400 words for hero shots, 80–150 for inserts | Reward long, structured 5-aspect prompts |
| Wan 2.2 | 200–400 words | Fine-tuned on long captions |
| Sora 2 / VEO 3.1 | 100–250 words | Plateau past ~250 |
| LTX-2 | ≤ 80 words | Degrades past that, keep tight |
| Runway Gen-4 | ≤ 60 words | "Focus on motion, not appearance" |

### Overlays Are Not Scene Depth

> Overlays (titles, HUD, subtitles, watermarks, framing graphics) are NOT part of the scene's foreground/midground/background depth axis. List them separately with content and placement. Never say "overlay in the foreground."

---

## Camera Shot Types

| Shot | When to Use |
|------|-------------|
| **Wide / establishing shot** | Open a scene, show location context |
| **Full / long shot** | Subject head-to-toe with environment |
| **Medium shot** | Waist up, balances detail with context |
| **Medium close-up** | Chest up, conversational intimacy |
| **Close-up** | Face or key object, emphasize emotion |
| **Extreme close-up** | Isolated detail (eye, drop, texture) |
| **Over-the-shoulder** | Conversation framing, connection |
| **Point-of-view (POV)** | Viewer becomes the character |
| **Bird's-eye / top-down** | Map-like overview, omniscient feel |
| **Worm's-eye view** | Looking straight up, emphasize height |
| **Dutch / canted angle** | Tilted horizon, unease or tension |
| **Low-angle** | Subject appears powerful, dominant |
| **High-angle** | Subject appears small, vulnerable |

## Camera Movements

The paper shows current models confuse translation, rotation, and lens-only changes — group your prompts so the model can't conflate them:

| Group | Primitives | Rule |
|---|---|---|
| **Translation** (camera physically moves) | dolly in/out, truck left/right, pedestal up/down | "dolly forward toward subject" |
| **Rotation** (camera pivots in place) | pan left/right, tilt up/down, roll CW/CCW | "pan right across the room" |
| **Lens-only** (no camera move) | zoom in/out, rack focus, pull focus, focus tracking | "zoom in" ≠ "dolly in" |
| **Hybrid / signature** | dolly zoom (vertigo), arc/orbit, crane, whip pan, tracking/follow, handheld | "vertigo" only at moments of revelation |
| **Stillness states** | static (NO movement at all — strict), micro-shake, locked-off | "static" requires zero movement, focus change, or zoom |

> **dolly ≠ zoom.** dolly is camera translation; zoom is focal-length change. Models follow whichever token dominates. **pan ≠ truck.** pan rotates, truck translates laterally.

> **Static shot is strict.** A static shot has zero movement, zero focus change, zero zoom. If any of those occur, do NOT write "static camera" — pick the right movement primitive.

## Camera Height (relative to ground)

| Primitive | Example |
|---|---|
| Aerial-level | "drone-altitude wide of the city" |
| Overhead-level | "rooftop height looking across the street" |
| Eye-level | "framed at eye level" |
| Hip-level | "hip-height tracking shot" |
| Ground-level | "low to the ground, ankle height" |
| Water-level | "skimming the water surface" |
| Underwater | "submerged below the surface" |

## Camera Angle (relative to subject)

| Primitive | Definition |
|---|---|
| **Bird's-eye** | strict top-down. Not the same as aerial. |
| High angle | looking down on subject |
| Level angle | camera and subject at same height |
| Low angle | looking up at subject |
| Worm's-eye | looking straight up |
| **Dutch angle (fixed)** | tilted horizon held steady |
| **Dutch angle (rolling)** | horizon tilt changes during shot |

> **bird's-eye = strict top-down. aerial = altitude.** A drone shot at 45° looking down is a high angle from aerial height, NOT bird's-eye.

## Point of View (POV)

| POV | Example |
|---|---|
| First-person | "the camera follows the character's viewpoint as they walk" |
| Drone | "aerial drone footage of city skyline" |
| Over-the-shoulder | "OTS framing of the laptop screen" |
| Top-down oblique | "top-down view of the chess board, tilted slightly" |
| Dashcam | "vehicle dashcam framing of the road" |
| Objective / Neutral | (default — use when no specific POV) |

## Lighting Vocabulary

| Term | Effect |
|------|--------|
| **Natural light** | Soft, realistic (morning sun, overcast, moonlight) |
| **Golden hour** | Warm sunlight, long shadows, romantic |
| **High-key** | Bright, even, cheerful — comedy, lifestyle |
| **Low-key** | Dark, high contrast — thriller, drama |
| **Rembrandt** | Triangle of light on cheek, classic portrait |
| **Film noir** | Deep shadows, stark highlights |
| **Volumetric** | Visible light rays through atmosphere (fog, dust) |
| **Backlighting** | Light behind subject, silhouette effect |
| **Side lighting** | Strong directional, dramatic shadows |
| **Practical lights** | In-frame sources (lamps, candles, neon signs) |
| **Rim / edge light** | Highlights subject outline, separates from background |

**Lighting direction modifiers**: key light, fill light, bounce, rim, spill, negative fill.

**Color temperature**: warm (tungsten, amber), cool (daylight, blue), mixed.

## Lens & Optical Effects

| Effect | Result |
|--------|--------|
| **Wide-angle lens** (24-35mm) | Broader view, exaggerated perspective |
| **Telephoto** (85mm+) | Compressed perspective, subject isolation |
| **Anamorphic** | Stretched aspect, signature lens flares |
| **Lens flare** | Streaks from bright light hitting lens |

### Lens Distortion

The paper distinguishes two primitives that models honor as separate effects — they are NOT interchangeable:

| Primitive | Effect |
|---|---|
| **Fisheye** | extreme curvature, edges bent strongly outward |
| **Barrel** | mild distortion, straight lines bow slightly outward |

### Focus / Depth of Field

| Primitive | Definition |
|---|---|
| Deep focus | everything sharp, FG to BG |
| Shallow DoF | subject sharp, background bokeh |
| Extremely shallow DoF | razor-thin focal plane |
| Rack focus | shifts focus between two subjects mid-shot |
| Pull focus | gradual focus shift (slower than rack) |
| Focus tracking | focus follows a moving subject |

When DoF changes during a shot, label start AND end focal plane (FG/MG/BG/out-of-focus).

## Subject Transitions

When subjects enter, leave, or hand off focus, name the transition explicitly:

| Primitive | When |
|---|---|
| **Subject revealing** | a new subject enters frame (by subject movement OR camera movement) |
| **Subject disappearing** | a subject exits frame |
| **Subject switching** | focus shifts from one subject to another (often via rack focus or camera move) |
| **Complex alternating** | subjects alternate focus multiple times |

Always name the cause: "by subject movement" or "by camera movement". This unlocks reveal-style camerawork in multi-shot prompts.

## Identity Anchoring for Multi-Shot Prompts

> Models lose character identity across cuts unless you re-state it. In every shot of a multi-shot prompt, repeat the same 3–6 disambiguating visual attributes for each named subject verbatim. Pronouns and "the same character" do not work.
>
> Example: "Aang — bald, blue arrow tattoo on forehead, orange-and-yellow robes — plants his staff. … Aang — bald, blue arrow tattoo on forehead, orange-and-yellow robes — turns to camera."

## Style & Aesthetic References

### Cinematic Styles
- Film noir, period drama, thriller, modern romance
- Documentary, arthouse, experimental film
- Epic space opera, fantasy, horror
- 1970s romantic drama, 90s documentary-style

### Animation Styles
- Studio Ghibli / Japanese anime
- Classic Disney, Pixar-like 3D
- Stop-motion, claymation
- Hand-painted 2D/3D hybrid
- Cel-shaded, low-poly 3D

### Art Movements
- Impressionistic, surrealist, Art Deco, Bauhaus
- Watercolor, charcoal sketch, ink wash
- Graphic novel, blueprint schematic

### Film Stock / Grade
- Kodak warm grade, Fuji cool tones
- 16mm black-and-white, 35mm photochemical contrast
- Vintage grain overlay, halation on speculars
- Teal-and-orange color grade

## Temporal Effects

### Playback Speed

The paper defines six explicit playback-speed primitives. Use the right one — they're not synonymous:

| Primitive | Definition |
|---|---|
| Time-lapse | events significantly faster than real time (clouds racing) |
| Fast-motion | slightly faster than real (1x–3x) |
| Slow-motion | slower than real |
| Stop-motion | frame-by-frame discrete movements |
| Speed-ramp | mix of fast and slow within the same shot |
| Time-reversed | plays in reverse |

### Other Temporal Devices

| Effect | Use |
|--------|-----|
| **Freeze-frame** | Dramatic pause |
| **Rapid cuts** | Energy, urgency |
| **Continuous / long take** | Immersion, tension |
| **Fade in / fade out** | Scene transitions |
| **Match cut** | Visual continuity between scenes |

## Audio Descriptions

Models that support audio generation (LTX-2, Sora 2, VEO 3) respond to:

**Ambient**: wind, rain, traffic, crowd murmur, forest birds, mechanical hum
**Diegetic sound**: footsteps, door creaking, glass clinking, keyboard typing
**Voice style**: whisper, calm narration, energetic announcer, gravitas
**Music mood**: "soft piano in background", "upbeat electronic"

Put dialogue in quotation marks: `Character says: "Hello world."`

## Prompt document layers (repo `-生视频提示词.md`)

When authoring project prompt files, separate **human spec** from **model delivery text**:

| Layer | Examples | Goes in Seedance copy block? |
| --- | --- | --- |
| **`[H]` spec** | Speech-rate tables, upload asset matrix, acceptance checklist, fix playbook | **No** |
| **Delivery text** | Content inside `## Track N · Seedance copy block` fenced blocks | **Yes** |

### Delivery text: positive-only · no section headers

The copy block describes **what to generate**, not workflow rules or corrections from a prior draft.

**Structure (this repo):**

- **No `【…】` section headers** — no `【参考绑定】`, `【摄影·运镜】`, `【微动·A线】`, `【约束护栏】`, or beat label lines like `0.00-3.00秒·钩子【18字】`.
- **Bindings**: `@图片` / `@音频` lines at the top, **without** a header row.
- **Scene + camera + micro-motion**: merged into flowing direct-description sentences.
- **Beats**: each starts with **`X.XX至X.XX秒，`** then performance + `阿姨说` / `强哥说`.
- **Lip-sync lock**: one closing sentence `以上口型与台词一字不改：「…」` — not a standalone titled block.
- **Final line** (after lip-sync lock): `禁止字幕，禁止背景音乐，禁止水印。` — only these three output bans belong in the copy block; place at the end, not the top.

| Put in delivery text | Keep in `[H]` spec only |
| --- | --- |
| Final line `禁止字幕，禁止背景音乐，禁止水印。` (after lip-sync lock) | Other constraint rails piled in the middle of the block |
| Reference bindings (`@图片2 = …`) without header | "Do not upload @audio on this track" |
| Speaker voice as positive (`阿姨口播：四川话女声` / `强哥口播：四川话男声`) | Speech-rate math (`6字/秒含标点`, **15s 须 90～93 字**, `字数÷6`); "Do not imitate 强哥 voice" |
| 强哥 beat performance + `——四川话` after `强哥说` | `Character says` in English |
| On-screen state (`强哥后方嘴闭验厨`) | `【约束护栏】` sections |
| `0.00至3.00秒，阿姨说：「…」` timestamp beats | Beat label rows with word-count tags |
| `全员自然眨眼每3～5秒` woven into overview or beats | `【微动·A线】` header blocks |
| Beat-level performance + `says` lines | Revision notes targeting old mistakes |

**After a revision**, do not add negation lines that only make sense relative to an earlier wrong draft — the model never saw that draft. Express the intent positively (track 1: aunt VO only; track 2: bind `@音频1` for 强哥).

> Camera anchors in Chinese (`不切镜、不变焦`) belong in delivery text per repo rule. English POV templates in `seedance-2-0` are skill reference only — **not** pasted into copy blocks.

### Reference tags: once at the top only

Inside a delivery copy block, **`@图片` / `@音频` / `{{Mixed N}}` appear only in the opening reference-binding section** — once per asset. After that section (scene overview, camera, beats), describe subjects and settings **directly**; do not repeat `@` tags or phrases like "consistent with @图片2".

| Binding / overview (appearance once) | Later beats (role name only) |
| --- | --- |
| `@图片2 = 强哥五官脸型发型；五官脸型短发工服男，保持同一人物身份。` + 总述 `强哥（五官脸型短发工服男）…` | `强哥后方嘴闭验厨` / `强哥对镜说：「…」` |
| `@图片1 = 新华苑改完厨房…` | `改完厨房自然窗光，明亮整洁` |
| 首段定妆 `大哥（55至65岁短袖T恤男）` | 之后只写 `大哥` / `嘴闭` |

### Background reference (`@图片1`): bind only, do not describe

For environment/background reference images in `-生视频提示词.md` delivery blocks:

- **Binding line only:** `{{场景}}背景，全程不换景。` (e.g. `翻新厨房背景` · `厕所背景` · `小区大门背景`)
- **Do not** list colors, materials, appliances, tile patterns, or layout coordinates from the reference photo
- **`[H]` upload table** may name the file for humans; that detail does not go into the copy block
- **Staging beats** may name functional zones (淋浴隔间、玻璃门) for action — not a substitute for uploading `@图片1`

See `.cursor/rules/seedance-delivery-block.mdc` § **背景图 · 绑定铁律**.

**Identity:** anchor appearance **once** (binding + overview / first entrance); later beats use **role names** only — not full hair/clothing strings every beat, and not `@` tags.

### Repo delivery language: Chinese

For `-生视频提示词.md` in this workspace, **delivery copy blocks are fully Chinese** — camera, lip-sync, binding, beats. Map English Seedance vocabulary to Chinese (e.g. 缓慢推近 not `dolly in`, 阿姨说 not `Character says`). API params (`standard`, `generate_audio`) stay in `[H]` parameter tables only.

## Per-track logic checks (Spatial · POV · Continuation)

Run **once per track** before delivery — especially talk-multi, handheld selfie, and any clip that uses a continuation screenshot.

### Standalone paste test

The model receives **only that track's copy block + uploads**. It never sees other tracks or `[H]` spec tables.

| Fail if copy block contains… | Fix |
| --- | --- |
| Track labels (`轨1`, `上一段`, `末帧截图来源`) | Move workflow to `[H]` only |
| Speech-rate math (`6字/秒`, **15s = 90～93 字**) | Keep in `[H]` only |

### Continuation frame: trust the image

When `@图片N = 作为首帧` from a prior render screenshot:

- **Do not** re-describe characters already locked in the image (holder, background extras) — appearance may differ from track-1 script.
- **Do** describe **new** motion/dialogue only (e.g. 强哥 walks toward lens, speaks CTA).
- **Do not** re-upload redundant refs (portrait of holder, environment plate) if the screenshot already contains them.

### POV holder vs subject depth

Before writing spatial language, answer: **who holds the camera?**

| Holder | Other subject approaching lens | Wrong | Right |
| --- | --- | --- | --- |
| Aunt handheld selfie | 强哥 CTA | 占自拍前景 / 占主画面 | 自深景向镜头走来，至中近景对镜口播 |
| Tripod / crew camera | Hero walk-in | (context-dependent) | 可写占前景 / dolly |

Foreground in a selfie belongs to the **phone rig**, not a second person "taking over" the frame unless POV explicitly switches.

### Camera words must match POV

| POV | Use | Do not mix in |
| --- | --- | --- |
| Handheld selfie | 微晃、不推近、不变焦、机位固定手臂长度 | 缓慢推近、拉远、dolly、变焦 |
| Mounted / crew | dolly in/out, push-in, truck | handheld micro-shake without stating POV change |

Full checklist: `.cursor/rules/seedance-delivery-block.mdc` § **交付块逻辑自检**.

## What to Avoid

> **Replace emotional adjectives with the visual cause of the emotion.**
> - "sad character" → "tears on cheek, shoulders slumped, staring at empty chair"
> - "cinematic mood" → "low-key Rembrandt key + 35mm anamorphic + crushed shadows, lifted-by-2-stops shadow detail"
> - "epic" → "low-angle, 24mm wide, sun directly behind subject, lens flare on the rim"
>
> "Inspiring," "powerful," "moody," "epic" do not constrain pixels.

> **Static shot is strict.** A static shot has zero movement, zero focus change, zero zoom. If any of those occur, do NOT write "static camera" — pick the right movement primitive.

| Don't | Why | Do Instead |
|-------|-----|-----------|
| "Beautiful scene" | Too vague, no visual info | "Wet cobblestone street, warm streetlamp glow reflecting in puddles" |
| "Person moves quickly" | No visible action | "Woman sprints three steps and vaults over the railing" |
| "Cinematic look" | Every model already tries this | Specify: "anamorphic lens, shallow DOF, golden hour lighting" |
| "Sad character" | Internal states aren't visible | "Tears on cheek, shoulders slumped, staring at empty chair" |
| Readable text / logos | Models can't render text reliably | Avoid signs with text, or accept imperfect rendering |
| Complex physics | Chaotic motion causes artifacts | Keep physics simple; dancing/walking OK, explosions risky |
| Multiple characters talking | Multi-person dialogue breaks sync | One speaker per clip, or use reaction shots |
| Overloaded prompts | Too many elements = incoherent | Start simple, layer complexity one element at a time |
| Conflicting lighting | "Bright noon" + "dark shadows" | Pick one lighting setup and commit |

## Prompt Iteration Strategy

1. **Start simple** — subject + action + setting. See what the model gives you.
2. **Add one element at a time** — camera, then lighting, then style.
3. **If a shot misfires** — strip back. Freeze camera, simplify action, try again.
4. **For consistency across clips** — repeat the same style/lighting/grade description.
5. **Use seed values** — when you find a good result, save the seed for variations.
6. **For Grok reference-image video** — assign each source image a clear role in the prompt using `<IMAGE_1>`, `<IMAGE_2>`, etc.

## Example: Generic Prompt Template

```
[Shot]: Medium close-up, slight low angle
[Camera]: Slow dolly-in
[Subject]: A weathered fisherman in his 60s, salt-and-pepper beard,
           dark wool sweater, calloused hands gripping a rope
[Action]: He pulls the rope hand-over-hand, muscles straining,
          then pauses and looks out to sea
[Setting]: Wooden dock at dawn, calm grey ocean, distant fog bank,
           seagulls wheeling overhead
[Lighting]: Soft overcast with warm break in clouds on the horizon,
            gentle rim light from the rising sun
[Style]: Documentary cinematography, 35mm film grain,
         muted earth tones with a cold blue-grey palette
[Audio]: Rope creaking, water lapping, distant gull cries, wind
```
