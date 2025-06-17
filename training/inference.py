from models.CNN import CNN
from config import *
from transformers import AutoTokenizer
import torch
import torch.nn as nn
from utils import load, get_classes_from_idx
import time

def inference(query):
    tokenizer = AutoTokenizer.from_pretrained("KoalaAI/Text-Moderation")
    tokenized_query = tokenizer(query, padding="max_length", truncation=True, return_tensors="pt")
    token_idx = tokenized_query["input_ids"]
    model = CNN(vocab_size=tokenizer.vocab_size, n_classes=N_CLASSES)
    _ = load(f"{SAVE_DIR}/latest.pth", model=model, optimizer=None)
    
    model.eval()
    with torch.no_grad():
        logit = model(token_idx)
        softmax_logit = nn.functional.softmax(logit, dim=1)
        pred_class = torch.argmax(softmax_logit, dim=1)
        pred_class = get_classes_from_idx([pred_class.item()])
        return pred_class


if __name__ == "__main__":
    query = ["how are you doing? Wanna kill yourself?"]
    start = time.time()
    output = inference(query=query)
    end = time.time()
    print(end-start)
