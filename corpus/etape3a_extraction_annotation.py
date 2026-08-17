"""
Etape 3a - Extraction des dialogues a annoter
=============================================
A partir du corpus filtre (corpus_edu_nettoye.csv), extrait :
  - 250 dialogues pour Zinedine (to_annotate_zinedine.csv)
  - 250 dialogues pour Sara    (to_annotate_sara.csv)
  - 50  dialogues en commun   (overlap_annotation.csv)

Usage:
    python etape3a_extraction_annotation.py

Auteurs : Zinedine Hamadi & Sara Hadidi
Memoire : M1 Sciences du Langage et Informatique - Sorbonne Universite 2025/2026
"""

import pandas as pd
import numpy as np
import os

SEED            = 42
N_OVERLAP       = 50
N_PER_ANNOTATOR = 250
INPUT_FILE      = "corpus_edu_nettoye.csv"

np.random.seed(SEED)

# Chargement
print(f"Chargement de {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)
print(f"  -> {len(df):,} lignes chargees")
print(f"  -> Colonnes : {list(df.columns)}")

# Melanger aleatoirement
df_shuffled = df.sample(frac=1, random_state=SEED).reset_index(drop=True)

# Overlap : 50 premiers dialogues communs aux deux annotateurs
overlap = df_shuffled.iloc[:N_OVERLAP].copy()

# 200 dialogues supplementaires pour chaque annotateur
zinedine_unique = df_shuffled.iloc[N_OVERLAP : N_OVERLAP + 200].copy()
sara_unique     = df_shuffled.iloc[N_OVERLAP + 200 : N_OVERLAP + 400].copy()

# Fichiers complets (overlap + unique)
df_zinedine = pd.concat([overlap, zinedine_unique], ignore_index=True)
df_sara     = pd.concat([overlap, sara_unique],     ignore_index=True)

# Ajouter les colonnes d'annotation vides
for df_out in [df_zinedine, df_sara, overlap]:
    df_out["edu_emotion"]   = ""
    df_out["metacog_label"] = ""
    df_out["notes"]         = ""

df_zinedine["annotator"] = "Zinedine Hamadi"
df_sara["annotator"]     = "Sara Hadidi"
overlap["annotator"]     = "overlap"

# Sauvegarde
df_zinedine.to_csv("to_annotate_zinedine.csv", index=False, encoding="utf-8")
df_sara.to_csv(    "to_annotate_sara.csv",     index=False, encoding="utf-8")
overlap.to_csv(    "overlap_annotation.csv",   index=False, encoding="utf-8")

print(f"\nFichiers generes :")
print(f"  to_annotate_zinedine.csv  - {len(df_zinedine)} dialogues (dont {N_OVERLAP} overlap)")
print(f"  to_annotate_sara.csv      - {len(df_sara)} dialogues (dont {N_OVERLAP} overlap)")
print(f"  overlap_annotation.csv    - {len(overlap)} dialogues communs")
print(f"\nProchaine etape : annoter les fichiers, puis lancer etape3b_accord_interannotateurs.py")
