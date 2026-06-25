# Wan2GP Model Catalog

Models organized by task. Use the `model_type` value (filename without `.json`) with `wangp.py generate --model <type>`.

## Text-to-Image

| model_type | Name | Params | Notes |
|---|---|---|---|
| `flux` | Flux 1 Dev 12B | 12B | General-purpose. Short direct prompts work best. |
| `flux_schnell` | Flux 1 Schnell 12B | 12B | Fast Flux variant, fewer steps needed. |
| `flux_krea` | Flux 1 Dev Krea 12B | 12B | Aesthetic photography focus. |
| `flux_chroma` | Flux 1 Chroma HD 8.9B | 8.9B | Strong base model for high-quality images. |
| `flux_chroma_radiance` | Flux 1 Chroma Radiance 8.9B | 8.9B | Enhanced Chroma variant. |
| `flux2_dev` | Flux 2 Dev 32B | 32B | Latest Flux generation. High quality, high VRAM. |
| `flux2_klein_4b` | Flux 2 Klein 4B | 4B | Lightweight Flux 2, distilled. |
| `flux2_klein_9b` | Flux 2 Klein 9B | 9B | Mid-size Flux 2, distilled. |
| `qwen_image_20B` | Qwen Image 20B | 20B | Excels at text rendering in images. |
| `qwen_image_2512_20B` | Qwen Image 2512 Release 20B | 20B | Latest Qwen image model. |
| `z_image` | Z-Image Turbo 6B | 6B | Fast, efficient. 8 steps default. |
| `z_image_base` | Z-Image Base 6B | 6B | Foundation model, higher quality. |
| `z_image_twinflow_turbo` | TwinFlow Z-Image Turbo 6B | 6B | 1-4 step distilled variant. |
| `hidream_o1` | HiDream O1 Full 10B | 10B | Unified text/pixel/reference model. |
| `hidream_o1_dev` | HiDream O1 Dev 10B | 10B | Distilled 8-step variant. |
| `ideogram4` | Ideogram v4 FP8 9.3B | 9.3B | Typography, layout control, graphic design. |
| `ideogram4_turbotime` | Ideogram v4 TurboTime 9.3B | 9.3B | Fast few-step variant. |
| `krea2_raw` | Krea 2 RAW | - | Undistilled aesthetic image model. |
| `krea2_turbo` | Krea 2 Turbo | - | Distilled fast variant. |
| `pi_flux2` | pi-FLUX.2 Dev 32B | 32B | 4-step distilled Flux 2. |

## Image-to-Image / Image Editing

| model_type | Name | Params | Notes |
|---|---|---|---|
| `flux_dev_kontext` | Flux 1 Dev Kontext 12B | 12B | Instruction-based image editing. |
| `flux_dev_uso` | Flux 1 USO Dev 12B | 12B | Style transfer (up to 2 references). |
| `flux_dev_umo` | Flux 1 UMO Dev 12B | 12B | Multi-reference image combining. |
| `flux_dev_kontext_dreamomni2` | Flux 1 DreamOmni2 12B | 12B | Multimodal instruction editing. |
| `qwen_image_edit_20B` | Qwen Image Edit 20B | 20B | High-quality image editing with text. |
| `qwen_image_edit_plus_20B` | Qwen Image Edit Plus 20B | 20B | Enhanced editing with effects. |
| `qwen_image_layered_20B` | Qwen Image Layered 20B | 20B | Decomposes images into RGBA layers. |

## Text-to-Video

| model_type | Name | Params | Notes |
|---|---|---|---|
| `t2v` | Wan2.1 Text2video 14B | 14B | Original Wan model. Cinematic prompts. |
| `t2v_2_2` | Wan2.2 Text2video 14B | 14B | Latest Wan version. |
| `t2v_sf` | Wan2.1 Lightning 14B | 14B | SelfForcing accelerated, fewer steps. |
| `t2v_fusionix` | Wan2.1 FusioniX 14B | 14B | Enhanced motion realism. |
| `t2v_1.3B` | Wan2.1 Text2video 1.3B | 1.3B | Lightweight, lower VRAM. |
| `t2v_nexus_1.3B` | Wan2.1 Nexus 1.3B | 1.3B | Enhanced small model. |
| `hunyuan` | Hunyuan Video T2V 720p 13B | 13B | Excellent text-to-video quality. |
| `hunyuan_t2v_fast` | Hunyuan FastHunyuan 13B | 13B | 6-step accelerated. |
| `hunyuan_1_5_t2v` | Hunyuan 1.5 T2V 720p 8B | 8B | New gen, lower params. |
| `hunyuan_1_5_480_t2v` | Hunyuan 1.5 T2V 480p 8B | 8B | Lower resolution variant. |
| `ltx2_22B` | LTX-2 2.3 Dev 22B | 22B | Up to 20s video with audio. |
| `ltx2_22B_distilled` | LTX-2 2.3 Distilled 22B | 22B | Faster 8-step generation. |
| `ltx2_19B` | LTX-2 2.0 Dev 19B | 19B | Previous LTX generation. |
| `ltx2_distilled` | LTX-2 2.0 Distilled 19B | 19B | Faster variant. |
| `moviigen` | MoviiGen 1080p 14B | 14B | Cinematic aesthetics, 1080p. |
| `k5_lite_t2v` | Kandinsky 5 Lite T2V 2B | 2B | Very lightweight. |
| `k5_pro_t2v` | Kandinsky 5 Pro T2V 19B | 19B | High quality, high VRAM. |
| `sky_df_14B` | SkyReels2 DF 540p 14B | 14B | Long video generation. |
| `longcat_video` | LongCat Video 13.6B | 13.6B | T2V, I2V, and continuation. |

## Image-to-Video

| model_type | Name | Params | Notes |
|---|---|---|---|
| `i2v` | Wan2.1 I2V 480p 14B | 14B | Standard image-to-video. |
| `i2v_720p` | Wan2.1 I2V 720p 14B | 14B | Higher resolution. |
| `i2v_2_2` | Wan2.2 I2V 14B | 14B | Latest version. |
| `i2v_fusionix` | Wan2.1 I2V FusioniX 14B | 14B | Enhanced motion. |
| `i2v_2_2_svi2pro` | Wan2.2 SVI2Pro I2V 14B | 14B | Unlimited continuation. |
| `hunyuan_i2v` | Hunyuan I2V 720p 13B | 13B | Good looking but less prompt adherence. |
| `hunyuan_1_5_i2v` | Hunyuan 1.5 I2V 720p 8B | 8B | New gen I2V. |
| `hunyuan_1_5_480_i2v` | Hunyuan 1.5 I2V 480p 8B | 8B | Lower resolution. |
| `flf2v_720p` | First-Last Frame 720p 14B | 14B | Supports start + end frames. |
| `fun_inp` | Fun InP I2V 14B | 14B | End image fixing support. |
| `fun_inp_1.3B` | Fun InP I2V 1.3B | 1.3B | Lightweight variant. |
| `k5_lite_i2v` | Kandinsky 5 Lite I2V 2B | 2B | Lightweight I2V. |
| `k5_pro_i2v` | Kandinsky 5 Pro I2V 19B | 19B | High quality I2V. |

## Text+Image-to-Video

| model_type | Name | Params | Notes |
|---|---|---|---|
| `ti2v_2_2` | Wan2.2 TextImage2video 5B | 5B | Combined text + image input. |
| `ti2v_2_2_fastwan` | Wan2.2 TI2V FastWan 5B | 5B | 3-step fast variant. |

## Video Editing / Control

| model_type | Name | Params | Notes |
|---|---|---|---|
| `vace_14B` | Vace 14B | 14B | ControlNet for video content control. |
| `vace_14B_2_2` | Wan2.2 Vace 14B | 14B | Latest Vace version. |
| `vace_1.3B` | Vace 1.3B | 1.3B | Lightweight ControlNet. |
| `lucy_edit` | Lucy Edit v1 5B | 5B | Instruction-guided video editing. |
| `lucy_edit_1_1` | Lucy Edit v1.1 5B | 5B | Latest Lucy version. |
| `kiwi_edit` | Kiwi Edit 5B | 5B | Video editing with reference images. |
| `chrono_edit` | Chrono Edit 14B | 14B | Image editor via video generation. |
| `vace_ditto_14B` | Ditto 14B | 14B | SOTA instruction-based video editing. |
| `hunyuan_custom_edit` | Hunyuan Custom Edit 13B | 13B | Video inpainting on people. |
| `recam_1.3B` | ReCamMaster 1.3B | 1.3B | Camera movement re-angling. |

## Character Animation / Talking Head

| model_type | Name | Params | Notes |
|---|---|---|---|
| `multitalk` | Multitalk 480p 14B | 14B | Two-person conversation from image + audio. |
| `multitalk_720p` | Multitalk 720p 14B | 14B | Higher resolution variant. |
| `infinitetalk` | Infinitetalk Single 14B | 14B | Long single-speaker talking head. |
| `infinitetalk_multi` | Infinitetalk Multi 14B | 14B | Long multi-speaker. |
| `hunyuan_avatar` | Hunyuan Avatar 13B | 13B | Audio-driven person animation. |
| `hunyuan_custom` | Hunyuan Custom 13B | 13B | Best people transfer model. |
| `fantasy` | Fantasy Talking 720p 14B | 14B | I2V + Fantasy Speaking module. |
| `standin` | Standin 14B | 14B | Identity preservation with reference. |
| `longcat_avatar` | LongCat Avatar 13.6B | 13.6B | Audio-driven character video. |
| `magi_human` | Magi Human 15B | 15B | Talking head with sync speech. |
| `animate` | Wan2.2 Animate 14B | 14B | Video + character image animation. |
| `scail` | SCAIL Preview 14B | 14B | Character animation with pose transfer. |
| `steadydancer` | Steady Dancer 14B | 14B | Dance animation with identity preservation. |
| `ovi` | Ovi v1.0 5s 10B | 10B | Audio+video generation, speaking characters. |
| `ovi_1_1` | Ovi v1.1 5s 10B | 10B | Latest Ovi version. |

## Audio / Music / TTS

| model_type | Name | Params | Notes |
|---|---|---|---|
| `index_tts2` | Index TTS 2 | - | Zero-shot TTS with emotion tags. |
| `chatterbox` | Chatterbox Multilingual TTS | - | Multilingual TTS. |
| `qwen3_tts_base` | Qwen3 TTS Base 1.7B | 1.7B | Voice clone with reference audio. |
| `qwen3_tts_customvoice` | Qwen3 Custom Voice 1.7B | 1.7B | Preset voices + instruction control. |
| `qwen3_tts_voicedesign` | Qwen3 Voice Design 1.7B | 1.7B | Natural language voice instructions. |
| `omnivoice` | OmniVoice TTS | - | Zero-shot TTS with voice design. |
| `kugelaudio_0_open` | KugelAudio 0 Open 7B | 7B | TTS with optional voice cloning. |
| `ace_step_v1` | ACE-Step v1.0 3.5B | 3.5B | Music generation. |
| `ace_step_v1_5` | ACE-Step v1.5 Turbo 2B | 2B | Fast music generation. |
| `stable_audio3_small` | Stable Audio 3 Small | - | Music-focused, up to 120s. |
| `stable_audio3_medium` | Stable Audio 3 Medium | - | Longer music, cinematic. |
| `heartmula_oss_3b` | HeartMuLa OSS 3B | 3B | Music from lyrics + tags. |

## Special

| model_type | Name | Params | Notes |
|---|---|---|---|
| `alpha` | Wan2.1 Alpha v1.0 14B | 14B | Transparent video generation (RGBA). |
| `alpha2` | Wan2.1 Alpha v2.0 14B | 14B | Improved transparency with alpha detail. |
| `phantom_14B` | Phantom 14B | 14B | People/object transfer into video. |
| `phantom_1.3B` | Phantom 1.3B | 1.3B | Lightweight transfer model. |
| `lynx` | Lynx 14B | 14B | ControlNet with SOTA identity preservation. |
| `vista4d` | Vista4D 384p 14B | 14B | Video reshooting from novel viewpoints. |
| `wanmove` | Wan-Move 480p 14B | 14B | Motion control generation. |
| `bernini` | Bernini-R 14B | 14B | Modify existing video content. |
