# Hardware Profiles and Recommendations

## GPU Detection

Wan2GP auto-detects your GPU and maps it to a profile key:

| GPU Family | Profile Key | Examples |
|---|---|---|
| NVIDIA RTX 50xx | `RTX_50` | RTX 5090, 5080, 5070 |
| NVIDIA RTX 40xx | `RTX_40` | RTX 4090, 4080, 4070, 4060 |
| NVIDIA RTX 30xx | `RTX_30` | RTX 3090, 3080, 3070, 3060 |
| NVIDIA RTX 20xx | `RTX_20` | RTX 2080, 2070, 2060 |
| NVIDIA GTX 10xx | `GTX_10` | GTX 1080, 1070, 1060 |
| Apple Silicon | `MPS` | M1, M2, M3, M4 (all variants) |
| AMD RX 7xxx | `AMD_GFX110X` | RX 7900, 7800, 7700, 7600 |
| AMD RX 7xxx (APU) | `AMD_GFX1151` | RX 7000, Z1, Phoenix |
| AMD RX 8xxx | `AMD_GFX1201` | RX 8000, Strix |

## Performance Profiles (1-5)

Profile is auto-selected based on RAM + VRAM:

| Profile | RAM | VRAM | Description |
|---|---|---|---|
| **1** | >60 GB | >22 GB | Full bf16, all models, maximum quality |
| **2** | >60 GB | ≤22 GB | int8 quantized for large models |
| **3** | >30 GB | >22 GB | bf16 for ≤7B, int8 for larger |
| **4** | >30 GB | ≤22 GB | int8 everywhere, most common |
| **5** | ≤30 GB | any | Minimum RAM, smallest models preferred |

## Attention Modes

| Mode | Best For | Notes |
|---|---|---|
| `sage2` | RTX 30/40/50 | SageAttention 2, fastest on modern NVIDIA |
| `sage` | RTX 20xx | SageAttention 1, good for older cards |
| `sdpa` | Fallback, AMD, Apple | PyTorch native attention |
| `flash` | NVIDIA with FA | Flash Attention 2/3 if available |

## VRAM → Model Size Guide

### 24 GB+ VRAM (RTX 4090, RTX 3090, etc.)
- **All models work** at bf16 or int8
- Can run 14B video models, 22B LTX-2, 20B Qwen Image
- Best quality, no compromises
- Recommended: Profile 1

### 16 GB VRAM (RTX 4080, RTX 5070 Ti, etc.)
- **14B models**: int8 quantization recommended
- **7B models**: bf16 works fine
- **Image models**: Most work (Flux 12B int8, Z-Image 6B, Qwen 20B int8)
- Recommended: Profile 3-4

### 12 GB VRAM (RTX 4070, RTX 3060 12GB, etc.)
- **14B models**: int8, may need lower resolution
- **7B models**: int8 recommended
- **1.3B models**: bf16 works
- **GGUF models**: Q4_K_M, Q6_K, Q8_0 variants
- **Image models**: Flux 12B int8, Z-Image 6B, HiDream 10B int8
- Recommended: Profile 4

### 8 GB VRAM (RTX 4060, RTX 3060 8GB, etc.)
- **1.3B models**: int8
- **GGUF Q4**: Best option for larger models
- **Image models**: Z-Image 6B int8, Flux Schnell int8
- Avoid: 14B models, 20B+ image models
- Recommended: Profile 5

### 6 GB VRAM (GTX 1060, RTX 3050, etc.)
- **GGUF Q4 only**: Very limited
- **Small image models**: Z-Image at reduced resolution
- Consider: Cloud/offload solutions
- Recommended: Profile 5

## Apple Silicon (MPS)

- Unified memory: RAM = VRAM
- M1/M2: 8-16 GB unified → Profile 4-5
- M3/M4: 16-36 GB unified → Profile 2-4
- M4 Pro/Max: 36-128 GB unified → Profile 1-2
- Attention mode: `sdpa` (default for MPS)
- No bfloat16 on M1/M2 (needs M3+)

## AMD GPUs

- RX 7900 XTX (24 GB): Profile 1-2, works with most models
- RX 7800 XT (16 GB): Profile 3-4
- RX 7600 (8 GB): Profile 5
- Attention mode: `sdpa` (default for AMD)
- Some models may have compatibility issues

## Quantization Options

| Type | VRAM Savings | Quality Impact | Notes |
|---|---|---|---|
| `int8` | ~50% | Minimal | Most common, good balance |
| `fp8` | ~50% | Minimal | Better than int8 on RTX 40+ |
| `nvfp4` | ~75% | Some loss | RTX 50xx only (sm120+) |
| `GGUF Q4_K_M` | ~75% | Moderate | CPU+GPU hybrid, works anywhere |
| `GGUF Q6_K` | ~60% | Light | Good balance for GGUF |
| `GGUF Q8_0` | ~50% | Minimal | Best GGUF quality |

## Quick Recommendations

**"I want to generate images"**
- 24 GB+ VRAM: `flux` or `qwen_image_20B` (best quality)
- 12-16 GB: `z_image` or `flux_schnell` (fast, efficient)
- 8 GB: `z_image` with int8

**"I want to generate videos"**
- 24 GB+ VRAM: `t2v` or `t2v_2_2` (Wan 14B, best quality)
- 16 GB: `t2v` with int8, or `ltx2_22B_distilled` (fast)
- 12 GB: `t2v_1.3B` or GGUF variants
- 8 GB: `t2v_1.3B` with int8

**"I want fast generation"**
- Images: `z_image_twinflow_turbo` (1-4 steps), `flux_schnell`
- Videos: `t2v_sf` (Lightning), `ltx2_22B_distilled` (8 steps), `hunyuan_t2v_fast` (6 steps)

**"I want the best quality regardless of speed"**
- Images: `qwen_image_20B`, `flux2_dev` (32B)
- Videos: `t2v` or `t2v_2_2` (Wan 14B, 30+ steps), `hunyuan` (13B)
