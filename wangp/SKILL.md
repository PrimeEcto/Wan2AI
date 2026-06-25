---
name: wangp
description: "Generate images and videos using local AI models via Wan2GP. Use when the user wants to create images, videos, animations, or audio with local diffusion models (Flux, Wan, Hunyuan, LTX, Qwen, Z-Image, etc.). Triggers on requests like 'generate an image', 'make a video', 'create an animation', 'text to image', 'text to video', or any local media generation task using Wan2GP."
---

# Wan2GP Skill

Generate images and videos locally using Wan2GP's 200+ AI models. Covers text-to-image, image-to-video, text-to-video, image editing, character animation, TTS, and music generation.

## Prerequisites

- Wan2GP installed (via Pinokio or standalone)
- Python environment with Wan2GP dependencies

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
