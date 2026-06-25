# Wan2AI

**Universal AI agent skill for generating images, videos, audio, and music using local AI models via [Wan2GP](https://github.com/DeepBeepMeep/Wan2GP).**

Install once, generate anywhere — works with MiMoCode, Claude Code, Codex, Cursor, Gemini CLI, and any agent that supports the [Agent Skills specification](https://agentskills.io).

---

## What It Does

Wan2AI gives AI agents the ability to:

| Capability | Models |
|---|---|
| **Generate images** | Flux, Qwen Image, Z-Image, HiDream, Ideogram, Krea, Chroma |
| **Generate videos** | Wan 2.1/2.2, HunyuanVideo, LTX-Video, Kandinsky, SkyReels, LongCat |
| **Edit images** | Flux Kontext, Qwen Edit, DreamOmni2, USO, UMO |
| **Edit videos** | Lucy Edit, Kiwi Edit, Chrono Edit, Vace, Ditto |
| **Animate characters** | Multitalk, Infinitetalk, Hunyuan Avatar, SCAIL, Steady Dancer, Ovi |
| **Generate speech** | IndexTTS2, Chatterbox, Qwen3 TTS, OmniVoice, KugelAudio |
| **Create music** | ACE-Step, Stable Audio 3, HeartMuLa |

Over **200 models** with hardware-aware selection, model-specific prompting guidance, and automatic terminal image display.

---

## Prerequisites

### 1. Install Wan2GP

Wan2AI requires [Wan2GP](https://github.com/DeepBeepMeep/Wan2GP) to be installed and working.

**Recommended: Install via [Pinokio](https://pinokio.computer)**

Pinokio is the simplest way to get Wan2GP running. It handles all dependencies, GPU setup, and model downloads automatically:

1. Download and install [Pinokio](https://pinokio.computer)
2. Search for **Wan2GP** in the Pinokio app
3. Click **Install** — Pinokio handles everything
4. Launch Wan2GP from Pinokio when you want to use it

**Alternative: Manual installation**

Follow the [Wan2GP README](https://github.com/DeepBeepMeep/Wan2GP) for manual setup. Requires Python 3.10+, CUDA (NVIDIA), ROCm (AMD), or MPS (Apple Silicon).

### 2. Install the Skill

```bash
npx skills add PrimeEcto/Wan2AI
```

That's it. The skill is now available to all supported AI agents on your system.

---

## Usage

Once installed, just ask your AI agent to generate something:

```
"Generate an image of a red fox in a snowy forest"
```
```
"Make a video of a sunset over the ocean"
```
```
"Create a talking head video from this portrait"
```
```
"Generate a lo-fi hip hop beat"
```

The agent will:
1. Detect your hardware (GPU, VRAM, RAM)
2. Recommend the best model for your system
3. Adapt the prompt to the model's conventions
4. Generate the media
5. Display the result in your terminal (if you opt in)

### What the Agent Handles

- **Hardware detection**: Automatically selects models that fit your VRAM
- **Model-specific prompting**: Each model family has different conventions — the agent knows them all
- **Image editing workflows**: Properly chains generation → editing pipelines
- **Terminal display**: Shows generated images directly in your terminal

---

## How It Works

Wan2AI is a [universal agent skill](https://agentskills.io) consisting of:

```
wangp/
├── SKILL.md              # Agent workflow instructions
├── agents/openai.yaml    # UI metadata
├── scripts/wangp.py      # Python CLI wrapping Wan2GP's API
└── references/
    ├── model-catalog.md  # 200+ models organized by task
    ├── prompting.md      # Per-family prompt conventions
    └── hardware.md       # GPU profiles and VRAM recommendations
```

The Python CLI (`wangp.py`) wraps Wan2GP's existing in-process API — no extra servers, no MCP dependencies, no code duplication. It:

- Auto-discovers your Wan2GP installation
- Auto-detects your hardware via Wan2GP's `setup.py`
- Re-execs in Wan2GP's Python environment if needed
- Outputs clean JSON for agent consumption

### CLI Commands

```bash
# Detect hardware and recommend settings
python scripts/wangp.py detect

# List available models (200+)
python scripts/wangp.py list
python scripts/wangp.py list --family flux
python scripts/wangp.py list --available

# Get default settings for a model
python scripts/wangp.py defaults z_image

# Get full model schema
python scripts/wangp.py schema flux_dev_kontext

# Generate with auto-display
python scripts/wangp.py generate --model z_image --prompt "a red fox" --show

# Display any image in terminal
python scripts/wangp.py show path/to/image.jpg
```

---

## Supported Models

### Image Generation

| Model | Params | Steps | Notes |
|---|---|---|---|
| `flux` | 12B | default | General-purpose, short prompts |
| `flux_schnell` | 12B | 10 | Fast Flux |
| `flux_chroma` | 8.9B | 20 | Strong base model |
| `flux2_dev` | 32B | default | Latest generation, high VRAM |
| `z_image` | 6B | 8 | Fast, efficient, NAG-guided |
| `z_image_twinflow_turbo` | 6B | 2 | Ultra-fast distilled |
| `qwen_image_20B` | 20B | default | Best text rendering in images |
| `hidream_o1` | 10B | 50 | Unified text/pixel/reference |
| `ideogram4` | 9.3B | default | Typography, layout control |
| `krea2_raw` | - | 52 | Aesthetic photography focus |

### Video Generation

| Model | Params | Steps | Notes |
|---|---|---|---|
| `t2v` / `t2v_2_2` | 14B | default | Best quality Wan T2V |
| `t2v_sf` | 14B | 4 | Lightning fast |
| `i2v` / `i2v_2_2` | 14B | default | Image-to-video |
| `hunyuan` | 13B | default | Excellent T2V quality |
| `hunyuan_1_5_t2v` | 8B | 30 | Lower VRAM Hunyuan |
| `ltx2_22B_distilled` | 22B | 8 | Fast with audio |
| `moviigen` | 14B | default | 1080p cinematic |

### Video Editing

| Model | Params | Notes |
|---|---|---|
| `lucy_edit` | 5B | Short imperative edit commands |
| `kiwi_edit` | 5B | Edit with reference images |
| `vace_14B` | 14B | ControlNet for video |
| `vace_ditto_14B` | 14B | SOTA instruction editing |

### TTS / Audio / Music

| Model | Notes |
|---|---|
| `index_tts2` | Emotion tags, multi-speaker |
| `chatterbox` | Multilingual TTS |
| `qwen3_tts_base` | Voice cloning |
| `ace_step_v1_5` | Music generation |
| `stable_audio3_small` | Music/SFX up to 120s |

See [references/model-catalog.md](wangp/references/model-catalog.md) for the complete list.

---

## Image Display

Wan2AI can display generated images directly in your terminal:

- **`viu`** — Rust terminal image viewer (recommended)
- **`chafa`** — Versatile terminal viewer
- **iTerm2 / Kitty** — Native inline image protocols
- **PIL fallback** — Opens in default OS image viewer

Install a terminal viewer for the best experience:

```bash
# Rust (recommended)
cargo install viu

# macOS
brew install chafa

# Ubuntu/Debian
apt install chafa

# Arch
pacman -S chafa
```

The agent will ask once per session if you want images displayed, then auto-install a viewer if needed.

---

## Hardware Requirements

| VRAM | Recommended Models |
|---|---|
| **24 GB+** | All models at full quality |
| **16 GB** | Most models with int8 quantization |
| **12 GB** | 7B models, GGUF variants, Z-Image |
| **8 GB** | 1.3B models, GGUF Q4, small image models |
| **6 GB** | GGUF Q4 only |

The agent auto-detects your hardware and recommends appropriate models.

---

## Agent Support

Wan2AI works with any agent that supports the Agent Skills specification:

- **MiMoCode** / **Codex** — `npx skills add PrimeEcto/Wan2AI`
- **Claude Code** — `npx skills add PrimeEcto/Wan2AI`
- **Cursor** — `npx skills add PrimeEcto/Wan2AI`
- **Gemini CLI** — `npx skills add PrimeEcto/Wan2AI`

---

## Troubleshooting

**"Wan2GP not found"**
- Set `WAN2GP_ROOT` to your Wan2GP `app` directory
- Or install Wan2GP via Pinokio (easiest)

**"Unknown model"**
- Run `python scripts/wangp.py list` to see all available models

**Out of memory**
- Use a smaller model (`t2v_1.3B` instead of `t2v`)
- Use GGUF quantized variants
- Lower resolution or frame count

**Images not displaying**
- Install `viu`: `cargo install viu`
- Or `chafa`: `apt install chafa` / `brew install chafa`

---

## License

MIT
