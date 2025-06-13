from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os 
import torch

class ModerationModel():
    def __init__(self):
        exist = os.path.exists("~/.cache/huggingface/models--KoalaAI--Text-Moderation")
        self.tokenizer = AutoTokenizer.from_pretrained("KoalaAI/Text-Moderation", local_files_only=exist)
        self.model = AutoModelForSequenceClassification.from_pretrained("KoalaAI/Text-Moderation", local_files_only=exist)

    def pred_logit(self, inputs):
        tokenizedInputs = self.tokenizer(inputs, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**tokenizedInputs).logits
            return logits
        
    def pred_classes(self, inputs):
        logits = self.pred_logit(inputs)
        predicted_class_id = logits.argmax().item()
        pred_class = self.model.config.id2label[predicted_class_id]
        return pred_class
