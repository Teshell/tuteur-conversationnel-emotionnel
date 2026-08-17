import yaml
with open("strategies.yaml", "r", encoding="utf-8") as f:
    STRATEGIES = yaml.safe_load(f)

SYSTEM_BASE = """Tu es un tuteur pédagogique intelligent spécialisé en informatique et sciences du langage.
Tu t'exprimes toujours en français, de manière claire et bienveillante.
{emotional_instruction}
Contexte émotionnel détecté : {emotion} (confiance : {confidence:.0%})
"""

def build_prompt(emotion: str, confidence: float) -> str:
    instruction = STRATEGIES.get(emotion, STRATEGIES["neutre"])["instruction"]
    return SYSTEM_BASE.format(emotional_instruction=instruction, emotion=emotion, confidence=confidence)