import torch
import torch.nn as nn
from models.CNN import CNN
from dataset import get_dataloader
from tqdm import tqdm
from utils import load
from config import N_CLASSES, DEVICE, BATCH

def evaluate(path):
    testLoader, vocab_size = get_dataloader(batch=BATCH, isTrain=False)

    model = CNN(vocab_size=vocab_size, n_classes=N_CLASSES).to(DEVICE)
    _ = load(path, model=model, optimizer=None)

    model.eval()
    total_samples = 0
    num_correct = 0
    
    for idx, (feature, label, teacher_logit) in enumerate(tqdm(testLoader)):
        total_samples += feature.shape[0]

        feature = feature.to(DEVICE)
        label = label.to(DEVICE)
        label_correct_class = torch.argmax(label, dim=1)

        logit = model(feature)
        softmax_logit = nn.functional.softmax(logit, dim=1)
        model_pred_class = torch.argmax(softmax_logit, dim=1)

        batch_correct = torch.sum(label_correct_class == model_pred_class)
        num_correct += batch_correct.item()

    return float(num_correct)/total_samples
