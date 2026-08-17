"""
Etape 3b - Calcul de l'accord inter-annotateurs (Cohen's kappa)
================================================================
Compare les annotations de Zinedine et Sara sur le fichier overlap
et calcule le Cohen's kappa pour les deux dimensions :
  - edu_emotion   (stress, frustration, engagement, confusion, satisfaction, neutre, autre)
  - metacog_label (planification, monitoring, auto-eval, aucun)

Usage:
    python etape3b_accord_interannotateurs.py

Fichiers attendus dans le repertoire courant :
    overlap_zinedine.csv  -- 50 lignes annotees par Zinedine
    overlap_sara.csv      -- 50 lignes annotees par Sara

Auteurs : Zinedine Hamadi & Sara Hadidi
Memoire : M1 Sciences du Langage et Informatique - Sorbonne Universite 2025/2026
"""

import pandas as pd
from sklearn.metrics import cohen_kappa_score
from collections import Counter

FILE_ZINEDINE = "overlap_zinedine.csv"
FILE_SARA     = "overlap_sara.csv"

# Chargement
print("Chargement des fichiers overlap...")
df_z = pd.read_csv(FILE_ZINEDINE)
df_s = pd.read_csv(FILE_SARA)
print(f"  Zinedine : {len(df_z)} lignes")
print(f"  Sara     : {len(df_s)} lignes")
assert len(df_z) == len(df_s), "Les deux fichiers n'ont pas le meme nombre de lignes !"

# Nettoyage
def clean(series, default):
    cleaned = series.fillna(default).str.lower().str.strip()
    corrections = {
        "confision": "confusion",
        "neuret":    "neutre",
        "neurtre":   "neutre",
        "auto-eval ": "auto-eval",
        "aucun ":    "aucun",
    }
    return cleaned.replace(corrections)

df_z["edu_emotion"]   = clean(df_z["edu_emotion"],   "neutre")
df_z["metacog_label"] = clean(df_z["metacog_label"], "aucun")
df_s["edu_emotion"]   = clean(df_s["edu_emotion"],   "neutre")
df_s["metacog_label"] = clean(df_s["metacog_label"], "aucun")

# Calcul du Cohen's kappa
print("\n" + "=" * 55)
print("ACCORD INTER-ANNOTATEURS -- Cohen's kappa")
print("=" * 55)

labels_emo  = sorted(set(df_z["edu_emotion"])  | set(df_s["edu_emotion"]))
labels_meta = sorted(set(df_z["metacog_label"])| set(df_s["metacog_label"]))

k_emo  = cohen_kappa_score(df_z["edu_emotion"],   df_s["edu_emotion"],   labels=labels_emo)
k_meta = cohen_kappa_score(df_z["metacog_label"], df_s["metacog_label"], labels=labels_meta)

pct_emo  = (df_z["edu_emotion"]   == df_s["edu_emotion"]).mean()   * 100
pct_meta = (df_z["metacog_label"] == df_s["metacog_label"]).mean() * 100

def interpret(k):
    if k >= 0.80: return "Excellent"
    if k >= 0.60: return "Substantiel"
    if k >= 0.40: return "Modere"
    return "Faible -- reviser le guide et recalibrer"

print(f"\n  edu_emotion   : kappa={k_emo:.3f} | accord={pct_emo:.1f}% | {interpret(k_emo)}")
print(f"  metacog_label : kappa={k_meta:.3f} | accord={pct_meta:.1f}% | {interpret(k_meta)}")

# Desaccords edu_emotion
print("\n" + "=" * 55)
print("DESACCORDS edu_emotion")
print("=" * 55)
desaccords_emo = [
    (z, s) for z, s in zip(df_z["edu_emotion"], df_s["edu_emotion"]) if z != s
]
print(f"\n  Total : {len(desaccords_emo)}/50\n")
for (a, b), n in Counter(desaccords_emo).most_common(10):
    print(f"  Zinedine='{a}' vs Sara='{b}' : {n}x")

# Desaccords metacog_label
print("\n" + "=" * 55)
print("DESACCORDS metacog_label")
print("=" * 55)
desaccords_meta = [
    (z, s) for z, s in zip(df_z["metacog_label"], df_s["metacog_label"]) if z != s
]
print(f"\n  Total : {len(desaccords_meta)}/50\n")
for (a, b), n in Counter(desaccords_meta).most_common(10):
    print(f"  Zinedine='{a}' vs Sara='{b}' : {n}x")

# Rapport
rapport_lines = [
    "RAPPORT D'ACCORD INTER-ANNOTATEURS",
    "====================================",
    "Memoire M1 -- Zinedine Hamadi & Sara Hadidi -- Sorbonne Universite 2025/2026",
    "",
    f"edu_emotion   : kappa={k_emo:.3f} | accord={pct_emo:.1f}% | {interpret(k_emo)}",
    f"metacog_label : kappa={k_meta:.3f} | accord={pct_meta:.1f}% | {interpret(k_meta)}",
    "",
    f"Desaccords edu_emotion   : {len(desaccords_emo)}/50",
    f"Desaccords metacog_label : {len(desaccords_meta)}/50",
]
with open("rapport_accord.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(rapport_lines))

print("\nrapport_accord.txt sauvegarde")

if k_emo >= 0.60 and k_meta >= 0.60:
    print("\nCorpus VALIDE -- vous pouvez passer a l'etape 4")
else:
    print("\nCorpus NON VALIDE -- revisez le guide et recommencez sur 30 dialogues")
