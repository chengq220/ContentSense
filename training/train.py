import torch
import torch.nn as nn
from models.FCN import FCN
from models.KoalaAIDeberta import ModerationModel
from dataset import get_dataloader
import torch.optim as optim
import wandb
import tqdm 

def train(learning_rate = 0.0001, batch = 16, epochs = 100, DEVICE = "cuda:0", beta = 0.5, T = 2):
    student = FCN(n_classes=8).to(DEVICE)
    teacher = ModerationModel()
    
    student.train()

    trainLoader = get_dataloader(batch=batch)
    CSE = nn.CrossEntropyLoss().to(DEVICE) # Already contains softmax in the criterion

    optimizer = optim.Adam(student.parameters(), lr=learning_rate)


    for epoch in range(epochs):
        running_loss = 0.0
        for idx, (feature, label, query) in tqdm(trainLoader):
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
            
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss / len(trainLoader)}")


if __name__ == "__main__":
