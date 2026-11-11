# 🎬 LUMA / KLING IMAGE-TO-VIDEO PACK
### Maa Ka Aanchal — 13 shots, 9:16, anime style

Yeh pack aapke **13 finished anime frames** + har shot ka **motion prompt** hai.
Aap image upload karo → prompt paste karo → 5 second clip milegi → main unhe timeline me lagā dunga.

---

## ⚙️ SETTINGS (ek hi baar set karo)

| Setting | Value |
|---|---|
| Tool | **Luma Ray2 / Kling 1.6 / Runway Gen-4 / Hailuo / Pika 2.2** (jo available ho) |
| Mode | **Image-to-Video** (start frame = pack ki PNG) |
| Duration | **5 sec** |
| Aspect | **9:16** (vertical) |
| Resolution | 1080p (ya 720p → baad me upscale) |
| Camera | `auto` ya prompt me diya gaya exact move |
| Loop | OFF |
| Takes | Har shot **3 attempts**, hero shots (**04, 08B, 09B**) ke **5** |

### Negative prompt (har generation me)
```
extra fingers, deformed hands, distorted face, face morphing, warped eyes,
double limbs, plastic skin, oversaturated, cartoon outline change, text,
subtitles, watermark, logo, jump scare, ghost makeup, blue skin, harsh flash
```
> **Zaroori:** prompt me **koi dialogue mat likho**. Lips ko VO se match karana hai to file `Maaya`/`HeyGen` jaise lip-sync tool me daalo — Luma se nahi.

---

## 🎥 SHOT-BY-SHOT MOTION PROMPTS

### 1 · `01A_thermometer.png` — 0:00–0:02
```
Macro shot of a digital thermometer on a crumpled bedsheet, its display glowing
faint green. Very slow push-in, dust motes drifting in the cold moonlight.
Static camera, no hands moving. Cinematic, anime illustration style.
```

### 2 · `01B_kabir_shiver.png` — 0:02–0:05
```
The young man wrapped in a white blanket shivers, shoulders trembling, breath
visible in the cold air, sweat on his forehead, eyes half closing. Slight handheld
camera shake. Warm lamp flickers softly on the left, blue window light on the right.
```

### 3 · `02_tear_phone.png` — 0:05–0:10
```
He lies on his side holding a glowing phone, a single tear slides down his cheek,
his lips tremble as he whispers. The phone's blue light pulses gently on his face.
Very slow push-in, subtle handheld drift.
```

### 4 · `03_door_stagger.png` — 0:10–0:14
```
He staggers forward holding the wall, weak knees, blanket slipping off the bed
behind him, reaching for the old wooden door. Handheld camera follows him slowly
from behind. Cold moonlight, deep shadows.
```

### 5 · `04_maa_reveal.png` — 0:14–0:19  *(hero shot — 5 takes)*
```
The old wooden door swings open and his mother stands there in a faded mustard
saree holding a steel glass of hot turmeric milk, thick steam rising. She smiles
softly. Warm golden light spills into the dark room. Static camera, only the door
and steam move. Her face stays still.
```

### 6 · `05A_cloth.png` — 0:19–0:21.5
```
Her weathered hand gently presses a folded wet cloth onto her sleeping son's
forehead. Tiny movement only, warm lamp glow, tender mood. Static close-up.
```

### 7 · `05B_caress.png` — 0:21.5–0:27.5
```
She sits on the bed edge and strokes his hair slowly; his half-open feverish eyes
drift up to her. Slow push-in, warm amber light, emotional.
```

### 8 · `06_maa_leaves.png` — 0:27.5–0:32.5
```
She turns off the yellow table lamp; the room falls into blue darkness; she walks
quietly to the wooden door and pulls it shut behind her, leaving him asleep.
Static wide camera, only she moves.
```

### 9 · `07_morning_phone.png` — 0:32.5–0:37.5
```
Soft morning light. He sits up in bed, touches his forehead with a relieved smile.
On the study table the phone lights up and vibrates, sliding slightly. Gentle
camera drift, dust in the light beam.
```

### 10 · `08A_hello_papa.png` — 0:37.5–0:40
```
He holds the phone to his ear, listening; his eyebrows slowly pull together in
confusion. Very subtle movement, static camera, shallow depth of field.
```

### 11 · `08B_shock.png` — 0:40–0:46  *(hero shot — 5 takes)*
```
Extreme close-up as shock lands: his eyes widen and go completely still, pupils
trembling, tears welling but not falling, lips parting slightly. He does NOT cry
and does NOT move his head. Extremely slow push-in, frozen, numb, devastating.
```

### 12 · `09A_head_turn.png` — 0:46–0:49
```
Slow motion: he turns his neck slowly to look down toward the study table beside
the bed, face blank and numb. Only the neck moves, 0.4x speed feel.
```

### 13 · `09B_glass_hero.png` — 0:49–0:55.5  *(hero shot — 5 takes)*
```
Macro of an empty steel glass with dried turmeric stains. Thick white steam curls
upward from the empty glass into the air, slowly and continuously. Warm lamp bokeh
flickers in the background. Static camera, only the steam moves.
```

---

## 📥 CLIPS AA JAAYEN TO

1. Clips ko `luma_pack/output/` me `01A.mp4 … 09B.mp4` naam se save karo
2. Mujhe bolo — main unhe exact timeline (0:00 → 0:55.5) par lagā kar, captions + audio ke saath final render kar dunga
3. Jo shot AI me kharab aaye, uska backup living-still version already ready hai

---

## 💡 TIPS

- **Face morph** ho raha ho → prompt me chehra describe mat karo, sirf action likho; base image se identity aati hai.
- **Steam** na aaye → `thick white steam, curling upward, kettle just poured` add karo.
- **Haath** kharab aaye → shot ko `static` rakho aur haath frame ke bahar crop karo.
- **Emotion** kam lage → `no sobbing, no crying, frozen expression` likho — under-acting zyada dard deti hai.
- Har clip ka **best 3–4 second** hi use hoga, poora 5 sec nahi.

*— Maa Ka Aanchal · Luma Pack v1*
