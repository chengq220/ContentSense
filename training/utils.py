import torch
import torch.nn as tnn

def load(path, model, optimizer):
    checkpoint = torch.load(path)
    if(model):
        model.load_state_dict(checkpoint['model'])
    if(optimizer):
        optimizer.load_state_dict(checkpoint['optimizer'])
    epoch = checkpoint['epoch']
    return epoch

def initialize_weights(module):
    if isinstance(module, tnn.Linear):
        tnn.init.xavier_uniform_(module.weight)
    elif isinstance(module, tnn.Conv2d):
        tnn.init.kaiming_normal_(module.weight, mode='fan_in', nonlinearity='relu')

def save(path, epoch, model, optimizer):
    checkpoint = { 
        'epoch': epoch,
        'model': model.state_dict(),
        'optimizer': optimizer.state_dict()
    }
    torch.save(checkpoint, path)

def get_classes_from_idx(idx:list) -> list:
    configureTable = {
        0: "H", 
        1: "H2",
        2: "HR",
        3: "OK",
        4: "S",
        5: "S3",
        6: "SH",
        7: "V", 
        8: "V2"
    }
    output = [configureTable[iidx] for iidx in idx]
    return output