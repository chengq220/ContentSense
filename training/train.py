import torch
import torch.nn as nn
from models.CNN import CNN
from models.KoalaAIDeberta import ModerationModel
from dataset import get_dataloader
import torch.optim as optim
import wandb
from tqdm import tqdm
from utils import save, initialize_weights
from evaluate import evaluate
from config import * 

def train(beta = 0.5, T = 2):
    trainLoader, vocab_size = get_dataloader(batch=BATCH)
    student = CNN(vocab_size=vocab_size, n_classes=N_CLASSES).to(DEVICE)
    student.apply(initialize_weights)

    if(WANDBON):
        wandb.init(
            project="ContentSense",
            config={
                "learning_rate": LR,
                "architecture": "CNN",
                "dataset": "Moderation-OpenAI",
                "epochs": EPOCHS,
                "optimzer": "Adams",
                "Loss": "CE + Distillation Loss",
                "initialization": "He + Xavier",
                "kernel_size": "4 + stride 4"
            },
        )
    
    student.train()
    CE = nn.CrossEntropyLoss().to(DEVICE) # Already contains softmax in the criterion

    optimizer = optim.Adam(student.parameters(), lr=LR)

    for epoch in range(EPOCHS):
        running_loss = 0.0
        for idx, (feature, label, teacher_logit, query) in enumerate(tqdm(trainLoader)):
            x = feature.to(DEVICE)
            y = label.to(DEVICE)
            teacher_logit = teacher_logit.to(DEVICE)

            optimizer.zero_grad()
            student_logit = student(x)

            soft_targets = nn.functional.softmax(teacher_logit / T, dim=-1)
            soft_prob = nn.functional.log_softmax(student_logit / T, dim=-1)

            teacher_student_loss = torch.sum(soft_targets * (soft_targets.log() - soft_prob)) / soft_prob.size()[0] * (T**2)
            gt_difference_loss = CE(student_logit, y)

            loss = (1-beta) * teacher_student_loss + (beta) * gt_difference_loss
            
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            
        if(epoch % 10 == 0):
            save(path=f"{SAVE_DIR}/{epoch}.pth", epoch = epoch, model = student, optimizer= optimizer)
        save(path=f"{SAVE_DIR}/latest.pth", epoch = epoch, model = student, optimizer= optimizer)
        
        epoch_loss = running_loss / len(trainLoader)
        acc, f1, _, _ = evaluate(path=f"{SAVE_DIR}/latest.pth")

        if(WANDBON):
            wandb.log({"Training Loss": epoch_loss})
            wandb.log({"Accuracy": acc})
            wandb.log({"F1-score": f1})

if __name__ == "__main__":
    train()