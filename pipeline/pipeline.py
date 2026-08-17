from emotion_classifier import EmotionClassifier
from prompt_builder import build_prompt
from llm_client import generate
import json, datetime, os

class DialogueHistory:
    def __init__(self, max_turns=5):
        self.history = []; self.max_turns = max_turns
    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-self.max_turns * 2:]
    def get(self): return self.history.copy()
    def reset(self): self.history = []

class EmotionalTutor:
    def __init__(self):
        self.classifier = EmotionClassifier()
        self.history    = DialogueHistory()
        self.logs       = []

    def respond(self, user_message: str) -> dict:
        er      = self.classifier.predict(user_message)
        prompt  = build_prompt(er["label"], er["confidence"])
        resp    = generate(prompt, user_message, self.history.get())
        self.history.add("user", user_message)
        self.history.add("assistant", resp)
        entry = {"timestamp": datetime.datetime.now().isoformat(),
                 "user_message": user_message, "emotion": er["label"],
                 "confidence": er["confidence"], "all_scores": er["all_scores"],
                 "llm_response": resp}
        os.makedirs("logs", exist_ok=True)
        with open("logs/dialogues.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        self.logs.append(entry)
        return {"response": resp, "emotion": er["label"], "confidence": er["confidence"]}

if __name__ == "__main__":
    tutor = EmotionalTutor()
    print("=== Tuteur Conversationnel Émotionnel ===")
    while True:
        msg = input("Apprenant : ").strip()
        if msg.lower() == "quit": break
        r = tutor.respond(msg)
        print(f"[{r['emotion']} {r['confidence']:.0%}] Tuteur : {r['response']}\n")