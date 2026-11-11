# 🎬 MAA KA AANCHAL — FINAL MASTER SCRIPT
### Luma Dream Machine Pro · Premium Edition
**Format:** 9:16 vertical short (Reels / Shorts) · **Runtime:** 57 sec · **Language:** Hindi dialogue, Hinglish direction
**Version:** 2.0 (production-hardened) · **Total shots:** 13 · **Characters:** 2

---

## ⚡ 0 · EK MINUTE MEIN YEH FILE KAISE USE KAREIN

1. **STEP 1** → Neeche `§2` se 2 base photos banao (Kabir + Maa). Face lock ke liye yeh sabse zaroori step hai.
2. **STEP 2** → `§5` ki shot-by-shot table kholo. Har row ka **SHORT PROMPT** Luma me paste karo, base photo ko start frame banao.
3. **STEP 3** → Jo clips acchi bani, `§6` ke timecode ke hisaab se timeline par chipka do.
4. **STEP 4** → `§7` ki SFX/music list add karo, phir `§8` ka colour grade.
5. **STEP 5** → `subtitles.srt` import karo (ready-made file repo mein hai).

> **Golden rule:** Luma se **dialogue mat karwao**. Luma lips ko theek se sync nahi karta — hamesha silent visual banao, aawaz post-production me daalo. Yeh ek rule poore video ka quality decide karta hai.

---

## 🧠 1 · WORLD BIBLE (Continuity Lock — har prompt me repeat hoga)

| Element | Fixed Detail (isko kabhi na badlo) |
|---|---|
| **Kabir** | 22 saal, patla, **grey hoodie** (ek hi hoodie poori video), messy black hair, halki darhi, pale skin |
| **Maa** | 50 saal, **faded mustard cotton saree, thin maroon border**, grey-streaked hair low bun, chhota gold nose stud, sindoor, mangalsutra, glass bangles, simple chappal |
| **PG Room** | Single bed (grey bedsheet), **wooden study table**, plastic chair, yellow table lamp, window with iron grill, ek hi wooden door with **metal latch**, walls par halke nishaan |
| **Lighting A (Kabir alone)** | Cold blue-grey moonlight + weak warm lamp, low key, deep shadows |
| **Lighting B (Maa present)** | Warm amber 3200K, soft, glowing, halka halo |
| **Lens / Look** | 35mm, shallow DOF, film grain, photorealistic, cinematic |
| **Sound world** | Bahar ki thandi hawa, ghadi ki tik-tik, koi city noise nahi (isolation) |
| **Prohibited** | Koi jumpscare nahi, koi ghost makeup nahi, koi blue skin nahi, koi VFX smoke nahi — Maa **bilkul normal aur zinda** dikhni chahiye |

**Colour psychology:** Jahan tak Maa ka haath / roshni pahunchti hai = warm. Baaki sab cold. Climax me warm light **gayab** ho jaati hai — bas steam bachti hai.

---

## 🖼️ 2 · STEP 0 — CHEHRA LOCK (Sabse Pehle)

Luma ko sirf prompt se face yaad nahi rehta. Isliye pehle **4 images** banao aur phone/laptop me `refs/` folder me rakho.

### 2.1 Kabir — Character Sheet (Midjourney / Leonardo / Flux)
```
Character reference sheet, same 22-year-old Indian man in all three panels:
(A) neutral front portrait, (B) three-quarter profile looking down, tired,
(C) upper body in a grey hoodie sitting on a bed.
Messy black hair, light stubble, pale sick skin, dark circles, lean build.
Plain grey background, soft even studio light, photorealistic, RAW photo,
85mm lens, sharp skin texture, no makeup.
--ar 3:2 --style raw
```
> Midjourney ho toh: `--cref <image_url> --cw 100` lagao taaki teeno panel ka chehra ek jaisa rahe.

### 2.2 Kabir — Base Look (Luma ke liye clean single frame)
```
Portrait of a 22-year-old Indian man wearing a grey hoodie, messy hair, pale
sick face, tired half-closed eyes, sitting in a dim Indian PG hostel room at
night. Warm table lamp from the left, cold blue window light from the right.
Photorealistic, cinematic, 35mm, film grain.
--ar 9:16
```

### 2.3 Maa — Character Sheet
```
Character reference sheet, same 50-year-old Indian mother in all three panels:
(A) warm front portrait with a gentle peaceful smile,
(B) three-quarter view holding a steel glass,
(C) full body standing in a dim hallway in a faded mustard cotton saree.
Grey-streaked hair in a low bun, small gold nose stud, sindoor, mangalsutra,
glass bangles, kind eyes, weathered hands, simple chappals.
Photorealistic, RAW photo, 85mm, soft light, no glamour makeup.
--ar 3:2 --style raw
```

### 2.4 Maa — Base Look
```
Portrait of a 50-year-old traditional Indian mother wearing a simple faded
mustard cotton saree with a thin maroon border, grey-streaked hair in a low
bun, warm and peaceful motherly smile, kind eyes, standing in a dim hallway
holding a steel glass. Photorealistic, cinematic, 35mm, film grain.
--ar 9:16
```

**Face-lock checklist**
- [ ] Kabir ki 3 images save (`kabir_1..3.png`)
- [ ] Maa ki 3 images save (`maa_1..3.png`)
- [ ] Dono images 2x upscale (Magnific / Upscayl) — Luma me detail zyada retain hoti hai
- [ ] Ek hi base image **har** shot me use karo, aaj ek, kal doosri — nahi

---

## ⚙️ 3 · LUMA SETTINGS (Ek hi baar set karo)

| Setting | Value | Kyun |
|---|---|---|
| Model | **Ray2 / latest video model** | Face + skin texture best |
| Mode | **Image-to-Video** (start frame = base photo) | Character consistency |
| Keyframes | Sirf shot **4, 8B, 9A, 9B** me (start + end frame) | Controlled reveal & head-turn |
| Duration | **5 sec** per generation | 2–3 sec ka best part use karo |
| Aspect | **9:16** (Reels) / 16:9 (YouTube long) | Vertical-first |
| Resolution | 1080p (upscale baad me) | |
| Loop | **OFF** | |
| Camera motion | `static` ya `slow push-in` — bas ek motion | Multi-motion = face warp |
| Takes | Har shot ke **3 attempts**, hero shots (4, 8B, 9B) ke **5** | ~13 shots × 3 ≈ 40 generations |

### Negative Prompt (har generation me daalo)
```
extra fingers, deformed hands, distorted face, face morphing, warped eyes,
double limbs, plastic skin, oversaturated, cartoon, anime, 3d render,
text, subtitles, watermark, logo, jump scare, ghost makeup, blue skin,
harsh flash lighting, fisheye, blurry
```

---

## 🎥 4 · TIMELINE MAP (57 sec)

| # | Scene | In | Out | Dur | Shot |
|---|---|---|---|---|---|
| 1 | Bukhaar aur akelapan | 00:00.0 | 00:05.0 | 5.0 | 1A + 1B |
| 2 | Maa ki yaad | 00:05.0 | 00:09.0 | 4.0 | 2 |
| 3 | Darwaze par dastak | 00:09.0 | 00:13.0 | 4.0 | 3 |
| 4 | **Maa ka chehra (reveal)** | 00:13.0 | 00:17.5 | 4.5 | 4 |
| 5 | Maa ka aanchal | 00:17.5 | 00:25.5 | 8.0 | 5A + 5B |
| 6 | Maa ka jaana | 00:25.5 | 00:29.0 | 4.5 | 6 |
| 7 | Subah aur phone | 00:29.0 | 00:34.0 | 5.0 | 7 |
| 8 | **Papa ki call (twist)** | 00:34.0 | 00:43.5 | 9.5 | 8A + 8B |
| 9 | **Khaali gilaas ki bhaap** | 00:43.5 | 00:53.0 | 9.5 | 9A + 9B |
| 10 | End card | 00:53.0 | 00:57.0 | 4.0 | Text on black |

**Kyun split kiya?** Luma ek generation me ~5 sec deta hai. Original plan me Scene 5 (7s) aur Scene 8 (10s) ek hi prompt me the — usme motion toot jaata hai. Ab har shot ek hi beat karta hai: **ek shot = ek emotion = ek camera move.**

---

## 🎬 5 · SHOT-BY-SHOT MASTER SCRIPT

---

### 🩺 SCENE 1 [00:00.0 – 00:05.0] — BUKHAAR AUR AKELAPAN

#### SHOT 1A — Thermometer Insert [00:00.0 – 00:02.0]
**Luma Mode:** Text-to-Video · Static macro · **2 sec**

```
Macro extreme close-up of a small digital thermometer lying on a crumpled grey
bedsheet in a dark room. The display glows faint green, digits slightly out of
focus. A sweat-damp hand rests beside it. Cold blue moonlight, deep shadows,
shallow depth of field, photorealistic, film grain.
```
**Motion:** very slow push-in, no camera shake.
**⚠️ Text-trap:** Luma digits ko galat likhta hai — **prompt me "103.4" likhne ki koshish mat karo.** Number editing me overlay graphic se daalo.

#### SHOT 1B — Kabir ka bukhaar [00:02.0 – 00:05.0]
**Luma Mode:** Image-to-Video (Kabir base) · Handheld · **3 sec**

```
Cinematic close-up of a 22-year-old Indian man in a grey hoodie curled under a
thin blanket in a small dim PG room, shivering, sweat on his forehead, pale
skin, eyes half closed, breathing heavy. Warm yellow table lamp on the left,
cold blue window light on the right. Handheld with slight shake, 35mm,
photorealistic, film grain.
```
**Motion:** slow lateral drift right.
**SFX:** thandi hawa ka howl + ghadi *tik-tik* + kaanpti saansein + thermometer *beep-beep*.

**🎨 GRADE:** Temp −20 (cold), Contrast +12, Saturation −15, Vignette +25.
**🔊 MIX:** Hawa −18 dB, Ghadi −26 dB, Saans −14 dB, Beep −12 dB.

---

### 💭 SCENE 2 [00:05.0 – 00:09.0] — MAA KI YAAD

#### SHOT 2 — Aansu aur phone ki roshni
**Luma Mode:** Image-to-Video (Kabir base) · Dolly-in · **4 sec**

```
Close-up of a 22-year-old Indian man in a grey hoodie lying on his side in bed
in a dark PG room, his face lit only by the cold glow of a smartphone held a
few inches away. A single tear slides down his cheek, lips trembling. Shallow
depth of field, photorealistic skin texture, cinematic, film grain.
```
**Motion:** slow dolly-in, handheld micro-shake.
**SFX:** phone ki halki screen hum + ek lambi saans.

**🗣️ DIALOGUE (VO, whisper):**
> **कबीर:** *(kho gayi, kaanpti phusphusahat)* "Maa... bohot tez bukhaar hai... kaash aap yahan hoti..."
> *(Roman: "Maa... bohot tez bukhaar hai... kaash aap yahan hoti...")*

**🎨 GRADE:** Same cold grade, sirf face par phone ka cyan-glow rakho.

---

### 🚪 SCENE 3 [00:09.0 – 00:13.0] — DARWAZE PAR DASTAK

#### SHOT 3 — Ladkhadate kadam
**Luma Mode:** Image-to-Video (Kabir base) · Handheld follow · **4 sec**

```
Medium shot: a weak 22-year-old Indian man in a grey hoodie grips the wall and
staggers toward an old wooden door with a metal latch in a dim PG room, legs
shaking, blanket slipping off the bed behind him. Cold moonlight, deep shadows,
handheld camera following behind him, photorealistic, cinematic.
```
**Motion:** handheld follow, ek hi direction (peeche se aage).
**SFX:** *Khat-Khat-Khat* (lohe ki kundi) — door ke **pehle** 2 dastak sunai do, phir wo darwaza kholta hai. Nange paon ki chap-chap.

**🎨 GRADE:** Cold, shadows ko crush karo (−10 blacks).

---

### 🌼 SCENE 4 [00:13.0 – 00:17.5] — MAA KA CHEHRA (THE REVEAL)

#### SHOT 4 — Darwaza khulta hai
**Luma Mode:** **Keyframes** (Start = Kabir base + door · End = Maa base + steel glass) · Static · **4.5 sec**

```
The old wooden door swings open to reveal a 50-year-old Indian mother in a
faded mustard cotton saree with a thin maroon border, grey-streaked hair in a
low bun, small gold nose stud, holding a steel glass of hot turmeric milk with
thick white steam rising from it. She smiles a soft, peaceful, glowing smile.
Warm amber light spills onto the boy's shoulder in the foreground. Dim hallway
behind her. Photorealistic, cinematic, 35mm.
```
**Motion:** static camera, sirf door + steam move karein. **Chehra sthir rahe.**
**SFX:** *Creeeak* (darwaza) → 0.5 sec sannata → **Bansuri BGM in** (soft, single flute, no drums).

**🎨 GRADE (yeh cut sabse important hai):** Warm Golden Glow — Temp +25, Highlights +10, Contrast −5, skin me halka bloom. **Cut ke saath music bhi "khulna" chahiye.**
**👁️ Continuity:** Maa ki saree wahi hai jo usne aakhri baar dekhi thi — prompt me border ka colour zaroor repeat karo.

---

### 🤍 SCENE 5 [00:17.5 – 00:25.5] — MAA KA AANCHAL

#### SHOT 5A — Geela kapda [00:17.5 – 00:20.0]
**Luma Mode:** Image-to-Video (Maa base) · Static close-up · **2.5 sec**

```
Close-up: a 50-year-old Indian mother's weathered hand gently places a folded
wet white cloth on the forehead of her sleeping 22-year-old son in a grey
hoodie, his eyes closed. Warm table lamp light, dark room, tender, intimate,
photorealistic, shallow depth of field.
```

#### SHOT 5B — Haath sehlaana [00:20.0 – 00:25.5]
**Luma Mode:** Keyframes (Start = 5A end frame) · Slow push-in · **5.5 sec**

```
Close-up over-the-shoulder: the 50-year-old Indian mother in the faded mustard
saree sits on the edge of the bed and strokes her son's hair; the boy's
half-open feverish eyes look up at her with relief. Warm amber lamp light, soft
shadows, photorealistic, cinematic, 35mm.
```

**🗣️ DIALOGUE (VO):**
> **कबीर:** *(neend aur bukhaar me, dheema)* "Mummy... aap itni raat ko gaon se kaise aayi?" · `00:20.0 – 00:23.4`
> **मम्मी:** *(halka muskurakar, bahut pyaar se)* "Tujhe bukhaar ho, aur mujhe pata na chale? Chal... doodh pee le, so ja." · `00:23.6 – 00:27.6`

> **✂️ Editing note (J-cut):** Maa ki line shot 6 par **overlap** karegi — jab tak woh lamp bujha rahi hai, uski aawaz chalti rahegi. Yeh natural lagta hai aur 57 sec me dialogue fit ho jaata hai. Aawaz pehle, tasveer baad me = professional cut.

**🎨 GRADE:** Warm, soft — skin par ekdum halka peach tone, shadows lift +8.
**🔊 MIX:** BGM −22 dB, VO −6 dB.

---

### 🕯️ SCENE 6 [00:25.5 – 00:29.0] — MAA KA JAANA

#### SHOT 6 — Lamp band, darwaza band
**Luma Mode:** Image-to-Video (Maa base) · Static wide · **4.5 sec**

```
Medium wide shot in a dim PG room: the 50-year-old Indian mother in the faded
mustard saree turns off a yellow table lamp; the room falls into blue darkness;
she quietly walks to the wooden door and pulls it shut behind her, leaving her
son asleep in bed. Photorealistic, cinematic, static camera, film grain.
```
**Motion:** sirf Maa chale — camera bilkul na hile.
**SFX:** switch ka *click* (dry, close) → andhera → darwaze ka halka *clack*. **BGM 00:29.0 par hard cut — bilkul mute.**

**🎨 GRADE:** Lamp off hote hi temperature −30, exposure −1.5 stop. Screen andha ho jaana chahiye.
**💡 Detail jo goosebumps deta hai:** Door band hone ke baad **1 sec** ruko — koi kadmon ki aawaz nahi. Sirf sannata. (Hallway me jaane ki aawaz *nahi* aani chahiye.)

---

### 📱 SCENE 7 [00:29.0 – 00:34.0] — SUBAH AUR PHONE

#### SHOT 7 — Match cut: neend se subah
**Luma Mode:** Image-to-Video (Kabir base) · Static · **5 sec**

```
Soft grey morning daylight. The 22-year-old Indian man in a grey hoodie sits up
in bed looking healthy and calm, touches his forehead with a faint relieved
smile. Beside him on the wooden study table a smartphone lights up and vibrates,
sliding slightly on the surface. Photorealistic, cinematic, 35mm, film grain.
```
**✂️ EDIT:** Shot 6 ke sote hue Kabir se seedha jagte Kabir par **match cut** — dono frame me sirf gardan/sir ki position match kare.
**SFX:** BGM **0.0 sec** (achanak gayab) → phone ki *Bzzzz-Bzzzz* 2 baar → kambal ki sarsarahat.

**🎨 GRADE:** Neutral-cool subah (temp −8), halka haze, contrast soft. Pehli baar thodi "normalcy" — yeh sukoon audience ko dhoka dega.

---

### 💔 SCENE 8 [00:34.0 – 00:43.5] — PAPA KI CALL (THE TWIST)

#### SHOT 8A — Phone kaan par [00:34.0 – 00:37.0]
**Luma Mode:** Image-to-Video (Kabir base) · Static close-up · **3 sec**

```
Close-up: the 22-year-old Indian man presses a smartphone to his ear in a dim
room, listening; his face is calm, then his eyebrows pull together slightly.
Photorealistic, shallow depth of field, cinematic, film grain.
```

#### SHOT 8B — Chehra pathar ho jaata hai [00:37.0 – 00:43.5]
**Luma Mode:** Keyframes (Start = 8A end frame) · Extremely slow push-in · **6.5 sec**

```
Extreme close-up of a 22-year-old Indian man's face as shock lands: eyes widen
and go still, pupils tremble, jaw tightens, lips part slightly, tears well up
but do not fall. Stone-frozen, unblinking, NOT sobbing, no head movement.
Dim light, ARRI Alexa look, photorealistic, film grain.
```
**Motion:** sirf 10% push-in. Koi head turn nahi, koi kandha hilna nahi. **Is shot me "ro" mat karwao** — rona aawaz me hoga, chehre me nahi. Wahi ise heartbreaking banata hai.

**🗣️ DIALOGUE (VO + TELEPHONE FILTER):**
> **कबीर:** "Hello? Papa? Mummy kahan—" · `00:34.0 – 00:36.5`
>
> **पापा:** *(tooti hui, roti hui aawaz)* "Kabir... beta jaldi gaon aa ja! Teri Mummy... raat 12 baje... heart attack. Woh... chali gayi beta." · `00:37.0 – 00:43.5`
>
> *(aawaz shot 9A par overlap karti hai)* "Aakhri saans tak bas tera naam le rahi thi... 'Mera Kabir... mujhe uske paas jaana hai...'" · `00:43.5 – 00:46.5`

**📞 TELEPHONE FILTER RECIPE (CapCut / Premiere):**
1. High-pass filter **300 Hz** (neeche ki awaaz kaato)
2. Low-pass **3.4 kHz** (upar ki chamak kaato)
3. Peak EQ **+6 dB @ 1.2 kHz** (phone ki "nasal" quality)
4. Bit-crush / distortion **halka** (10–15%)
5. **Room reverb** — chhota, 0.4 sec decay (gaon ka kamra, phone ke us paar)
6. Volume **−3 dB** VO se neeche
7. Papa ki aawaz me **saans tootne** wali breath rakho — rone se pehle ek "hichki" jaisi awaaz. Sabse zyada wahi chubhta hai.

**🔊 SFX:** Background **pin-drop silence**. Sirf Papa ki aawaz, Kabir ki rukti hui saans, aur 00:43.0 par phone ke speaker se halka *click*.
**🎨 GRADE:** Saturation −35, contrast +8, skin par halka grey. Rang chehre se nikal jaana chahiye.

---

### 🥛 SCENE 9 [00:43.5 – 00:53.0] — KHAALI GILAAS KI BHAAP (CLIMAX)

#### SHOT 9A — Gardan ka slow turn [00:43.5 – 00:46.5]
**Luma Mode:** Keyframes (Start = 8B end frame · End = face tilted down) · Slow motion · **3 sec**

```
Slow motion close-up: the frozen, tearful 22-year-old Indian man slowly turns
his neck to look down toward the wooden study table beside his bed, expression
still blank and numb. Dark moody lighting, shallow depth of field,
photorealistic, cinematic.
```
**Motion:** sirf gardan — 40% speed (slow-mo post me bhi kar sakte ho, 0.4x par optical flow on).
**SFX:** 00:43.5 se **Heartbeat** — *Dhak-Dhak* 60 BPM se shuru, 3 beats me 90 BPM tak tez. Har beat par halka sub-bass (−20 Hz shelf +4 dB).

#### SHOT 9B — Khaali gilaas, garam bhaap [00:46.5 – 00:53.0]
**Luma Mode:** **Keyframes** (Start = glass base · End = same glass, steam thicker) · Static + 5% push-in · **6.5 sec**

```
Cinematic macro extreme close-up of an empty Indian stainless steel glass
standing on a wooden study table. Thick yellow turmeric milk residue and dried
stains along the bottom and inner sides, and thick white hot steam rising
clearly from the empty glass into the air. Dimly lit PG room bokeh background.
Mysterious, goosebumps, photorealistic, 8k, macro lens.
```
**Motion:** static camera, sirf bhaap upar uthe. **Koi haath, koi chehra frame me nahi.**

> **🎯 Yeh shot poori video ka payoff hai.** Kam se kam **5 takes** lo. Steam ko "thick, slow, curling" likho — patli dhundh jaisi bhaap nahi. Bhaap ke saath table par gilaas ki **reflection** bhi dikhni chahiye.

**SFX:** 00:46.5 par **Sad Violin** (single sustained note, phir dheere-dheere rise) + halka room tone. 00:52.0 par ek *riser*, jo end card par cut ho.
**🎨 GRADE:** Bhaap par ekdum halka **warm** tone (Maa ka last trace) — baaki frame cold. Yeh contrast hi message hai: *roshni chali gayi, bhaap reh gayi.*

---

### ⬛ END CARD [00:53.0 – 00:57.0]

- 00:53.0 – 00:54.0 → **Fade to black** (1 sec, dissolve nahi — seedha dip)
- 00:54.0 – 00:57.0 → Text fade-in, **pure white, thin serif / Poppins Light**, centre aligned:

> **"Maa ko maut bhi nahi rok sakti, jab uska bacha takleef mein ho... ❤️‍🩹"**

- Text **3 sec** screen par rahe, phir 0.5 sec black tail (end screen ke liye).
- Text ke saath **violin sustain** chalte rehna chahiye, 00:57.0 par cut.
- **Optional:** 00:56.0 par halka sa *heartbeat* wapas — ek beat, phir khatam. (Chills × 2)

---

## 🎙️ 6 · VOICEOVER RECORDING SHEET

| Role | Kaun | Tone | Mic / Notes |
|---|---|---|---|
| **Kabir** | 20–25 saal ka male voice | Dard bhara, kaanpta, dheema — kabhi loud nahi | Phone recorder bhi chalega, par room echo kam ho. Scene 2 whisper me, scene 8 normal |
| **Maa** | 45–55 saal ki female voice | Sukoon, pyaar, thakan nahi — "sab theek hai" wala bharosa | Maa ki aawaz me **koi ghostly effect nahi**. Bilkul normal, garam |
| **Papa** | 50–60 saal ka male voice | Toota hua, roti hui, saans phoolti hui | Telephone filter (upar recipe) |

**Recording tips:**
- Har line **3 baar** bolo — dheema, normal, aur "thoda zyada toota hua". Editor best uthayega.
- Har line ke pehle 2 sec **silence** record karo (noise profile ke liye).
- Devanagari lines voice artist ko WhatsApp par bhejo, Roman lines editor ke liye.

**AI voice use kar rahe ho?** ElevenLabs Hindi me "Kabir — Arjun/Chaitanya", "Maa — Vaishnavi/Kavya", "Papa — Ravi/Manthan" try karo. Stability **0.45**, Similarity **0.75**, Style **0.35** — zyada style me aawaz nakli lagti hai.

---

## 🔊 7 · SFX & MUSIC CUE SHEET (Timecode-wise)

| Time | Layer | Detail | Level |
|---|---|---|---|
| 00:00.0 | Hawa | Tez thandi hawa, window se | −18 dB |
| 00:00.3 | Ghadi | *Tik-tik*, slow, loop | −26 dB |
| 00:00.8 | Thermometer | *Beep-beep-beep* (3 baar) | −12 dB |
| 00:02.5 | Saans | Kaanpti, bhaari, close-mic | −14 dB |
| 00:05.5 | Screen hum | Phone glow ka halka electrical hum | −30 dB |
| 00:09.5 | Kundi | *Khat-Khat-Khat*, lohe par lohe ka | −10 dB |
| 00:11.5 | Kadam | Nange paon, chhap-chhap | −16 dB |
| 00:13.2 | Darwaza | *Creeeak* + latch ka *clack* | −10 dB |
| 00:13.8 | **Bansuri BGM** | Single flute, warm, no percussion, loop | −22 dB |
| 00:17.8 | Kapda | Geela kapda maathe par rakhne ki halki *slap* | −26 dB |
| 00:25.6 | Switch | Lamp ka *click* (dry, close) | −8 dB |
| 00:28.0 | Darwaza | Halka *clack* — band | −14 dB |
| **00:29.0** | **BGM CUT** | Bansuri **achanak band**, 0 fade | — |
| 00:29.2 | Phone | *Bzzzz-Bzzzz*, table par, 2 baar | −8 dB |
| 00:34.2 | Room tone | Subah ka halka silence, birds door | −34 dB |
| 00:37.0 | **Papa VO** | Telephone filter, roti hui | −3 dB |
| 00:43.0 | Speaker click | Phone ke andar se | −20 dB |
| **00:43.5** | **Heartbeat** | *Dhak-Dhak*, 60→90 BPM | −12 dB |
| 00:46.5 | **Violin** | Dard bhari, single sustain → rise | −16 dB |
| 00:52.0 | Riser | 1 sec, end card par cut | −20 dB |
| 00:54.0 | Violin tail | Sustain, fade | −22 dB |

**Mix rule:** VO **−6 dB** · Music **−22 dB** (duck to −26 under VO) · SFX **−8 se −26** · Master peak **−1 dBTP**. Koi bhi cheez **0 dB** par nahi.

---

## 🎨 8 · COLOUR GRADE (Scene-wise)

| Scene | Temp | Tint | Contrast | Sat | Special |
|---|---|---|---|---|---|
| 1 | −20 | +4 green | +12 | −15 | Vignette 25, glow bloom |
| 2 | −20 | +2 | +10 | −18 | Face par cyan glow preserve |
| 3 | −25 | 0 | +15 | −20 | Blacks −10 (crush) |
| **4 (reveal)** | **+25** | +6 warm | −5 | +5 | Bloom +15, highlight roll-off |
| 5 | +22 | +8 | −2 | +8 | Skin peach, shadows +8 |
| 6 | −30 | 0 | +20 | −25 | Exposure −1.5 stop |
| 7 | −8 | 0 | −5 | −5 | Haze / fog +10 |
| 8 | −5 | −4 | +8 | −35 | Grey skin, tears highlight |
| 9 | −22 | 0 | +18 | −20 | **Sirf bhaap warm** |
| End | — | — | — | — | Pure black + white text |

**Finishing:** film grain **8–12%** (sab shots par same), subtle chromatic aberration 2%, 24 fps timeline (slow-mo shots 0.4x), letterbox **nahi** (vertical hai).

---

## 📤 9 · EXPORT SETTINGS

| Platform | Spec |
|---|---|
| Reels / Shorts | 1080×1920 · 30 fps · H.264 · 12–16 Mbps · AAC 320 kbps · < 60 sec |
| YouTube (long) | 1920×1080 · 24 fps · 20 Mbps · same audio |
| Thumbnail | 1080×1920 frame from Shot 9B + text overlay |

---

## 📝 10 · CAPTIONS (`subtitles.srt` repo me ready hai)

Rules: max **2 lines**, max **32 characters per line**, white text + black shadow/stroke 2px, bottom safe area se **12% upar**. Captions **dialogue only** — sound effects nahi.

---

## 📦 11 · PACKAGING

### Hook (0–2 sec text overlay — optional but story ke liye zaroori)
> **"Raat 12 baje Maa chali gayi... phir bhi darwaze par khadi thi."**

### Title options
1. **Maa Ka Aanchal** — *Raat 12 Baje Chali Gayi Thi Maa...*
2. **Khaali Gilaas** — Ek Sachchi Maa Ki Kahani
3. **Aakhri Bhaap** | Maa Ki Mohabbat Ka Sabse Dard Bhara Saboot

### Description
```
Raat 12 baje Maa ko heart attack aaya. Subah Papa ka phone aaya... par us raat
darwaze par kaun tha? Ek 57-second emotional story — Maa ki mamta, jo maut se
bhi bada hai.

🎬 Luma Dream Machine Pro — Premium Edition
#maa #emotionalstory #hindistory #shorts
```

### Hashtags
`#maa #mamta #emotional #hindistories #sadstory #shorts #reels #hearttouch #lumaai #aistories #motherlove #emotionalvideo`

### Thumbnail prompt
```
Extreme close-up of an empty steel glass with thick white steam rising and
yellow turmeric stains, in a dark room, one blurred tearful brown eye reflected
in the steel. Photorealistic, moody, cinematic, 9:16.
```

---

## ✂️ 12 · 30-SECOND VERTICAL CUTDOWN (extra reach ke liye)

| Time | Shot | Change |
|---|---|---|
| 00:00–00:04 | 1B + 5A (intercut) | Hook: thermometer beep + "Maa... kaash aap yahan hoti" |
| 00:04–00:10 | 4 | Reveal (full) |
| 00:10–00:15 | 5B | "Chal, doodh pee le, so ja" |
| 00:15–00:18 | 6 | Lamp off |
| 00:18–00:24 | 8A → 8B | "Hello Papa? Mummy kahan—" / "Woh chali gayi beta" |
| 00:24–00:30 | 9B | Gilaas + bhaap + end text |

Yeh version me Scene 2, 3, 7 kaat do. **Hook pehle 2 sec me dard dena chahiye.**

---

## 🧯 13 · TROUBLESHOOTING

| Problem | Fix |
|---|---|
| Chehra har shot me badal jaata hai | Base image har shot me start frame banao; prompt me wardrobe words repeat karo (grey hoodie / faded mustard saree). Post me **InsightFace / face swap** se last 5% fix karo. |
| Luma hands bigaad raha hai | Haath ko frame se bahar rakho — shot ko over-the-shoulder ya insert banao (glass, kapda, phone). |
| Steam nahi aa rahi | "thick white hot steam rising, curling" + "kettle just poured" phrase add karo; ya CapCut me steam overlay + screen blend mode. |
| Awaaz aur lips match nahi | **Luma me lips mat khulwao.** Dialogue off-screen rakho, ya chehra profile/insert me dikhao. Yehi is script ka design hai. |
| Digits text galat aa raha | Prompt se numbers hatao, number **graphic overlay** se daalo. |
| Video "nakli" lag rahi | Grain, halka chromatic aberration, real SFX layers, aur music ki **hard cut** — yeh 4 cheezein AI video ko real bana deti hain. |
| Emotion nahi aa raha | Rona chehre par nahi, **aawaz aur sannate** me hai. Shot 8B me koi aansu na bahao — bas aankh sthir. |

---

## ✅ 14 · PRODUCTION CHECKLIST

**PRE**
- [ ] Kabir base + character sheet (3 images)
- [ ] Maa base + character sheet (3 images)
- [ ] Refs 2x upscale
- [ ] Luma settings: Ray2, 5s, 9:16, keyframes on
- [ ] Negative prompt set

**GENERATE (13 shots × 3 takes)**
- [ ] 1A [ ] 1B [ ] 2 [ ] 3 [ ] 4 *(5 takes)*
- [ ] 5A [ ] 5B [ ] 6 [ ] 7 [ ] 8A [ ] 8B *(5 takes)*
- [ ] 9A [ ] 9B *(5 takes)*

**AUDIO**
- [ ] Kabir VO (2 lines) [ ] Maa VO (1 line) [ ] Papa VO (2 parts)
- [ ] Telephone filter on Papa
- [ ] SFX layers (13 cues)
- [ ] Bansuri BGM + hard cut
- [ ] Heartbeat + violin

**POST**
- [ ] Timeline 24 fps, 13 shots placed
- [ ] J-cut on Maa's line (shot 5B → 6)
- [ ] J-cut on Papa's line (shot 8B → 9A)
- [ ] Match cut Scene 6 → 7
- [ ] Grade per scene
- [ ] Grain 10% uniform
- [ ] SRT import + styling
- [ ] End card text 3 sec
- [ ] Export 1080×1920 · 30 fps · 14 Mbps

---

## 📁 15 · REPO FILES

| File | Kya hai |
|---|---|
| `MASTER-SCRIPT.md` | Yeh file — poora blueprint |
| `prompts.csv` | 13 shots ke copy-paste prompts (sheet me kholo, ek-ek cell copy karo) |
| `subtitles.srt` | Ready captions, import karo |
| `banner.png` | Project banner |

---

**🎯 Aakhri baat:** Is script me sab kuch set hai — lekin poori video ka 70% **aawaz** hai. Agar Papa ki aawaz me woh ek "tooti hui saans" nahi aayi, toh duniya ka best Luma shot bhi kaam nahi karega. Pehle audio banao, phir video.

*— Luma Dream Machine Pro · Premium Edition*
