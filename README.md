# 🇰🇲 OpenShikomori — Open-source Comorian AI

[English](README.md) | [Français](README.fr.md) | [العربية](README.ar.md)

> **The first open-source effort to build a Speech-to-Text and Language Model for Comorian (Shikomori)** — a low-resource language spoken by ~800,000 people across the Comoros Islands.

---

## 🌍 Why This Project Exists

Comorian (Shikomori) has **no existing AI language model**, no public speech dataset, and no automatic transcription tool. **OpenShikomori** aims to change that — starting with a trustworthy public shell for voice collection and building toward a full ASR + LLM pipeline optimized for African languages.

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

---

## 🗺️ Roadmap

### Phase 1 — Public Foundation & Trust *(Now)*
- [x] Open-source web shell for mission framing
- [x] Privacy-first contribution model
- [ ] Multilingual support (Comorian, French, English, Arabic)
- [ ] First 10-hour reviewed speech target

### Phase 2 — Recording & Contributor Entry
- [ ] Contributor profiles and dialect selection
- [ ] Managed recording prompts (Web & Mobile)
- [ ] Private audio submission pipeline

### Phase 3 — Scale & Dataset Release
- [ ] Target: 100+ hours of corrected Comorian audio+text
- [ ] Public dataset release on HuggingFace 🤗
- [ ] Fine-tuned Whisper ASR model

### Phase 4 — Translation & LLM
- [ ] Parallel corpus: Comorian ↔ French ↔ English
- [ ] Fine-tune NLLB-200 for translation
- [ ] Deploy accessible translation tools for the Comorian community

---

## 🤝 How to Contribute

### I am a native Comorian speaker
This is the most valuable contribution you can make:
1. Review transcription files and correct errors
2. Record yourself reading text passages via our upcoming web shell
3. Help identify which dialect is spoken in audio files

### I am a developer / ML engineer
1. Improve the recording shell (`website/`)
2. Build the fine-tuning notebooks
3. Help with data formatting for HuggingFace

---

## 💖 Sponsorship

We are looking for partners and individual sponsors to help fund the compute costs and data collection efforts for this project.

*Sponsors will be listed here.*

[**Become a Sponsor**](https://github.com/sponsors/fanom2813)

---

## 📜 License

This project is licensed under the **MIT License**. Collected transcriptions and datasets are intended to be released under **CC BY 4.0**.

---

## 👤 Author

**[@fanom2813](https://github.com/fanom2813)**

Built with ❤️ for the Comorian people and language.

---

<div align="center">

**🇰🇲 Preserving Shikomori, one word at a time**

⭐ Star this repo if you support African language AI

</div>
