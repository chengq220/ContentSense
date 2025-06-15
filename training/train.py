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

def train(learning_rate = 0.0001, batch = 16, epochs = 100, n_classes = 9, DEVICE = "cpu", beta = 0.5, T = 2, enableWandb = False):
    student = CNN(n_classes=n_classes).to(DEVICE)
    teacher = ModerationModel()

    if(enableWandb):
        wandb.init(project="ContentModeration")
        wandb.watch(student, log='all')
    
    student.train()

    trainLoader = get_dataloader(batch=batch)
    CSE = nn.CrossEntropyLoss().to(DEVICE) # Already contains softmax in the criterion

    optimizer = optim.Adam(student.parameters(), lr=learning_rate)

    for epoch in range(epochs):
        running_loss = 0.0
        for idx, (feature, label, query) in enumerate(tqdm(trainLoader)):
            x_cuda = feature.to(DEVICE)
            y_cuda = label.to(DEVICE)

            teacher_logit = teacher.pred_logit(query)

            optimizer.zero_grad()
            student_logit = student(x_cuda)

            soft_targets = nn.functional.softmax(teacher_logit / T, dim=-1)
            soft_prob = nn.functional.log_softmax(student_logit / T, dim=-1)

            teacher_student_loss = torch.sum(soft_targets * (soft_targets.log() - soft_prob)) / soft_prob.size()[0] * (T**2)
            gt_difference_loss = CSE(student_logit, y_cuda)

            loss = (1-beta) * teacher_student_loss + (beta) * gt_difference_loss
            print(loss)
            exit()
            
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
        
        epoch_loss = running_loss / len(trainLoader)
        accuracy = evaluate(path="weights/latest.pth", n_classes= n_classes, DEVICE=DEVICE)

        if(enableWandb):
            wandb.log({"Training Loss": epoch_loss})
            wandb.log({"Test Accuracy": accuracy})

        if(epoch % 10 == 0):
            save(path=f"weights/{epoch}.pth", epoch = epoch, model = student, optimizer= optimizer)
        save(path=f"weights/latest.pth", epoch = epoch, model = student, optimizer= optimizer)

if __name__ == "__main__":
    train(DEVICE="cuda:0")