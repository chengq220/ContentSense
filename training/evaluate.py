import torch
import torch.nn as nn
from models.CNN import CNN
from dataset import get_dataloader
from tqdm import tqdm
from utils import load

def evaluate(path, n_classes = 9, batch = 16, DEVICE = "cpu"):
    model = CNN(n_classes=n_classes).to(DEVICE)
    _ = load(path, model=model, optimizer=None)
    
    testLoader = get_dataloader(batch=batch, isTrain=False)

    model.eval()
    total_samples = 0
    num_correct = 0
    
    for idx, (feature, label, _) in enumerate(tqdm(testLoader)):
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
