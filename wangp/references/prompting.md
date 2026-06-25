# Prompting Guide by Model Family

All conventions derived from actual model defaults in `app/defaults/*.json` and handler logic in `app/models/*/`.

---

## IMAGE GENERATION MODELS

### Z-Image Turbo 6B (`z_image`)

**Default prompt**: *(none — uses system fallback)*
**Resolution**: 1024x1024 | **Steps**: 8 | **Guidance**: 0 (uses NAG)

**Prompting style**: Concise, descriptive text. Uses NAG (Negative-Aware Guidance) instead of CFG — set `guidance_scale=0`, `NAG_scale=1.0`, `NAG_tau=3.5`, `NAG_alpha=0.5`.

**Example prompts**:
```
A red fox sitting in a misty forest at dawn, soft golden light, photorealistic
```
```
A minimalist logo for a coffee shop, clean lines, white background
```

**Key**: Don't write long cinematic paragraphs. Keep it to 1-2 sentences. NAG handles quality internally.

### Z-Image Base 6B (`z_image_base`)

**Default prompt**: *(none)*
**Resolution**: 1024x1024 | **Steps**: 30 | **Guidance**: 4 | **Flow shift**: 6.0

Same prompting style as Turbo but needs more steps. Uses standard CFG (guidance_scale=4), not NAG.

### TwinFlow Z-Image Turbo (`z_image_twinflow_turbo`)

**Default prompt**: *(none)*
**Resolution**: 1024x1024 | **Steps**: 2 | **Guidance**: 0 (NAG)

Distilled variant — only 2 steps. Same prompting as Z-Image Turbo. Uses `unified_solver: true`.

### Z-Image ControlNet (`z_image_control`, `z_image_control2`, `z_image_control2_1`)

**Resolution**: 1024x1024 (v1/v2) or 1920x1088 (v2.1) | **Steps**: 9

Supports guide types: Pose (`PV`), Canny (`DV`), Depth (`EV`), Scribble (`V`), Raw Format. v2/v2.1 also support inpainting with mask modes `A`/`NA`. Set `control_net_weight=0.75`.

---

### Flux 1 Dev (`flux`)

**Default prompt**: `draw a hat`
**Resolution**: 1280x720 | **Embedded guidance**: 2.5 | **Uses NAG**

**Prompting style**: Short, direct. The default is literally "draw a hat". Don't overthink it.

**Example prompts**:
```
draw a hat
```
```
A photorealistic portrait of a cyberpunk samurai, neon rain, cinematic lighting
```
```
a fox walking in fresh snow at golden hour, natural light, detailed fur
```

### Flux 1 Schnell (`flux_schnell`)

**Default prompt**: `draw a hat`
**Resolution**: 1280x720 | **Steps**: 10

Fast variant. Same prompting as Flux Dev. Supports inpainting.

### Flux 1 Dev Kontext (`flux_dev_kontext`)

**Default prompt**: `add a hat`
**Resolution**: 1280x720 | **Embedded guidance**: 2.5 | **Denoising strength**: 1.0

**Prompting style**: Instruction-based editing. Short imperative commands. Requires a reference image set as `image_start` with prompt type `KI`.

**How to use for editing**:
```
add a hat
```
```
replace the background with a sunset beach
```
```
make the person smile
```

**Image input**: Set `image_start` to the source image. The model treats it as the main subject/landscape to edit.

### Flux 1 Dev USO (`flux_dev_uso`)

**Default prompt**: `the man is wearing a hat`
**Resolution**: 1024x1024 | **Embedded guidance**: 4

**Prompting style**: Style transfer. Reference images are style sources. Prompt describes the desired output.

**Image input**: Supports up to 3 reference images via `image_refs`. First image = main subject (`K`), remaining = style references (`I`). Set prompt type to `KI` or `KIJ`.

### Flux 1 Dev UMO (`flux_dev_umo`)

**Default prompt**: `the man is wearing a hat`
**Resolution**: 768x768 | **Embedded guidance**: 4

**Prompting style**: Multi-reference combining. Multiple people/objects merged into one scene.

**Image input**: All reference images are people/objects (`I` prompt type).

### Flux 1 DreamOmni2 (`flux_dev_kontext_dreamomni2`)

**Default prompt**: `In the scene, the character from the first image stands on the left, and the character from the second image stands on the right. They are shaking hands against the backdrop of a spaceship interior.`
**Resolution**: 1280x720

**Prompting style**: Detailed scene description referencing which image contains which subject. Multimodal instruction-based editing and generation.

### Flux 1 Chroma (`flux_chroma`, `flux_chroma_radiance`)

**Default prompt**: `draw a hat`
**Resolution**: 1280x720 | **Steps**: 20 | **Guidance**: 1 (single phase)

**No negative prompt** — Chroma variants don't support negative prompts. Uses single-phase guidance.

### Flux 2 Dev (`flux2_dev`)

**Default prompt**: `draw a hat on top of a hat inside a hat`
**Resolution**: 1024x1024 | **Embedded guidance**: 4.0

Supports inpainting, ControlNet guides (Pose/Motion/Depth). Same short prompting style.

### Flux 2 Klein (`flux2_klein_4b`, `flux2_klein_9b`)

**Default prompt**: *(uses system fallback)*
**Steps**: 4 (distilled)

Distilled Flux 2 variants. Same short prompting style.

### Pi-Flux.2 (`pi_flux2`)

**Default prompt**: *(uses system fallback)*
Uses Pi-Flow method with Gaussian mixture velocity field prediction. 4-step distilled.

---

### Qwen Image 20B (`qwen_image_20B`, `qwen_image_2512_20B`)

**Default prompt**: `draw a hat`
**Resolution**: 1280x720

**Prompting style**: Supports long-form text rendering in images. Good for infographics, posters, text-heavy designs.

**Example prompts**:
```
draw a hat
```
```
A professional infographic about climate change, with the title "Our Warming World" in bold sans-serif font, three data visualization sections, clean modern design, white background
```

### Qwen Image Edit (`qwen_image_edit_20B`, `qwen_image_edit_plus_20B`, `qwen_image_edit_plus2_20B`)

**Default prompt**: `add a hat`
**Resolution**: 1280x720 or 1024x1024

**Prompting style**: Instruction-based editing with text rendering support. Short imperative commands.

**How to use for editing**:
```
add a hat
```
```
change the background to a beach
```
```
add the text "SALE" in red bold letters at the top
```

### Qwen Image Layered (`qwen_image_layered_20B`)

**Default prompt**: *(uses system fallback)*
Decomposes images into multiple RGBA layers. Prompt describes the scene to decompose.

---

### HiDream O1 (`hidream_o1`, `hidream_o1_dev`)

**Default prompt**: `A tiny porcelain robot arranging wildflowers on a sunlit kitchen table, crisp details, natural colors`
**Resolution**: 1920x1088 | **Steps**: 50 | **Guidance**: 5

**Prompting style**: More descriptive than Flux. Include subject, action, environment, and style details.

**Example prompts**:
```
A tiny porcelain robot arranging wildflowers on a sunlit kitchen table, crisp details, natural colors
```
```
A serene Japanese garden with a stone path leading to a small wooden bridge over a koi pond, cherry blossoms falling, soft morning light
```

---

### Ideogram v4 (`ideogram4`)

**Default prompt**: *(structured JSON — see below)*
**Resolution**: default | **Steps**: default

**Prompting style**: IDEOGRAM USES A UNIQUE STRUCTURED JSON FORMAT. Not plain text.

**Default prompt format**:
```json
{
  "aspect_ratio": "4:3",
  "high_level_description": "A playful cinematic highway scene of a large gray elephant standing in a bathtub on the flatbed trailer of a moving semi-truck...",
  "compositional_deconstruction": {
    "background": "A sunlit highway with asphalt lanes...",
    "elements": [
      {"type": "obj", "bbox": [120,260,760,760], "desc": "A massive African elephant with wrinkled gray skin..."},
      {"type": "obj", "bbox": [80,330,420,720], "desc": "A curved stream of clear sparkling water..."}
    ]
  }
}
```

**Key**: Ideogram expects JSON with `aspect_ratio`, `high_level_description`, and `compositional_deconstruction` (background + positioned elements). This is completely different from other models.

---

### Krea 2 (`krea2_raw`, `krea2_turbo`)

**Default prompt**: `a fox walking in fresh snow at golden hour, natural light, detailed fur`
**Steps**: 52 (RAW) / distilled (Turbo) | **Guidance**: 3.5

**Prompting style**: Natural language with aesthetic focus. Include lighting, mood, and texture details.

---

## VIDEO GENERATION MODELS

### Wan 2.1 Text-to-Video (`t2v`, `t2v_fusionix`, `t2v_sf`)

**Default prompt**: *(none — uses system fallback)*
**Resolution**: 832x480 | **Video length**: 81 frames | **Flow shift**: 5.0

**System fallback prompt** (used when no prompt specified):
```
A large orange octopus is seen resting on the bottom of the ocean floor, blending in with the sandy and rocky terrain. Its tentacles are spread out around its body, and its eyes are closed. The octopus is unaware of a king crab that is crawling towards it from behind a rock, its claws raised and ready to attack. The crab is brown and spiny, with long legs and antennae. The scene is captured from a wide angle, showing the vastness and depth of the ocean. The water is clear and blue, with rays of sunlight filtering through. The shot is sharp and crisp, with a high dynamic range. The octopus and the crab are in focus, while the background is slightly blurred, creating a depth of field effect.
```

**Prompting style**: Detailed cinematic narrative. Describe subject, action, environment, camera angle, lighting, and depth of field. Natural language paragraphs.

**Lightning (`t2v_sf`)**: 4 steps, guidance=1, flow_shift=3. Same prompt style.
**FusioniX (`t2v_fusionix`)**: 8 steps, guidance=1, embedded_guidance=6. Same prompt style.

### Wan 2.2 Text-to-Video (`t2v_2_2`)

**Default prompt**: *(none — uses system fallback)*
Same prompting style as Wan 2.1.

### Wan 2.1 Image-to-Video (`i2v`, `i2v_720p`, `i2v_fusionix`)

**Default prompt**: *(none — uses system fallback)*
**Resolution**: 832x480 or 1280x720

**System fallback prompt** (I2V):
```
Several giant wooly mammoths approach treading through a snowy meadow, their long wooly fur lightly blows in the wind as they walk, snow covered trees and dramatic snow capped mountains in the distance, mid afternoon light with wispy clouds and a sun high in the distance creates a warm glow, the low camera view is stunning capturing the large furry mammal with beautiful photography, depth of field.
```

**Prompting style**: Describe the motion and action. The image provides the starting frame; the prompt describes what happens next.

### Wan 2.2 Image-to-Video (`i2v_2_2`)

**Default prompt**: *(none)*
Same as Wan 2.1 I2V. Supports enhanced lightning variants.

### Wan 2.2 Text+Image-to-Video (`ti2v_2_2`)

**Default prompt**: *(none)*
Combined text + image input. 5B parameter model.

### First-Last Frame to Video (`flf2v_720p`)

**Default prompt**: *(none)*
**Resolution**: 1280x720

Supports both start AND end image. The prompt describes the transition between frames.

### Fun InP (`fun_inp`, `fun_inp_1.3B`)

**Default prompt**: *(none)*

Alternative I2V with built-in end image fixing. Supports start and end image natively.

---

### HunyuanVideo Text-to-Video (`hunyuan`, `hunyuan_t2v_fast`, `hunyuan_t2v_accvideo`)

**Default prompt**: *(none — uses system fallback)*
**Resolution**: default (832x480) | **Video length**: default (81)

Same cinematic narrative style as Wan. 13B parameters — best quality T2V.

**FastHunyuan**: 6-step accelerated. **AccVideo**: distillation-accelerated.

### HunyuanVideo 1.5 (`hunyuan_1_5_t2v`, `hunyuan_1_5_i2v`)

**Default prompt**: *(none)*
**Resolution**: 1280x720 | **Steps**: 30 | **Video length**: 97

8B parameter model. Same prompting style as original HunyuanVideo. 480p and 720p variants.

### HunyuanVideo Image-to-Video (`hunyuan_i2v`)

**Default prompt**: *(none)*
**Resolution**: 1280x720

Describe the motion/action. Image provides starting frame.

---

### LTX-2 2.3 (`ltx2_22B`, `ltx2_22B_distilled`)

**Default prompt** (LTX uses a LONG screenplay-style prompt):
```
A warm sunny backyard. The camera starts in a tight cinematic close-up of a woman and a man in their 30s, facing each other with serious expressions. The woman, emotional and dramatic, says softly, "That's it... Dad's lost it. And we've lost Dad." The man exhales, slightly annoyed: "Stop being so dramatic, Jess." A beat. He glances aside, then mutters defensively, "He's just having fun." The camera slowly pans right, revealing the grandfather in the garden wearing enormous butterfly wings, waving his arms in the air like he's trying to take off. He shouts, "Wheeeew!" as he flaps his wings with full commitment. The woman covers her face, on the verge of tears. The tone is deadpan, absurd, and quietly tragic.
```
**Resolution**: 1280x720 | **Steps**: 8 (distilled) | **Video length**: 241

**Prompting style**: VERBOSE SCREENPLAY FORMAT. Include:
- Scene setting ("A warm sunny backyard")
- Camera directions ("The camera starts in a tight cinematic close-up...")
- Character dialogue in quotes
- Character actions and emotions
- Tone/atmosphere description

The more detail, the better. LTX thrives on long, detailed prompts with dialogue.

### LTX-2 2.0 (`ltx2_19B`, `ltx2_distilled`)

Same verbose screenplay style as LTX-2 2.3. 19B parameters.

### LTX Video 0.9.8 (`ltxv_13B`, `ltxv_distilled`)

**Default prompt**: *(none)*
13B parameter model. Supports very long videos (up to 1800 frames).

---

### Kandinsky 5 (`k5_lite_t2v`, `k5_pro_t2v`, `k5_lite_i2v`, `k5_pro_i2v`)

**Default prompt**: *(none)*
Russian/English bilingual model. 2B (Lite) or 19B (Pro) parameters.

### SkyReels2 Diffusion Forcing (`sky_df_14B`, `sky_df_1.3B`)

**Default prompt**: *(none)*
Designed for very long video generation beyond the usual 5s limit.

### LongCat Video (`longcat_video`)

**Default prompt**: *(none)*
Supports T2V, I2V, and video continuation with a unified transformer. 13.6B parameters.

### MoviiGen (`moviigen`)

**Default prompt**: *(none)*
1080p cinematic aesthetics. Based on Wan T2V architecture.

---

## EDITING MODELS

### Lucy Edit (`lucy_edit`, `lucy_edit_1_1`)

**Default prompt**: `change the clothes to red`
**Resolution**: 1280x720 | **Steps**: 30 | **Video length**: 81

**Prompting style**: SHORT IMPERATIVE COMMANDS. Single action per prompt. No tags or delimiters.

**Examples**:
```
change the clothes to red
```
```
add sunglasses to the person
```
```
replace the background with a beach
```

**Input**: Requires source video. Motion and composition preserved automatically.

### Kiwi Edit (`kiwi_edit`)

**Default prompt**: `Change the woman's dress to a vivid red while preserving her pose, face, and the room lighting.`
**Steps**: 30 | **Video length**: 81

**Prompting style**: Descriptive edit instructions with PRESERVATION CLAUSES. Longer than Lucy.

**Instruct-Only (`kiwi_edit_instruct_only`)**: `Remove the monkey.` — short commands, no reference image.
**Reference-Only (`kiwi_edit_reference_only`)**: `Apply the style from the reference image.` — image-driven editing.

### Chrono Edit (`chrono_edit`)

**Default prompt**: `Rotate the pose of the woman so that she is facing the right`
**Steps**: default

Image editor that generates a video internally to produce the edit. More complex transformations.

### Vace ControlNet (`vace_14B`, `vace_1.3B`, `vace_14B_2_2`)

**Default prompt**: *(none)*
ControlNet for video content control. Supports video guide, masks, reference images. Lightning variant: 8 steps.

### Vace Ditto (`vace_ditto_14B`)

**Default prompt**: `Render the subjects as classical sculptures carved from single blocks of pristine white marble`
SOTA instruction-based video editing.

### Hunyuan Custom Edit (`hunyuan_custom_edit`)

**Default prompt**: *(none)*
Video inpainting on people. Add accessories or completely replace clothing.

---

## CHARACTER ANIMATION / TALKING HEAD

### Multitalk (`multitalk`, `multitalk_720p`)

**Default prompt**: *(none)*
Two-person conversation from image + audio. Requires reference image and audio input.

### Infinitetalk (`infinitetalk`, `infinitetalk_multi`)

**Default prompt**: *(none)*
Long talking head videos. Single or multi-speaker variants.

### Hunyuan Avatar (`hunyuan_avatar`)

**Default prompt**: *(none)*
Audio-driven person animation. Requires reference image + audio.

### Hunyuan Custom (`hunyuan_custom`)

**Default prompt**: *(none)*
Best model for people transfer. Quite consistent identity preservation.

### Fantasy Talking (`fantasy`)

**Default prompt**: *(none)*
**Resolution**: 1280x720
I2V + Fantasy Speaking module for talking head generation.

### Standin (`standin`)

**Default prompt**: *(none)*
Identity preservation with reference image. Combined with T2V.

### Wan Animate (`animate`)

**Default prompt**: *(none)*
Takes video + character image. Supports 'Animation' or 'Replacement' mode.

### SCAIL (`scail`, `scail2_14B`)

**Default prompt**: *(none)*
Character animation with end-to-end reference, pose, and mask conditioning.

### Steady Dancer (`steadydancer`)

**Default prompt**: *(none)*
Dance animation with robust first-frame preservation.

### Ovi (`ovi`, `ovi_1_1`)

**Default prompt**:
```
A singer in a glittering jacket grips the microphone, sweat shining on his brow, and shouts, <S>The end is night<E>. The crowd roars in response, fists in the air. Behind him, a guitarist steps to the front of the stage, leaning into a wild solo, <S>the final chord rings out<E>.
```

**Prompting style**: Use `<S>` and `<E>` tags to mark speech segments within the scene description. Generates audio + video simultaneously.

### LongCat Avatar (`longcat_avatar`, `longcat_avatar_multi`)

**Default prompt**: *(none)*
Audio-driven character video. Single or multi-speaker. 13.6B parameters.

### Magi Human (`magi_human`, `magi_human_distill`)

**Default prompt**:
```
A calm woman with short dark hair looks into the camera and speaks clearly in English about how small daily habits can improve confidence. Her expression stays warm and natural, with subtle head movement, realistic blinking, and clean lip sync. Background is a softly blurred living room.
```
**Resolution**: 448x256 | **Steps**: 32

**Prompting style**: Describe the person, their expression, speech content, movements, and background. Talking head model.

### Phantom (`phantom_14B`, `phantom_1.3B`)

**Default prompt**: *(none)*
People/object transfer into generated video. Requires reference images.

### Lynx (`lynx`)

**Default prompt**: *(none)*
ControlNet with SOTA identity preservation. Requires reference image (close-up).

### Bernini (`bernini`, `bernini_1.3B`)

**Default prompt**: `Replace the person's outer shirt with the shirt from the reference image while preserving the original motion, camera framing, lighting, background, and body pose.`
**Resolution**: 832x480 | **Steps**: 40 | **Video length**: 81

**Prompting style**: Detailed edit instructions with explicit preservation clauses.

### MoCha (`mocha`)

**Default prompt**: `video`
**Steps**: 20 | **Video length**: 81
Single-character replacement using source video, first-frame mask, and reference images.

---

## TTS / AUDIO MODELS

### IndexTTS2 (`index_tts2`)

**Default prompt**:
```
[fear] At the very beginning I was so afraid to speak.
[sadness] Nobody would talk to me. I felt so alone.
[disgust] They would just ignore me and pretend that I didnt exist
[happy] By chance I discovered a new world
```

**Prompting style**: Emotion tags in brackets. Each line = one emotional segment.

**Emotion tags**: `[happy]`, `[sadness]`, `[anger]`, `[surprise]`, `[fear]`, `[disgust]`

**Multi-speaker**:
```
Speaker 1: [happy] Welcome to the show!
Speaker 2: [excited] Thanks for having me!
```

### Chatterbox TTS (`chatterbox`)

**Default prompt**: `Welcome to Chatterbox !`
Simple text. `model_mode` for language selection. `exaggeration` and `pace` control expressiveness.

### Qwen3 TTS Base (`qwen3_tts_base`)

**Default prompt**: `I checked the schedule twice, and everything lines up.`
Voice clone from reference audio. For dialogue: `Speaker 1:` / `Speaker 2:` tags.

### Qwen3 TTS Custom Voice (`qwen3_tts_customvoice`)

**Default prompt**: `The lights are already on, so we can start whenever you are ready.`
Preset speaker profiles with optional instruction control.

### Qwen3 TTS Voice Design (`qwen3_tts_voicedesign`)

**Default prompt**: `I wish you a good day. Please keep the door closed. I am afraid AI haters are going to come in. Oh I am so afraid !`
Describe the voice you want in natural language.

### OmniVoice (`omnivoice`)

**Default prompt**: `I told you this would happen.[laughter] But no, nobody listened. Dont you feel dumb now ? [question-en] What now?`

**Prompting style**: Inline emotion/action tags: `[laughter]`, `[question-en]`, etc.

### KugelAudio (`kugelaudio_0_open`)

**Default prompt**: `Hello! This is KugelAudio speaking in a clear, friendly voice.`
TTS with optional voice cloning. Two-speaker dialogue support.

### DramaBox Audio (`dramabox_audio`)

**Default prompt**:
```
Speaker 1:
A confident, slightly condescending man leans in close with a smooth baritone voice, "You've been looking at the wrong evidence. The horizon doesn't curve; it stays flat right up until your eyes give out."
Speaker 2:
An incredulous woman tilts her head back, her tone sharp and rising in pitch, "That's not how any of this works."
```

**Prompting style**: Speaker tags with voice descriptions, dialogue in quotes.

### Scenema Audio (`scenema_audio`)

**Default prompt**:
```
Speaker 1{voice="Confident adult man, skeptical and emphatic", gender="male", scene="a spirited debate beside a map"}: [Pointing at the map with absolute confidence] Look at this map...
Speaker 2{voice="Patient adult woman, calm and logical", gender="female"}: [sighs, pinching the bridge of her nose] That's not how maps work.
```

**Prompting style**: Speaker tags with structured metadata `{voice="...", gender="...", scene="..."}`, inline actions in brackets.

---

## MUSIC MODELS

### ACE-Step (`ace_step_v1`, `ace_step_v1_5`)

**Default prompt**:
```
[Verse]
Neon rain on the city line
You hum the tune and I fall in time
[Chorus]
Hold me close and keep the time
```

**Prompting style**: Song structure tags `[Verse]`, `[Chorus]`, `[Bridge]`, etc. with lyrics.

### Stable Audio 3 (`stable_audio3_small`, `stable_audio3_medium`)

**Default prompt**: `Lo-fi house loop with warm tape saturation, mellow bass, soft vinyl crackle, and a relaxed 120 BPM groove.`

**Prompting style**: Genre + instruments + mood + BPM. Short descriptive paragraph.

**SFX variant**: `Impulse response of a large concrete stairwell, a single sharp hand clap, followed by a natural decay.`

### HeartMuLa (`heartmula_oss_3b`)

**Default prompt**: *(none)*
Music generation conditioned on lyrics and tags.

---

## SPECIAL MODELS

### Alpha Transparent Video (`alpha`, `alpha2`)

**Default prompt**: `A large orange octopus is seen resting. The background of the video is transparent.`
Generates transparent RGBA video. Append "The background of the video is transparent." to your prompt.

---

## IMAGE EDITING WORKFLOW

For models that support both T2I and I2I editing:

1. **Flux Kontext**: Set `image_start` to source image, prompt type `KI`, prompt = edit instruction
2. **Flux USO**: Set `image_refs` to style images, prompt type `KI` or `KIJ`, prompt = desired output description
3. **Flux UMO**: Set `image_refs` to people/objects, prompt type `I`, prompt = scene description
4. **Qwen Image Edit**: Set `image_start` to source image, prompt = edit instruction
5. **Lucy Edit**: Set `video_source` to source video, prompt = short edit command
6. **Kiwi Edit**: Set `video_source` + optional `image_refs`, prompt = edit instruction with preservation clause
7. **Vace**: Set `video_source`/`image_guide`/`image_mask` as needed, prompt = description or instruction
