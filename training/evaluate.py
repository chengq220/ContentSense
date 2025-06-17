import torch
import torch.nn as nn
from models.CNN import CNN
from models.KoalaAIDeberta import ModerationModel
from dataset import get_dataloader
from tqdm import tqdm
from utils import load
from config import N_CLASSES, DEVICE, BATCH, MODEL
import time 
from sklearn.metrics import f1_score

def evaluate(path):
    testLoader, vocab_size = get_dataloader(batch=BATCH, isTrain=False)
    if(MODEL == "CNN"):
        model = CNN(vocab_size=vocab_size, n_classes=N_CLASSES).to(DEVICE)
        _ = load(path, model=model, optimizer=None)
        model.eval()
    elif(MODEL == "KoalaAI"):
        model = ModerationModel()
    else:
        raise Exception("Model not recognized")
    total_samples = 0
    num_correct = 0
    f1 = 0
    start = time.time()
    with torch.no_grad():
        for idx, (feature, label, teacher_logit, query) in enumerate(tqdm(testLoader)):
            total_samples += feature.shape[0]

            feature = feature.to(DEVICE)
            label = label.to(DEVICE)
            label_correct_class = torch.argmax(label, dim=1)

            if(MODEL == "CNN"):
                logit = model(feature)
            elif(MODEL == "KoalaAI"):
                logit = model.pred_logit(query)
            else:
                raise Exception("Model not recognized")
            
            softmax_logit = nn.functional.softmax(logit, dim=1)
            model_pred_class = torch.argmax(softmax_logit, dim=1)

            f1 += f1_score(label_correct_class, model_pred_class, average='weighted')

            batch_correct = torch.sum(label_correct_class == model_pred_class)
            num_correct += batch_correct.item()

        end = time.time()
        timeTaken = end - start

    return float(num_correct)/total_samples, float(f1)/len(testLoader), timeTaken, total_samples


if __name__ == "__main__":
    acc, f1, timeTaken, sampleSize = evaluate("training/weights/latest.pth")
    print("Accuracy: ", acc)
    print("F1: ", f1)
    print("Time taken: ", timeTaken)
    print("# Samples: ", sampleSize)
