from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os 
import torch

class ModerationModel():
    def __init__(self):
        exist = os.path.exists("~/.cache/huggingface/models--KoalaAI--Text-Moderation")
        self.tokenizer = AutoTokenizer.from_pretrained("KoalaAI/Text-Moderation", local_files_only=exist, padding=True)
        self.model = AutoModelForSequenceClassification.from_pretrained("KoalaAI/Text-Moderation", local_files_only=exist)

    def pred_logit(self, inputs):
        tokenizedInputs = self.tokenizer(inputs, padding="max_length", truncation=True, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**tokenizedInputs).logits
            return logits
        
    def pred_classes(self, inputs):
        logits = self.pred_logit(inputs)
        predicted_class_id = logits.argmax(dim=1)
        pred_class = [self.model.config.id2label[idx.item()] for idx in predicted_class_id]
        return pred_class

    

def get_n_params(model):
    pp=0
    for p in list(model.parameters()):
        nn=1
        for s in list(p.size()):
            nn = nn*s
        pp += nn
    return pp

if __name__ == "__main__":
    model = AutoModelForSequenceClassification.from_pretrained("KoalaAI/Text-Moderation")
    print(get_n_params(model))
    # query = "how are you doing are you doing fine?"
    # model = ModerationModel()
    # print(model.pred_classes([query]))
