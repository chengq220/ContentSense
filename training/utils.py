import torch

def load(path, model, optimizer):
    checkpoint = torch.load(path)
    if(model):
        model.load_state_dict(checkpoint['model'])
    if(optimizer):
        optimizer.load_state_dict(checkpoint['optimizer'])
    epoch = checkpoint['epoch']
    return epoch

def save(path, epoch, model, optimizer):
    checkpoint = { 
        'epoch': epoch,
        'model': model.state_dict(),
        'optimizer': optimizer.state_dict()
    }
    torch.save(checkpoint, path)
