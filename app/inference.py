from app.models.CNN import CNN
import torch
import torch.nn as nn
from app.utils import get_classes_from_idx

def inference(query, model, tokenizer):
    tokenized_query = tokenizer(query, padding="max_length", truncation=True, return_tensors="pt")
    token_idx = tokenized_query["input_ids"]
    
    model.eval()
    with torch.no_grad():
        logit = model(token_idx)
        softmax_logit = nn.functional.softmax(logit, dim=1)
        pred_class = torch.argmax(softmax_logit, dim=1)
        pred_class = get_classes_from_idx(pred_class.numpy().tolist())
        return pred_class


if __name__ == "__main__":
    query = ["how are you doing? Wanna kill yourself?", "how about going out for dinner tonight"]
    output = inference(query=query)
    print(output)
