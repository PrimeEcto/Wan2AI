---
name: wangp
description: "Generate images and videos using local AI models via Wan2GP. Use when the user wants to create images, videos, animations, or audio with local diffusion models (Flux, Wan, Hunyuan, LTX, Qwen, Z-Image, etc.). Triggers on requests like 'generate an image', 'make a video', 'create an animation', 'text to image', 'text to video', or any local media generation task using Wan2GP."
---

# Wan2GP Skill

Generate images and videos locally using Wan2GP's 200+ AI models. Covers text-to-image, image-to-video, text-to-video, image editing, character animation, TTS, and music generation.

## Prerequisites

- **Wan2GP**: The skill checks for Wan2GP on first use. If not found, it offers to install automatically via Pinokio's headless CLI (recommended). Manual install also works: https://github.com/DeepBeepMeep/Wan2GP
- **Pinokio** (optional, for auto-install): `npm install -g pinokio` — the skill can install this automatically if needed.

## Image Display and User Interaction (per harness)

### Displaying Images

Different harnesses display images differently. Use the method appropriate for your environment:

**MiMoCode / Codex / Claude Code** (has `Read` tool for images):
- After generation, use the `Read` tool on the generated image file path. The tool will display the image inline in the conversation.
- Do NOT use `--show` or `viu` — the `Read` tool handles display natively.
- Example: After `wangp.py generate` returns a path, call `Read(path="/path/to/image.jpg")`.

**Cursor / VS Code extensions (Cline, Roo, GitHub Copilot)** (IDE-based):
- Images display inline in the IDE chat panel when referenced.
- After generation, tell the user the file path. The IDE may auto-preview images in the workspace.
- For explicit display, use `Read` tool if available, or mention the path so the user can click to open.

**Terminal-based agents (Gemini CLI, OpenCode, Warp, Hermes Agent, etc.)**:
- Use `--show` flag on `generate` to display via `viu`/`chafa`.
- Auto-install `viu` if needed: `cargo install viu` or `apt install chafa`.
- Fallback: report the file path and let the user open it.

**General rule**: If the harness has a `Read` tool that supports images, prefer that over `--show`. If not, use `--show` with a terminal image viewer.

### Asking User Questions

Different harnesses have different mechanisms for asking the user questions:

**MiMoCode / Codex** (has `question` tool):
- Use the `question` tool for structured questions with predefined options.
- Example for display preference:
  ```
  question(questions=[{
    question: "Do you want generated images displayed after each generation?",
    header: "Image display",
    options: [
      {label: "Yes, show images", description: "Display images in terminal after each generation"},
      {label: "No, just paths", description: "Only report the file path"}
    ]
  }])
  ```
- Use `question` tool for model selection, upscaling method choice, resolution selection, etc.

**Claude Code** (conversational):
- Ask questions directly in conversation. Claude Code does not have a structured question tool.
- Present options as a numbered list and ask the user to pick.

**Cursor / VS Code extensions**:
- Ask questions in the chat panel. Present options as a numbered or bulleted list.

**Hermes Agent** (has `Clarify` function):
- Use Hermes Agent's native `Clarify` function for structured questions when available.
- Fall back to conversational questions if Clarify is not accessible.

**Other harnesses**:
- Ask questions conversationally in the chat.
- Present options as a numbered list.
- Keep questions concise — most harnesses don't have structured input mechanisms.

### Harness-Specific Capabilities

| Harness | Image Display | Question Method | Special |
|---|---|---|---|
| MiMoCode | `Read` tool | `question` tool | Hooks, tools, TUI plugins |
| Codex | `Read` tool | `question` tool | MCP, plugins, marketplace |
| Claude Code | `Read` tool | Conversational | `context: fork`, hooks, MCP |
| Cursor | IDE chat panel | Conversational | IDE integration |
| Cline | IDE chat panel | Conversational | Browser automation, MCP |
| Roo Code | IDE chat panel | Conversational | Multi-mode agent |
| GitHub Copilot | VS Code chat | Conversational | VS Code integration |
| Gemini CLI | Terminal (`--show`) | Conversational | Open source |
| OpenCode | Terminal (`--show`) | Conversational | Open source |
| Hermes Agent | Terminal (`--show`) | `Clarify` function | Structured input |
| Warp | Terminal (`--show`) | Conversational | Terminal integration |
| Kiro CLI | IDE panel | Conversational | Spec-driven dev |
| Goose | Terminal (`--show`) | Conversational | MCP extensible |

## Displaying Results

For harnesses with a `Read` tool that supports images (MiMoCode, Codex, Claude Code): use `Read` on the generated file path. Do NOT use `--show`.

For terminal-based harnesses (Gemini CLI, OpenCode, Warp, Hermes Agent): use `--show` flag or `show` subcommand:

```bash
python scripts/wangp.py generate --model z_image --prompt "a red fox" --show
python scripts/wangp.py show path/to/image.jpg
```

Terminal display methods (tried in order):
1. `viu` — fast Rust terminal image viewer (recommended: `cargo install viu`)
2. `chafa` — versatile terminal viewer (`apt install chafa` / `brew install chafa`)
3. `timg` — terminal media viewer
4. iTerm2 / Kitty inline image protocol (automatic)
5. Sixel via `img2sixel`
6. PIL fallback — opens in default OS image viewer

## Workflow

### IMPORTANT: Transparency First

Before doing ANYTHING, tell the user what you're about to do. The skill runs detection, reads Wan2GP files, and calls its API — this can look suspicious if unexplained. Always start with a brief explanation like:

> "I'll set up Wan2GP for you. First I need to detect your hardware and check the Wan2GP installation."

If the user hasn't used this skill before, explain the full workflow upfront:

> "Here's what I'll do: detect your GPU/VRAM, recommend the best model, adapt the prompt for that model, generate the media, and optionally display it."

Never silently start reading Wan2GP files or running commands without context.

### Step 0: Check Wan2GP Installation

**Before running detect**, ask the user if they want the agent to search for Wan2GP. Searching scans multiple drives and costs context/tokens. Give them these options:

> "I need to find your Wan2GP installation. How would you like to proceed?"
>
> 1. **Search for it** — I'll scan your drives to find the best Wan2GP install (uses some tokens)
> 2. **I'll navigate there myself** — Close this and run your CLI/harness from the Wan2GP directory directly
> 3. **I don't have Wan2GP** — Install it automatically via Pinokio

(Use the `question` tool for MiMoCode/Codex, numbered list for other harnesses.)

**If user chooses "Search for it"**:
```bash
python scripts/wangp.py detect
```

The `detect` output includes `wan2gp_version`, `wan2gp_update_available`, `python_env_ok`, and if multiple installs exist, `all_installations` showing all found paths with maturity scores. The highest-scored install is automatically selected.

**If Wan2GP is fully working** (version detected, python_env_ok=true):
- Check `wan2gp_update_available`. If true, tell the user: "Wan2GP has an update available (current: X, latest: Y). Want me to update it?"
- If they say yes: `python scripts/wangp.py update`
- Proceed to Step 1.

**If Wan2GP is NOT found or NOT working** (detect fails, python_env_ok=false, missing dependencies):

Do NOT try to manually install Wan2GP dependencies (pip install diffusers, torch, etc.). This wastes tokens and time. Instead, offer to install via Pinokio's headless CLI:

> "Wan2GP is not installed or not set up. I can install it automatically via Pinokio's headless CLI, which handles all dependencies, GPU setup, and model downloads. Want me to proceed?"

If they say yes, run these 3 steps in order:

```bash
# 1. Install Pinokio core headlessly (skip if already installed)
npm install -g pinokio

# 2. Download Wan2GP into Pinokio's app cache
pinokio download https://github.com/6Morpheus6/wan2gp

# 3. Run Wan2GP's install script (handles venv, CUDA, torch, all deps)
pinokio run ~/.pinokio/api/wan2gp/install.js
```

After install completes, set `WAN2GP_ROOT` and re-run `detect`:
```bash
export WAN2GP_ROOT=~/.pinokio/api/wan2gp/app
python scripts/wangp.py detect
```

**If the user declines Pinokio install**, tell them:
> "You can also install Wan2GP manually from https://github.com/DeepBeepMeep/Wan2GP. Once installed, set WAN2GP_ROOT to the app directory."

Do NOT attempt manual pip/conda installs. Do NOT read Wan2GP source files to "figure out" the installation. Either use Pinokio or let the user handle it manually.

**If user chooses "I'll navigate there myself"**:
> "No problem. Navigate to your Wan2GP directory in your terminal, then launch your CLI/harness from there. The skill will find Wan2GP automatically when you run it from that directory."

Do NOT search. Do NOT run detect. Stop here and let the user handle it.

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

#### IMAGE GENERATION HIERARCHY (best first, by hardware tier)

**12GB VRAM (RTX 4070, 3060 12GB, etc.) — your default tier:**
1. `qwen_image_2512_20B` — Best text rendering + realism. USE LIGHTNING PRESET (see below).
2. `krea2_turbo` — Best aesthetics, 8 steps, fast.
3. `ideogram4` — Best for typography/layout. USE TURBO PRESET (12 steps).
4. `z_image` — Fastest, 8 steps, NAG-guided.
5. `flux` with Turbo Alpha LoRA — Good general purpose, 10 steps.
6. `flux2_klein_9B` — Distilled Flux 2, 4 steps, very fast.
7. `hidream_o1_dev` — Distilled, 28 steps.

**16GB+ VRAM:**
- All above at higher quality + `flux2_dev` (32B with INT8)
- `krea2_raw` (52 steps, maximum quality)
- `hidream_o1` (50 steps, full quality)

**8GB VRAM:**
- `z_image` with INT8, `flux2_klein_4B`, `flux_schnell`

#### VIDEO GENERATION HIERARCHY

**12GB VRAM:**
1. `t2v_sf` — Wan Lightning, 4 steps, fastest T2V
2. `t2v_fusionix` — FusioniX, 8 steps, good motion
3. `ltx2_22B_distilled` — LTX-2 distilled, 8 steps, with audio
4. `t2v_1.3B` — Lightweight Wan, 30 steps
5. `hunyuan_1_5_480_t2v` — Hunyuan 1.5 480p, 30 steps

**16GB+ VRAM:**
- `t2v` or `t2v_2_2` — Full Wan 14B, 30 steps (best quality)
- `hunyuan` — HunyuanVideo 13B
- `ltx2_22B` — Full LTX-2 22B

#### CRITICAL: MODEL-SPECIFIC PRESETS

**When user asks for Qwen Image (any variant):**
- ALWAYS use `qwen_image_2512_20B` (latest release, not the older `qwen_image_20B`)
- Apply Lightning preset by adding to settings:
  ```json
  "activated_loras": ["https://huggingface.co/DeepBeepMeep/Qwen_image/resolve/main/loras_accelerators/Qwen-Image-2512-Lightning-4steps-V1.0-bf16.safetensors"],
  "loras_multipliers": "1",
  "num_inference_steps": 4,
  "guidance_scale": 1
  ```
- If 4-step gives OOM, try 8-step preset instead:
  ```json
  "activated_loras": ["https://huggingface.co/DeepBeepMeep/Qwen_image/resolve/main/loras_accelerators/Qwen-Image-2512-Lightning-8steps-V1.0-bf16.safetensors"],
  "num_inference_steps": 8
  ```

**When user asks for Flux 2 Dev 32B:**
- Model type: `flux2_dev`
- Apply Turbo LoRA for 8-step generation:
  ```json
  "activated_loras": ["https://huggingface.co/fal/FLUX.2-dev-Turbo/resolve/main/flux.2-turbo-lora.safetensors"],
  "loras_multipliers": "1",
  "num_inference_steps": 8
  ```
- If OOM, fall back to `flux2_klein_9B` (distilled, 4 steps, much less VRAM)

**When user asks for Flux 1 (any variant):**
- Apply Turbo Alpha LoRA for 10-step generation:
  ```json
  "activated_loras": ["https://huggingface.co/DeepBeepMeep/Flux/resolve/main/loras_accelerators/FLUX.1-Turbo-Alpha.safetensors"],
  "loras_multipliers": "1",
  "num_inference_steps": 10,
  "embedded_guidance_scale": 3.5
  ```

**When user asks for Ideogram:**
- Default is 20 steps. For faster: use Turbo preset (12 steps).
- Model type: `ideogram4` (FP8, 9.3B)

**When user asks for Krea 2:**
- Use `krea2_turbo` (8 steps) by default, not `krea2_raw` (52 steps)

#### OOM DETECTION AND RECOVERY

If generation fails with OOM (out of memory), CUDA error, or killed signal:
1. Tell the user: "Generation ran out of memory. Let me try a smaller model/fewer steps."
2. If using Qwen 2512 4-step → try 8-step preset
3. If using Flux 2 Dev 32B → fall back to `flux2_klein_9B`
4. If using any 14B+ model → try the 1.3B or distilled variant
5. Lower resolution: 1280x720 → 832x480
6. If still failing: suggest a fundamentally smaller model (Z-Image, Flux 2 Klein 4B)
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
- `--upscale METHOD` (spatial upsampling during generation, e.g. `lanczos2`, `flashvsr2`, `coz4`)
- `--show` (display image after generation)

**Output**: JSON with `success`, `generated_files` (paths), and any errors.

### Step 6: Report Results

Report the output file paths to the user. If generation failed, check the error message and suggest fixes (lower resolution, different model, fewer frames).

## Upscaling

### Upscale During Generation

Add `--upscale` to any generate call to upscale the output immediately:

```bash
python scripts/wangp.py generate --model z_image --prompt "a red fox" --upscale lanczos2 --show
python scripts/wangp.py generate --model t2v --prompt "a sunset" --upscale flashvsr2
```

### Upscale an Existing Image/Video

Use the `upscale` subcommand to upscale any existing file:

```bash
python scripts/wangp.py upscale path/to/image.jpg --method lanczos2 --show
python scripts/wangp.py upscale path/to/video.mp4 --method flashvsr2
```

### Upscaling Methods

| Method | Scale | Media | GPU Required | Notes |
|---|---|---|---|---|
| `lanczos2` - `lanczos4` | 2-4x | image+video | No | Fast, basic quality. Good for quick upscaling. |
| `flashvsr2` - `flashvsr4` | 2-4x | image+video | Yes (Triton) | AI upscaling, much better quality. |
| `flashvsr2pass2` - `flashvsr2pass4` | 2-4x | image+video | Yes | Two-pass FlashVSR, reduces banding. |
| `coz2` - `coz16` | 2-16x | image only | Yes | Chain-of-Zoom, extreme upscaling. |
| `flux_pid4` | 4x | image only | Yes | PiD upscaler with Flux backbone. |
| `vae2` | 2x | during gen only | Yes | VAE-integrated, generation-time only. |

**Recommended**:
- Quick/lossless: `lanczos2`
- Best quality video: `flashvsr2` or `flashvsr2pass2`
- Best quality image: `flux_pid4` or `coz4`
- Extreme upscaling: `coz8` or `coz16`

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
