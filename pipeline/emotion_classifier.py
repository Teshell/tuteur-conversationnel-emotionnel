from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

LABELS    = ["stress", "frustration", "engagement", "confusion", "satisfaction", "neutre"]
THRESHOLD = 0.5

class EmotionClassifier:
    def __init__(self, model_path="emobert_v1/"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model     = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.device    = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    def predict(self, text: str) -> dict:
        if not text or not text.strip():
            return {"label": "neutre", "confidence": 0.0, "all_scores": {l: 0.0 for l in LABELS}}
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=128, padding=True).to(self.device)
        with torch.no_grad():
            probs = F.softmax(self.model(**inputs).logits, dim=-1).squeeze()
        confidence = probs.max().item()
        label = LABELS[probs.argmax().item()] if confidence >= THRESHOLD else "neutre"
        return {"label": label, "confidence": round(confidence, 3),
                "all_scores": {l: round(p.item(), 3) for l, p in zip(LABELS, probs)}}