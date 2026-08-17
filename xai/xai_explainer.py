from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import yaml

LABELS    = ["stress", "frustration", "engagement", "confusion", "satisfaction", "neutre"]
THRESHOLD = 0.5

class XAIExplainer:
    def __init__(self, model_path, templates_path="xai_templates.yaml"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model     = AutoModelForSequenceClassification.from_pretrained(
            model_path, output_attentions=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        with open(templates_path, "r", encoding="utf-8") as f:
            self.templates = yaml.safe_load(f)

    def explain(self, text: str) -> dict:
        inputs = self.tokenizer(text, return_tensors="pt",
            truncation=True, max_length=128, padding=True).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        probs      = F.softmax(outputs.logits, dim=-1).squeeze()
        confidence = probs.max().item()
        label      = LABELS[probs.argmax().item()] if confidence >= THRESHOLD else "neutre"
        attn       = outputs.attentions[-1].mean(dim=1).squeeze().mean(dim=0).cpu().numpy()
        token_ids  = inputs["input_ids"].squeeze().cpu().numpy()
        tokens     = self.tokenizer.convert_ids_to_tokens(token_ids)
        filtered   = [(t.replace("Ġ","").strip(), float(s))
                      for t, s in zip(tokens, attn)
                      if t not in ["<s>","</s>","<pad>"] and len(t.replace("Ġ","")) > 2]
        top        = sorted(filtered, key=lambda x: x[1], reverse=True)[:3]
        top_str    = ", ".join([f'"{t}"' for t, _ in top])
        template   = self.templates[label]["template"]
        explanation = template.replace("{top_tokens}", top_str)
        return {"label": label, "confidence": round(confidence, 3),
                "top_tokens": top, "explanation": explanation}