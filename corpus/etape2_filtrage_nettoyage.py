"""
Etape 2 - Filtrage et nettoyage du corpus
==========================================
Filtre les dialogues a contexte educatif via une liste de mots-cles thematiques
et applique un nettoyage basique (doublons, longueur minimale).

Usage:
    python etape2_filtrage_nettoyage.py

Fichier attendu : corpus_brut.csv (produit par etape1)
Fichier produit : corpus_edu_nettoye.csv

Auteurs : Zinedine Hamadi & Sara Hadidi
Memoire : M1 Sciences du Langage et Informatique - Sorbonne Universite 2025/2026
"""

import pandas as pd
import re

INPUT_FILE  = "corpus_brut.csv"
OUTPUT_FILE = "corpus_edu_nettoye.csv"
MIN_WORDS   = 4

# 60 mots-cles educatifs repartis en 4 groupes
KEYWORDS = {
    "apprentissage": [
        "learn", "understand", "study", "exercise", "lesson", "course",
        "homework", "practice", "revise", "concept", "explain", "definition",
        "example", "lecture", "tutorial", "assignment",
    ],
    "difficulte": [
        "confus", "stuck", "help me", "explain", "don't get", "how do i",
        "i'm lost", "make sense", "clarify", "difficult", "hard", "struggling",
        "not sure", "don't understand", "wrong", "mistake", "error",
    ],
    "acteurs_educatifs": [
        "teacher", "professor", "tutor", "student", "class", "exam",
        "test", "grade", "score", "quiz", "lecture", "school", "university",
        "college", "homework", "assignment",
    ],
    "metacognition": [
        "think about", "i realize", "step by step", "my goal", "i checked",
        "i need to", "i was wrong", "i understand now", "let me try",
        "i should", "i think", "planning", "reviewing", "checking",
        "strategy", "approach",
    ],
}

ALL_KEYWORDS = [kw for group in KEYWORDS.values() for kw in group]


def has_educational_keyword(text):
    if not isinstance(text, str):
        return False
    text_lower = text.lower()
    return any(kw in text_lower for kw in ALL_KEYWORDS)


def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"\s+", " ", text).strip()
    return text


print(f"Chargement de {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)
print(f"  -> {len(df):,} paires chargees")

# Nettoyage du texte
df["utterance"] = df["utterance"].apply(clean_text)
df["context"]   = df["context"].apply(clean_text)

# Suppression des utterances trop courtes
df = df[df["utterance"].str.split().str.len() >= MIN_WORDS]
print(f"  -> {len(df):,} apres filtre longueur minimale ({MIN_WORDS} mots)")

# Filtrage educatif : au moins un keyword dans utterance OU context
mask = df["utterance"].apply(has_educational_keyword) | df["context"].apply(has_educational_keyword)
df_edu = df[mask].copy()
print(f"  -> {len(df_edu):,} apres filtrage educatif ({len(df_edu)/len(df)*100:.1f}%)")

# Suppression des doublons
df_edu = df_edu.drop_duplicates(subset=["utterance"]).reset_index(drop=True)
print(f"  -> {len(df_edu):,} apres suppression des doublons")

# Ajouter colonne mots-cles detectes
def matched_keywords(text):
    if not isinstance(text, str):
        return ""
    text_lower = text.lower()
    return ", ".join([kw for kw in ALL_KEYWORDS if kw in text_lower])[:200]

df_edu["matched_kw"] = df_edu["utterance"].apply(matched_keywords)

# Sauvegarde
df_edu.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print(f"\nFichier sauvegarde : {OUTPUT_FILE}")
print(f"Distribution par source :")
print(df_edu["source"].value_counts().to_string())
print(f"\nTop emotions :")
print(df_edu["emotion"].value_counts().head(10).to_string())
