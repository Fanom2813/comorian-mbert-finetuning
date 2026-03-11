# 🇰🇲 Shikomori AI — Comorian Language Speech & NLP Project

> **The first open-source effort to build a Speech-to-Text and Language Model for Comorian (Shikomori)** — a low-resource language spoken by ~800,000 people across the Comoros Islands.

---

## 🌍 Why This Project Exists

Comorian (Shikomori) has **no existing AI language model**, no public speech dataset, and no automatic transcription tool. This project aims to change that — starting from raw audio collected from the web, building toward a full ASR + LLM pipeline optimized for African languages.

This is not just a research project. It is an act of **language preservation**.

---

## 🎯 Project Goals

| Goal | Status |
|------|--------|
| 🎙️ Collect Comorian audio from the web | 🔄 In Progress |
| 📝 Transcribe audio using Whisper | 🔄 In Progress |
| ✅ Correct transcriptions with native speakers | 🔄 In Progress |
| 📦 Build public Comorian audio+text dataset | 🔜 Planned |
| 🤖 Fine-tune Whisper ASR on Comorian | 🔜 Planned |
| 🧠 Fine-tune African LLM on Comorian text | 🔜 Planned |
| 🚀 Publish models on HuggingFace Hub | 🔜 Planned |

---

## 🗣️ About the Language

**Shikomori** (also called Comorian) is a Bantu language with strong Arabic and French influences, spoken across four islands:

| Dialect | Island |
|---------|--------|
| Shingazidja | Grande Comore (Ngazidja) |
| Shimwali | Mohéli (Mwali) |
| Shindzuani | Anjouan (Ndzuani) |
| Shimaore | Mayotte |

Linguistic family: **Bantu → Sabaki branch → closely related to Swahili**
Additional influences: **Arabic** (religious vocabulary), **French** (modern loanwords)

---

## 🏗️ Architecture

```
                    PHASE 1 — RECORD & TRANSCRIBE
    ┌─────────────────────────────────────────────────────┐
    │  Record Voice / Web Audio                          │
    │  faster-whisper large-v3 (Swahili mode)            │
    │  → Raw Transcription → Native Speaker Correction   │
    └─────────────────────┬───────────────────────────────┘
                          │
                    PHASE 2 — FINE-TUNE WHISPER
    ┌─────────────────────▼───────────────────────────────┐
    │  Corrected audio+text pairs (10-50h)               │
    │  → Fine-tune whisper-small on Comorian             │
    │  → Auto-transcribe MORE audio → Snowball effect    │
    └─────────────────────┬───────────────────────────────┘
                          │
                    PHASE 3 — SCALE DATASET
    ┌─────────────────────▼───────────────────────────────┐
    │  Fine-tuned Whisper → Bulk transcription            │
    │  → Correct → Retrain → 100+ hours dataset          │
    │  → Publish on HuggingFace 🤗                       │
    └─────────────────────┬───────────────────────────────┘
                          │
                    PHASE 4 — TRANSLATION AI
    ┌─────────────────────▼───────────────────────────────┐
    │  Parallel corpus: Comorian ↔ French ↔ English      │
    │  Fine-tune NLLB-200 for translation                │
    │  → Translation app for Comorian people             │
    └─────────────────────────────────────────────────────┘
```

### 💻 Compute Strategy (All Free)
| Platform | GPU | Hours/Week | Best For |
|----------|-----|------------|----------|
| Google Colab | T4 (16 GB) | ~15-30h | Recording, transcription, experiments |
| Kaggle | P100 or 2×T4 | **30h** | Fine-tuning (heavy lifting) |
| **Combined** | — | **~50-60h** | Everything needed for Phase 1-3 |

---

## 📁 Repository Structure

```
comorian-mbert-finetuning/
│
├── 📓 01_transcribe.ipynb        # Record/upload → transcribe with Whisper
├── 📓 02_finetune_whisper.ipynb   # Fine-tune Whisper on corrected Comorian data
├── 📓 03_translate.ipynb          # Build Comorian ↔ French ↔ English translation
│
├── 📚 data/
│   └── raw/                       # Raw audio (not committed — too large)
│
└── README.md
```

---

## 🚀 Quick Start

### Transcribe (Google Colab)
1. Open `01_transcribe.ipynb` in [Google Colab](https://colab.research.google.com)
2. Go to `Runtime` → `Change runtime type` → Select **T4 GPU**
3. Run all cells — record your voice or load audio from Drive
4. Review and correct transcriptions

### Fine-tune Whisper (Kaggle recommended)
1. Collect 10-50 hours of corrected audio+text pairs
2. Open `02_finetune_whisper.ipynb` on [Kaggle](https://kaggle.com) (30h/week free GPU)
3. Train and export your Comorian Whisper model

### Translation (Kaggle recommended)
1. Build a parallel corpus (Comorian + French + English)
2. Open `03_translate.ipynb` on Kaggle
3. Fine-tune NLLB-200 for Comorian translation

---

## ⚙️ Pipeline Settings

### Transcription (faster-whisper)
| Setting | Value | Why |
|---------|-------|-----|
| `no_speech_threshold` | `0.3` | Helps skip non-speech while still catching quiet speech |
| `log_prob_threshold` | `-1.5` | Flags low-confidence decoding more aggressively |
| `compression_ratio_threshold` | `3.0` | Rejects pathological decoding loops |
| `condition_on_previous_text` | `True` | Uses context for better guessing |
| `word_timestamps` | `True` | Enables timestamp-aware decoding; notebook saves segment timestamps |
| `language` | `auto → sw fallback` | Auto-detect first, then retry with Swahili for mixed Comorian clips |

---

## 📄 Output Format

For each audio file, the pipeline produces:

**`filename_transcript.txt`** — Clean full text:
```
Source File  : story_01.mp3
Model        : faster-whisper large-v3
Selected Pass : auto-detect
Requested Lang: auto
Detected Lang : sw
Lang Prob     : 0.62
Avg Logprob   : -0.24
Transcribed  : 2025-03-10 14:32
=======================================================

Salamualaikum warahmatullahi wabarakatuh
Habar Zaho, wa jeje, wa mirongolo omar...
```

**`filename_timestamps.txt`** — Timestamped with confidence:
```
Source        : story_01.mp3
Selected Pass : auto-detect
Detected Lang : sw
Avg Logprob   : -0.24
🟢 > -0.3 confident | 🟡 uncertain | 🔴 needs correction
=======================================================

[1.7s → 5.7s]  🟢 (-0.12)  Salamualaikum warahmatullahi wabarakatuh
[5.7s → 16.2s] 🟢 (-0.24)  Habar Zaho, wa jeje, wa mirongolo omar
[19.0s → 30.9s] 🟡 (-0.55)  silawa, harma, ikartie...
```

### Confidence Indicators
| Icon | Score | Meaning |
|------|-------|---------|
| 🟢 | `avg_logprob > -0.3` | Whisper is confident — likely correct |
| 🟡 | `-0.7 < avg_logprob <= -0.3` | Uncertain — worth reviewing |
| 🔴 | `avg_logprob <= -0.7` | Guessing — needs human correction |

---

## 📊 Current Accuracy Results

Tested on a ~90 second Comorian audio sample:

| Model | Accuracy | Confidence | Notes |
|-------|----------|------------|-------|
| openai-whisper large | ~71% | 0.67–0.97 | Baseline |
| faster-whisper large-v3 | **~92%** | **0.91–0.98** | Current |
| Fine-tuned on Comorian | ~97%+ | TBD | Future goal |

---

## 🗺️ Roadmap

### Phase 1 — Record & Transcribe *(Now)*
- [x] Pipeline with faster-whisper large-v3
- [x] Voice recording in browser
- [x] Google Drive integration
- [ ] Record 10-50 hours of Comorian speech
- [ ] Correct transcriptions with native speakers

### Phase 2 — Fine-tune Whisper on Comorian *(2-4 months)*
- [ ] Format corrected audio+text as HuggingFace dataset
- [ ] Fine-tune `openai/whisper-small` on Comorian (Kaggle — 30h/week free GPU)
- [ ] Evaluate WER improvement
- [ ] Use fine-tuned model to transcribe MORE audio faster (snowball)

### Phase 3 — Scale Dataset *(4-8 months)*
- [ ] Snowball: fine-tuned Whisper → auto-transcribe → correct → retrain
- [ ] Target: 100+ hours of corrected Comorian audio+text
- [ ] Publish dataset on HuggingFace 🤗

### Phase 4 — Translation AI *(8-12 months)*
- [ ] Build parallel corpus: Comorian ↔ French ↔ English
- [ ] Fine-tune NLLB-200 (Meta's translation model)
- [ ] Build translation app
- [ ] Mobile app (Android first — most used in Comoros)

---

## 🤝 How to Contribute

### I am a native Comorian speaker
This is the most valuable contribution you can make:
1. Review transcription files and correct errors
2. Record yourself reading text passages
3. Help identify which dialect is spoken in audio files

### I am a developer / ML engineer
1. Improve the transcription pipeline
2. Build the fine-tuning notebook
3. Help with data formatting for HuggingFace
4. Build the correction review tool

### I have audio recordings
1. Stories, speeches, radio, TV, podcasts in Comorian
2. Open an issue or send a PR with the source links

---

## 🌍 Related Projects & Communities

| Project | Description | Link |
|---------|-------------|------|
| **Masakhane** | NLP for African languages | [masakhane.io](https://masakhane.io) |
| **AfricaNLP** | African language AI workshop | ACL/EMNLP |
| **Mozilla Common Voice** | Crowdsourced voice dataset | [commonvoice.mozilla.org](https://commonvoice.mozilla.org) |
| **MMS by Meta** | ASR for 1000+ languages | [HuggingFace](https://huggingface.co/facebook/mms-300m) |
| **AfriBERTa** | BERT for African languages | [HuggingFace](https://huggingface.co/castorini/afriberta_large) |
| **AfroXLMR** | XLM-R for African languages | [HuggingFace](https://huggingface.co/Davlan/afro-xlmr-large) |

---

## 📚 References

- Whisper: [Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) — OpenAI
- faster-whisper: [CTranslate2 implementation of Whisper](https://github.com/SYSTRAN/faster-whisper)
- AfriBERTa: [Few-shot Learning for African Languages](https://arxiv.org/abs/2111.07978)
- Masakhane: [Participatory Research for Low-resource Language NLP](https://arxiv.org/abs/2010.07445)

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](https://github.com/fanom2813/shikomori-ai/blob/main/LICENSE) for details.

All collected audio data respects the original sources' terms of use. Transcriptions are released under **CC BY 4.0**.

---

## 👤 Author

**[@fanom2813](https://github.com/fanom2813)**

Built with ❤️ for the Comorian people and language.

> *"A language is not just a way of communicating — it is a way of seeing the world."*

---

<div align="center">

**🇰🇲 Preserving Shikomori, one word at a time**

⭐ Star this repo if you support African language AI

</div>
