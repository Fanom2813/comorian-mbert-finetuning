# 🇰🇲 OpenShikomori — IA Comorienne Open-Source

[English](README.md) | [Français](README.fr.md) | [العربية](README.ar.md)

> **Le premier effort open-source pour construire un modèle de reconnaissance vocale (Speech-to-Text) et de langage pour le comorien (Shikomori)** — une langue à faibles ressources parlée par environ 800 000 personnes dans l'archipel des Comores.

---

## 🌍 Pourquoi ce projet existe

Le comorien (Shikomori) ne dispose d'**aucun modèle de langage IA existant**, d'aucun ensemble de données vocales public et d'aucun outil de transcription automatique. **OpenShikomori** vise à changer cela — en commençant par une interface publique de confiance pour la collecte de voix et en évoluant vers un pipeline complet ASR + LLM optimisé pour les langues africaines.

Ce n'est pas seulement un projet de recherche. C'est un acte de **préservation linguistique**.

---

## 🎯 Objectifs du projet

| Objectif | Statut |
|----------|--------|
| 🎙️ Collecter de l'audio comorien sur le web | 🔄 En cours |
| 📝 Transcrire l'audio avec Whisper | 🔄 En cours |
| ✅ Corriger les transcriptions avec des locuteurs natifs | 🔄 En cours |
| 📦 Construire un dataset public audio+texte comorien | 🔜 Prévu |
| 🤖 Fine-tuner Whisper ASR pour le comorien | 🔜 Prévu |
| 🧠 Fine-tuner un LLM africain sur le texte comorien | 🔜 Prévu |
| 🚀 Publier les modèles sur HuggingFace Hub | 🔜 Prévu |

---

## 🗣️ À propos de la langue

Le **Shikomori** (également appelé comorien) est une langue bantoue avec de fortes influences arabes et françaises, parlée sur quatre îles :

| Dialecte | Île |
|----------|-----|
| Shingazidja | Grande Comore (Ngazidja) |
| Shimwali | Mohéli (Mwali) |
| Shindzuani | Anjouan (Ndzuani) |
| Shimaore | Mayotte |

Famille linguistique : **Bantou → Branche Sabaki → étroitement lié au Swahili**
Influences additionnelles : **Arabe** (vocabulaire religieux), **Français** (emprunts modernes)

---

## 🏗️ Architecture

```
                    PHASE 1 — ENREGISTREMENT & TRANSCRIPTION
    ┌─────────────────────────────────────────────────────┐
    │  Enregistrement Voix / Audio Web                    │
    │  faster-whisper large-v3 (mode Swahili)             │
    │  → Transcription brute → Correction par locuteurs   │
    └─────────────────────┬───────────────────────────────┘
                          │
                    PHASE 2 — FINE-TUNING WHISPER
    ┌─────────────────────▼───────────────────────────────┐
    │  Paires audio+texte corrigées (10-50h)              │
    │  → Fine-tuning whisper-small sur le comorien        │
    │  → Auto-transcription de PLUS d'audio → Effet boule │
    └─────────────────────┬───────────────────────────────┘
                          │
                    PHASE 3 — MISE À L'ÉCHELLE DU DATASET
    ┌─────────────────────▼───────────────────────────────┐
    │  Whisper fine-tuné → Transcription en masse         │
    │  → Correction → Réentraînement → Dataset 100h+      │
    │  → Publication sur HuggingFace 🤗                   │
    └─────────────────────┬───────────────────────────────┘
                          │
                    PHASE 4 — IA DE TRADUCTION
    ┌─────────────────────▼───────────────────────────────┐
    │  Corpus parallèle : Comorien ↔ Français ↔ Anglais   │
    │  Fine-tuning NLLB-200 pour la traduction            │
    │  → App de traduction pour le peuple comorien        │
    └─────────────────────────────────────────────────────┘
```

---

## 🗺️ Feuille de route (Roadmap)

### Phase 1 — Fondation publique et confiance *(Actuel)*
- [x] Interface web open-source pour le cadrage de la mission
- [x] Modèle de contribution respectueux de la vie privée
- [ ] Support multilingue (Comorien, Français, Anglais, Arabe)
- [ ] Cible : 10 premières heures de parole révisées

### Phase 2 — Enregistrement et entrée des contributeurs
- [ ] Profils de contributeurs et sélection du dialecte
- [ ] Prompts d'enregistrement gérés (Web & Mobile)
- [ ] Pipeline de soumission audio privée

### Phase 3 — Échelle et sortie du dataset
- [ ] Cible : 100+ heures d'audio+texte comorien corrigé
- [ ] Sortie du dataset public sur HuggingFace 🤗
- [ ] Modèle Whisper ASR fine-tuné

### Phase 4 — Traduction et LLM
- [ ] Corpus parallèle : Comorien ↔ Français ↔ Anglais
- [ ] Fine-tuning NLLB-200 pour la traduction
- [ ] Déploiement d'outils de traduction accessibles pour la communauté comorienne

---

## 🤝 Comment contribuer

### Je suis un locuteur natif comorien
C'est la contribution la plus précieuse que vous puissiez apporter :
1. Réviser les fichiers de transcription et corriger les erreurs
2. Vous enregistrer en lisant des passages de texte via notre future interface web
3. Aider à identifier quel dialecte est parlé dans les fichiers audio

### Je suis un développeur / ingénieur ML
1. Améliorer l'interface d'enregistrement (`website/`)
2. Construire les carnets de notes (notebooks) de fine-tuning
3. Aider au formatage des données pour HuggingFace

---

## 💖 Parrainage (Sponsorship)

Nous recherchons des partenaires et des parrains individuels pour aider à financer les coûts de calcul et les efforts de collecte de données pour ce projet.

*Les parrains seront listés ici.*

[**Devenir parrain**](https://github.com/sponsors/fanom2813)

---

## 📜 Licence

Ce projet est sous licence **MIT**. Les transcriptions et les ensembles de données collectés sont destinés à être publiés sous **CC BY 4.0**.

---

## 👤 Auteur

**[@fanom2813](https://github.com/fanom2813)**

Construit avec ❤️ pour le peuple et la langue comorienne.

---

<div align="center">

**🇰🇲 Préserver le Shikomori, un mot à la fois**

⭐ Star ce repo si vous soutenez l'IA pour les langues africaines

</div>
