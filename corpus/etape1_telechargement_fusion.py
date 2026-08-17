"""
Etape 1 - Telechargement et fusion des datasets
================================================
Telecharge EmpathicDialogues et DailyDialog depuis HuggingFace
et les fusionne dans un format unifie (source, conv_id, context, utterance, emotion).

Usage:
    pip install datasets pandas
    python etape1_telechargement_fusion.py

Auteurs : Zinedine Hamadi & Sara Hadidi
Memoire : M1 Sciences du Langage et Informatique - Sorbonne Universite 2025/2026
"""

import pandas as pd
from datasets import load_dataset
import os

OUTPUT_FILE = "corpus_brut.csv"

rows = []

# EmpathicDialogues
print("Chargement EmpathicDialogues...")
ed = load_dataset("Estwld/empathetic_dialogues_llm")

for split in ed.keys():
    for conv_id, (convs, emotion) in enumerate(
        zip(ed[split]["conversations"], ed[split]["emotion"])
    ):
        turns = []
        for turn in convs:
            utt = turn.get("content", "").strip() if isinstance(turn, dict) else str(turn).strip()
            if utt:
                turns.append(utt)

        for i, utt in enumerate(turns):
            context = turns[i - 1] if i > 0 else ""
            rows.append({
                "source":   "empathic_dialogues",
                "conv_id":  f"ed_{split}_{conv_id}",
                "context":  context,
                "utterance": utt,
                "emotion":  emotion,
            })

print(f"  -> {len(rows):,} paires EmpathicDialogues")

# DailyDialog
print("Chargement DailyDialog...")
dd = load_dataset("frankdarkluo/DailyDialog")

dd_start = len(rows)
for split in dd.keys():
    for conv_id, dialog in enumerate(dd[split]["dialog"]):
        turns = [t.strip() for t in dialog if t.strip()]
        for i, utt in enumerate(turns):
            context = turns[i - 1] if i > 0 else ""
            rows.append({
                "source":    "daily_dialog",
                "conv_id":   f"dd_{split}_{conv_id}",
                "context":   context,
                "utterance": utt,
                "emotion":   "no_emotion",
            })

print(f"  -> {len(rows) - dd_start:,} paires DailyDialog")

# Fusion et sauvegarde
df = pd.DataFrame(rows)
df = df[df["utterance"].str.strip() != ""].reset_index(drop=True)
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print(f"\nTotal : {len(df):,} paires")
print(f"Fichier sauvegarde : {OUTPUT_FILE}")
print(df["source"].value_counts().to_string())
