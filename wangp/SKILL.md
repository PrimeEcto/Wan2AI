---
name: wangp
description: "Generate images and videos using local AI models via Wan2GP. Use when the user wants to create images, videos, animations, or audio with local diffusion models (Flux, Wan, Hunyuan, LTX, Qwen, Z-Image, etc.). Triggers on requests like 'generate an image', 'make a video', 'create an animation', 'text to image', 'text to video', or any local media generation task using Wan2GP."
---

# Wan2GP Skill

Generate images and videos locally using Wan2GP's 200+ AI models. Covers text-to-image, image-to-video, text-to-video, image editing, character animation, TTS, and music generation.

## Prerequisites

- Wan2GP installed (via Pinokio or standalone)
- Python environment with Wan2GP dependencies

## Image Display Preference (per session)

On the FIRST generation in a session, ask the user:

> "Do you want generated images displayed in the terminal after each generation?"

- **If yes**: Remember this for the rest of the session. Before the first `--show` usage, check if a terminal image viewer is installed. If not, auto-install one:
  - Try `cargo install viu` (if cargo is available)
  - Else try `pip install viuer` + use Python PIL fallback
  - Else try `apt install chafa` / `brew install chafa` (platform-dependent)
  - After install, verify it works with `which viu` or `which chafa`
- **If no**: Never use `--show`. Just report file paths.
- **Only stop showing** if the user explicitly says "don't show images", "stop displaying", or similar. Do NOT stop based on inference or silence.
- When showing is enabled, ALWAYS pass `--show` to `generate` calls and use `show` for any file path the user asks about.

## Displaying Results

Generated images can be displayed directly:

```bash
# Show an existing file
python scripts/wangp.py show path/to/image.jpg

# Generate and show immediately
python scripts/wangp.py generate --model z_image --prompt "a red fox" --show
```

Display methods (tried in order):
1. `viu` — fast Rust terminal image viewer (recommended: `cargo install viu`)
2. `chafa` — versatile terminal viewer (`apt install chafa` / `brew install chafa`)
3. `timg` — terminal media viewer
4. iTerm2 / Kitty inline image protocol (automatic)
5. Sixel via `img2sixel`
6. PIL fallback — opens in default OS image viewer

## Workflow

### Step 1: Detect Hardware

```bash
python scripts/wangp.py detect
```

Returns JSON with GPU, VRAM, RAM, recommended profile, and suitable model sizes. Use this to guide model selection.

### Step 2: Choose a Model

Read `references/model-catalog.md` to match user intent to a `model_type`. Key decision factors:

1. **Task type**: What does the user want? (image, video, edit, animate, TTS, music)
2. **Hardware**: What does `detect` report? Match VRAM to model size.
3. **Speed vs quality**: Lightning/distilled variants are faster; base models are higher quality.

For quick reference:
- **Best images**: `flux` (12B), `qwen_image_20B` (20B), `hidream_o1` (10B)
- **Fast images**: `z_image` (6B, 8 steps), `flux_schnell` (12B, fast)
- **Best video**: `t2v` or `t2v_2_2` (Wan 14B), `hunyuan` (13B)
- **Fast video**: `t2v_sf` (Lightning), `ltx2_22B_distilled` (8 steps)
- **Low VRAM**: `t2v_1.3B`, GGUF variants, `z_image`

### Step 3: Get Default Settings

```bash
python scripts/wangp.py defaults <model_type>
```

Returns the model's default settings (resolution, steps, etc.). Use as baseline.

### Step 4: Adapt the Prompt

Read `references/prompting.md` for model-specific prompt guidance. Each model family has VERY different conventions:

- **Flux**: Short, direct — "draw a hat", "add a hat" (editing). Don't write paragraphs.
- **Z-Image**: Concise 1-2 sentences. Uses NAG (guidance_scale=0). Don't write long descriptions.
- **Qwen Image**: Short instructions for editing, or detailed text for text-in-image rendering.
- **HiDream**: More descriptive — include subject, action, environment, style details.
- **Ideogram**: UNIQUE JSON FORMAT with `aspect_ratio`, `high_level_description`, `compositional_deconstruction`. Not plain text.
- **Wan T2V**: Detailed cinematic narrative with camera motion, character actions, environment.
- **LTX**: VERBOSE screenplay format (200+ words) with dialogue in quotes, camera directions, character emotions.
- **HunyuanVideo**: Similar to Wan — detailed cinematic narrative.
- **Lucy/Kiwi Edit**: Short imperative commands — "change the clothes to red", "Remove the monkey."
- **IndexTTS2**: Emotion tags `[happy]`, `[sadness]` with `Speaker 1:` prefixes.
- **Ovi**: Scene description with `<S>` and `<E>` tags marking speech segments.
- **Music (ACE-Step)**: Song structure tags `[Verse]`, `[Chorus]` with lyrics.

### Step 5: Generate

```bash
python scripts/wangp.py generate --model <type> --prompt "..." [options]
```

**Options**:
- `--resolution WxH` (e.g., 1280x720)
- `--steps N` (inference steps)
- `--seed N` (reproducibility, -1 for random)
- `--frames N` (video frame count)
- `--image PATH` (start image for I2V/I2I)
- `--negative TEXT` (negative prompt)
- `--guidance-scale F` (prompt adherence)
- `--output-dir DIR` (output location)
- `--attention MODE` (sdpa/sage/sage2/flash)
- `--profile N` (1-5, performance profile)
- `--show` (display image after generation)

**Output**: JSON with `success`, `generated_files` (paths), and any errors.

### Step 6: Report Results

Report the output file paths to the user. If generation failed, check the error message and suggest fixes (lower resolution, different model, fewer frames).

## Multi-Step Workflows

**Image → Video**: Generate image first, then animate:
```bash
# Generate image
python scripts/wangp.py generate --model flux --prompt "A red fox in a forest" --output-dir ./output
# Animate it
python scripts/wangp.py generate --model i2v_2_2 --prompt "The fox walks forward" --image ./output/fox.png
```

**Image → Edit**: Generate then edit:
```bash
python scripts/wangp.py generate --model flux --prompt "A portrait"
python scripts/wangp.py generate --model flux_dev_kontext --prompt "Add sunglasses" --image ./output/portrait.png
```

**Video → Audio**: Generate video then add audio:
```bash
python scripts/wangp.py generate --model t2v --prompt "A person talking"
# Then use TTS or audio model separately
```

## Image Editing Workflows

For models that support both generation AND editing, the key is setting the right image input:

**Flux Kontext** (instruction-based editing):
```bash
python scripts/wangp.py generate --model flux_dev_kontext --prompt "add sunglasses" --image ./portrait.png
```
Prompt = short edit instruction. Image = source to edit.

**Flux USO** (style transfer):
```bash
python scripts/wangp.py generate --model flux_dev_uso --prompt "a portrait in watercolor style" --image ./style_ref.png
```
Prompt = desired output description. Image = style reference.

**Qwen Image Edit**:
```bash
python scripts/wangp.py generate --model qwen_image_edit_plus_20B --prompt "add the text HELLO at the top" --image ./source.png
```
Prompt = edit instruction. Supports text rendering in edits.

**Lucy Edit** (video editing):
```bash
python scripts/wangp.py generate --model lucy_edit --prompt "change the clothes to red" --image ./video.mp4
```
Prompt = short imperative command. Image input = source video.

**Kiwi Edit** (video editing with reference):
```bash
python scripts/wangp.py generate --model kiwi_edit --prompt "Change the dress to match the reference while preserving pose and lighting" --image ./video.mp4
```
Prompt = edit instruction with preservation clause.

## Error Recovery

- **"Wan2GP not found"**: Set `WAN2GP_ROOT` env var or install Wan2GP
- **"Unknown model"**: Run `python scripts/wangp.py list` to see available models
- **OOM / out of memory**: Lower resolution, fewer frames, use int8/GGUF variant, or smaller model
- **Slow generation**: Use Lightning/distilled variants, reduce steps
- **Poor quality**: Increase steps, use negative prompt, try larger model

## When to Use

- User wants to generate images locally (not via API)
- User wants to generate videos from text or images
- User wants to edit images/videos with AI
- User wants local TTS or music generation
- User has Wan2GP installed

## When Not to Use

- User wants cloud-based generation (use imagegen skill instead)
- User doesn't have Wan2GP installed
- User wants to edit SVG/vector/code-native assets

## Reference Map

- `references/model-catalog.md`: Full model list organized by task type
- `references/prompting.md`: Per-family prompt guidance
- `references/hardware.md`: GPU profiles, VRAM recommendations, quantization options
- `scripts/wangp.py`: CLI tool for Wan2GP interaction
