# Wan2AI

**Universal AI agent skill for generating images, videos, audio, and music with 200+ local models.**

Install once, generate anywhere. Works with MiMoCode, Claude Code, Codex, Cursor, Gemini CLI, Hermes Agent, and any harness that supports the [Agent Skills specification](https://agentskills.io).

<p align="center">
  <img src="wangp/assets/wangp.svg" width="80" alt="Wan2AI">
</p>

---

## What It Does

| Capability | Models |
|---|---|
| **Generate images** | Flux 2 Dev, Qwen Image 2512, Z-Image, Krea 2, HiDream, Ideogram, Chroma |
| **Generate videos** | Wan 2.2, HunyuanVideo 1.5, LTX-2, Kandinsky 5, SkyReels, LongCat |
| **Edit images** | Flux Kontext, Qwen Edit, DreamOmni2, USO, UMO |
| **Edit videos** | Lucy Edit, Kiwi Edit, Chrono Edit, Vace, Ditto |
| **Animate characters** | Multitalk, Infinitetalk, Hunyuan Avatar, SCAIL, Steady Dancer, Ovi |
| **Generate speech** | IndexTTS2, Chatterbox, Qwen3 TTS, OmniVoice, KugelAudio |
| **Create music** | ACE-Step, Stable Audio 3, HeartMuLa |

### Key Features

- **Hardware-aware** — auto-detects GPU/VRAM and recommends models that actually fit
- **Model-specific prompting** — each model family has different conventions; the agent knows them all
- **Auto-presets** — Lightning LoRAs for Qwen, Turbo LoRAs for Flux, applied automatically
- **OOM recovery** — detects out-of-memory errors and falls back to smaller models or fewer steps
- **Browser gallery** — live image viewer with auto-refresh, history, and zoom
- **Auto-install** — if Wan2GP isn't found, offers to install it via Pinokio headlessly

---

## Quick Start

### 1. Install the Skill

```bash
npx skills add PrimeEcto/Wan2AI -g
```

That's it. The skill is now available to all supported AI agents on your system.

### 2. Use It

Open your AI agent and ask it to generate something:

```
"Generate an image of a red fox in a snowy forest"
```
```
"Make a video of a sunset over the ocean with cinematic camera movement"
```
```
"Create a talking head video from this portrait"
```
```
"Generate a lo-fi hip hop beat"
```

The agent handles everything: hardware detection, model selection, prompt adaptation, generation, and display.

---

## Wan2GP Setup

Wan2AI uses [Wan2GP](https://github.com/DeepBeepMeep/Wan2GP) as its generation engine. You have three options:

### Option A: Let the Agent Install It

If Wan2GP isn't installed, the agent will detect this and offer to install it automatically via [Pinokio](https://pinokio.computer)'s headless CLI:

```
"Wan2GP is not installed. I can install it automatically via Pinokio. Want me to proceed?"
```

If you say yes, it runs:
```bash
npm install -g pinokio
pinokio download https://github.com/6Morpheus6/wan2gp
pinokio run ~/.pinokio/api/wan2gp/install.js
```

This handles all dependencies, GPU setup, CUDA/torch installation, and model downloads — zero manual configuration.

### Option B: Install Wan2GP via Pinokio (GUI)

1. Download [Pinokio](https://pinokio.computer)
2. Search for **Wan2GP** and click Install
3. Launch Wan2GP from Pinokio

### Option C: Manual Installation

Follow the [Wan2GP README](https://github.com/DeepBeepMeep/Wan2GP). Requires Python 3.10+, CUDA (NVIDIA), ROCm (AMD), or MPS (Apple Silicon).

---

## How It Works

```
wangp/
├── SKILL.md                    # Agent workflow + design principles
├── agents/openai.yaml          # UI metadata
├── scripts/
│   ├── wangp.py                # Python CLI wrapping Wan2GP's API
│   └── viewer/
│       ├── server.py           # Gallery HTTP server with SSE
│       ├── gallery.html        # Dark-themed gallery UI
│       └── start.sh            # Start script
└── references/
    ├── model-catalog.md        # 200+ models organized by task
    ├── prompting.md            # Per-family prompt conventions
    └── hardware.md             # GPU profiles and VRAM recommendations
```

The Python CLI (`wangp.py`) wraps Wan2GP's existing in-process API — no extra servers, no MCP dependencies, no code duplication.

### CLI Reference

```bash
# Detect hardware, Wan2GP version, and all installations
python scripts/wangp.py detect

# List 200+ models with optional filters
python scripts/wangp.py list --family flux
python scripts/wangp.py list --available

# Get default settings for a model
python scripts/wangp.py defaults qwen_image_2512_20B

# Generate with preset LoRA and gallery output
python scripts/wangp.py generate \
  --model qwen_image_2512_20B \
  --prompt "a red fox in snow" \
  --lora "https://huggingface.co/DeepBeepMeep/Qwen_image/resolve/main/loras_accelerators/Qwen-Image-2512-Lightning-4steps-V1.0-bf16.safetensors" \
  --output-dir /tmp/wangp-gallery \
  --show

# Upscale an existing image
python scripts/wangp.py upscale image.jpg --method lanczos2

# Check for Wan2GP updates
python scripts/wangp.py update
```

---

## Browser Gallery

Wan2AI includes a built-in image gallery that opens in your browser. Images appear automatically as they're generated — no manual refresh needed.

```
Agent: "Would you like a live gallery in your browser?"
User:  "Yes"
Agent: *starts server, opens browser*
       *all generations stream to gallery automatically*
```

**Features:**
- Live auto-refresh with toast notifications for new images
- Gallery history with clickable thumbnails
- Click to zoom, arrow keys to navigate
- Image dimensions and filename metadata
- Dark theme optimized for viewing generated images
- Keyboard shortcuts: `←` `→` navigate, `Space` zoom, `Esc` close

---

## Supported Models (Highlights)

### Image Generation (12GB VRAM recommended tier)

| Model | Params | Steps | Best For |
|---|---|---|---|
| `qwen_image_2512_20B` + Lightning | 20B | 4 | Text rendering + realism |
| `krea2_turbo` | ~12B | 8 | Aesthetic photography |
| `ideogram4` + Turbo | 9.3B | 12 | Typography, layouts |
| `z_image` | 6B | 8 | Fast generation |
| `flux` + Turbo Alpha | 12B | 10 | General purpose |
| `flux2_klein_9B` | 9B | 4 | Fast distilled Flux 2 |

### Video Generation

| Model | Params | Steps | Best For |
|---|---|---|---|
| `t2v_sf` (Lightning) | 14B | 4 | Fast text-to-video |
| `t2v_2_2` | 14B | 30 | Best quality T2V |
| `ltx2_22B_distilled` | 22B | 8 | Fast with audio |
| `hunyuan_1_5_t2v` | 8B | 30 | Lower VRAM |
| `i2v_2_2` | 14B | 30 | Image-to-video |

See [references/model-catalog.md](wangp/references/model-catalog.md) for the complete 200+ model list.

---

## Auto-Presets

The agent automatically applies acceleration LoRAs when you request specific models:

| Request | Preset Applied | Steps |
|---|---|---|
| Qwen Image (any) | `qwen_image_2512_20B` + Lightning 4-step LoRA | 4 |
| Qwen Image (OOM) | Fallback to Lightning 8-step LoRA | 8 |
| Flux 2 Dev 32B | Turbo LoRA from HuggingFace | 8 |
| Flux 1 (any) | Turbo Alpha LoRA | 10 |
| Krea 2 | `krea2_turbo` (distilled) | 8 |
| Ideogram | Turbo preset | 12 |

If a generation runs out of memory, the agent detects it and automatically retries with a smaller model or fewer steps.

---

## Hardware Requirements

| VRAM | What You Can Run |
|---|---|
| **24 GB+** | Everything at full quality |
| **16 GB** | Most models with int8 quantization |
| **12 GB** | Image models (Qwen Lightning, Z-Image, Krea 2 Turbo), 14B video with int8 |
| **8 GB** | 1.3B video models, GGUF variants, small image models |
| **6 GB** | GGUF Q4 only |

The agent auto-detects your hardware and picks models that fit.

---

## Agent Support

Wan2AI works with any agent that supports the [Agent Skills specification](https://agentskills.io):

| Agent | Install Command |
|---|---|
| MiMoCode | `npx skills add PrimeEcto/Wan2AI -g` |
| Codex | `npx skills add PrimeEcto/Wan2AI -g` |
| Claude Code | `npx skills add PrimeEcto/Wan2AI -g` |
| Cursor | `npx skills add PrimeEcto/Wan2AI -g` |
| Gemini CLI | `npx skills add PrimeEcto/Wan2AI -g` |
| Hermes Agent | `npx skills add PrimeEcto/Wan2AI -g` |
| Cline | `npx skills add PrimeEcto/Wan2AI -g` |
| Roo Code | `npx skills add PrimeEcto/Wan2AI -g` |
| GitHub Copilot | `npx skills add PrimeEcto/Wan2AI -g` |
| OpenCode | `npx skills add PrimeEcto/Wan2AI -g` |

Use `-g` for global installation (available to all agents).

---

## Troubleshooting

| Problem | Solution |
|---|---|
| "Wan2GP not found" | Let the agent install it via Pinokio, or set `WAN2GP_ROOT` env var |
| "Unknown model" | Run `python scripts/wangp.py list` to see all 200+ models |
| Out of memory | Agent auto-detects OOM and retries with smaller model. Or use `z_image`, `flux2_klein_4B` |
| Slow generation | Use distilled variants: `t2v_sf`, `krea2_turbo`, `ltx2_22B_distilled` |
| Gallery not opening | Check that port isn't blocked. Server runs on `127.0.0.1` by default |
| Update available | Agent detects and offers to run `python scripts/wangp.py update` |

---

## License

MIT
