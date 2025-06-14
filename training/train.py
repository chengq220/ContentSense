import torch
import torch.nn as nn
from models.CNN import CNN
from models.KoalaAIDeberta import ModerationModel
from dataset import get_dataloader
import torch.optim as optim
import wandb
from tqdm import tqdm
from utils import save
from evaluate import evaluate
from config import * 

def train(beta = 0.5, T = 2):
    trainLoader, vocab_size = get_dataloader(batch=BATCH)
    student = CNN(vocab_size=vocab_size, n_classes=N_CLASSES).to(DEVICE)
    teacher = ModerationModel()

    if(WANDBON):
        wandb.init(
            project="ContentSense",
            config={
                "learning_rate": LR,
                "architecture": "CNN",
                "dataset": "Moderation-OpenAI",
                "epochs": EPOCHS,
                "optimzer": "Adams",
                "Loss": "CE + Distillation Loss"
            },
        )
    
    student.train()
    CSE = nn.CrossEntropyLoss().to(DEVICE) # Already contains softmax in the criterion

    optimizer = optim.Adam(student.parameters(), lr=LR)

    for epoch in range(EPOCHS):
        running_loss = 0.0
        for idx, (feature, label, query) in enumerate(tqdm(trainLoader)):
            x = feature.to(DEVICE)
            y = label.to(DEVICE)

            teacher_logit = teacher.pred_logit(query).to(DEVICE)

            optimizer.zero_grad()
            student_logit = student(x)

            soft_targets = nn.functional.softmax(teacher_logit / T, dim=-1)
            soft_prob = nn.functional.log_softmax(student_logit / T, dim=-1)

            teacher_student_loss = torch.sum(soft_targets * (soft_targets.log() - soft_prob)) / soft_prob.size()[0] * (T**2)
            gt_difference_loss = CSE(student_logit, y)

            loss = (1-beta) * teacher_student_loss + (beta) * gt_difference_loss
            
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            
        if(epoch % 10 == 0):
            save(path=f"{SAVE_DIR}/{epoch}.pth", epoch = epoch, model = student, optimizer= optimizer)
        save(path=f"{SAVE_DIR}/latest.pth", epoch = epoch, model = student, optimizer= optimizer)
        
        epoch_loss = running_loss / len(trainLoader)
        accuracy = evaluate(path=f"{SAVE_DIR}/latest.pth")

        if(WANDBON):
            wandb.log({"Training Loss": epoch_loss})
            wandb.log({"Test Accuracy": accuracy})

if __name__ == "__main__":
    train()