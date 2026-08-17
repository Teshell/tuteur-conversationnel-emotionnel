# Tuteur Conversationnel Emotionnel

**Memoire M1 — Sciences du Langage et Informatique**
Sorbonne Universite — 2025/2026

**Auteurs :** Zinedine Hamadi & Sara Hadidi
**Encadrement :** Nour El Houda Ben Chaabene & Victoria Eyharabide — STIH Laboratory, Sorbonne Universite

---

## Description

Ce projet implemente un tuteur conversationnel base sur un LLM, capable de :
1. **Detecter les emotions** de l'apprenant (stress, frustration, engagement, confusion, satisfaction, neutre)
2. **Adapter ses reponses pedagogiques** en fonction de l'etat emotionnel detecte
3. **Fournir des explications interpretables** (XAI) sur ses decisions

Le systeme s'articule en trois modules :
- **Module 1 — EmoBERT** : classifieur d'emotions fine-tune sur RoBERTa
- **Module 2 — Pipeline** : connexion EmoBERT → LLM via injection de contexte emotionnel
- **Module 3 — XAI** : visualisation d'attention + templates linguistiques

---

## Resultats

| Version | Strategie | Accuracy | F1-macro |
|---------|-----------|----------|----------|
| v1 | Baseline (corpus desequilibre) | 0.62 | 0.20 |
| v2 | Sous-echantillonnage neutre + GoEmotions | 0.69 | 0.58 |
| v3a | + Data augmentation Zephyr-7B | 0.61 | 0.52 |
| v3b | + Class weights | 0.59 | 0.57 |
| v4 | + Context simple + modele specialise | 0.63 | 0.59 |
| **v5** | **+ Contexte multi-tours + seuil neutre=0.6** | **0.63** | **0.60** |

**Accord inter-annotateurs :** kappa = 0.79 (emotions) | kappa = 0.92 (metacognition)

---

## Structure du depot

```
tuteur-conversationnel-emotionnel/
├── corpus/
│   ├── etape1_telechargement_fusion.py
│   ├── etape2_filtrage_nettoyage.py
│   ├── etape3a_extraction_annotation.py
│   ├── etape3b_accord_interannotateurs.py
│   └── make_annotation_excel.py
├── emobert/
│   ├── reequilibrage_v5_multiturn.ipynb
│   └── analyse_erreurs.ipynb
├── pipeline/
│   ├── emotion_classifier.py
│   ├── prompt_builder.py
│   ├── llm_client.py
│   ├── pipeline.py
│   └── strategies.yaml
├── xai/
│   ├── xai_explainer.py
│   ├── xai_templates.yaml
│   └── xai_colab.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

```bash
# Cloner le depot
git clone https://github.com/Teshell/tuteur-conversationnel-emotionnel.git
cd tuteur-conversationnel-emotionnel

# Creer un environnement virtuel
python3.11 -m venv venv
source venv/bin/activate

# Installer les dependances
pip install -r requirements.txt
```

---

## Utilisation

### 1. Assembler le corpus

```bash
cd corpus/
python etape1_telechargement_fusion.py
python etape2_filtrage_nettoyage.py
python etape3a_extraction_annotation.py
# Annoter manuellement les fichiers CSV generes
python etape3b_accord_interannotateurs.py
```

### 2. Entrainer EmoBERT (Google Colab recommande — GPU T4)

Ouvrir `emobert/reequilibrage_v5_multiturn.ipynb` sur [Google Colab](https://colab.research.google.com).

### 3. Lancer le pipeline

```bash
cd pipeline/
python pipeline.py
```

---

## Datasets utilises

| Dataset | Source | Usage |
|---------|--------|-------|
| EmpathicDialogues | [HuggingFace](https://huggingface.co/datasets/Estwld/empathetic_dialogues_llm) | Corpus + fine-tuning 32 classes |
| DailyDialog | [HuggingFace](https://huggingface.co/datasets/frankdarkluo/DailyDialog) | Corpus |
| GoEmotions | [HuggingFace](https://huggingface.co/datasets/google-research-datasets/go_emotions) | Enrichissement classes rares |

---

## Technologies

- **Python 3.11**
- **HuggingFace Transformers** — RoBERTa, Zephyr-7B
- **PyTorch** — entraînement GPU
- **scikit-learn** — metriques, class weights
- **Google Colab** — GPU T4 (15GB VRAM)

---

## Publication

Ce travail a ete soumis a la conference **MMM 2027** :

> Hamadi Z., Hadidi S., Ben Chaabene N.E.H., Eyharabide V. (2027).
> *Emotion-Aware Conversational Tutoring: A Reproducible Pipeline for Educational Dialogue and an Honest Account of What Remains Open.*
> MMM 2027.

---

## Licence

Projet academique — Sorbonne Universite 2025/2026.
