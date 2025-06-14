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

def get_classes_from_idx(idx:list) -> list:
    configureTable = {
        0: "S", 
        1: "H",
        2: "V",
        3: "HR",
        4: "SH",
        5: "S3",
        6: "H2",
        7: "V2", 
        8: "OK"
    }
    output = [configureTable[iidx] for iidx in idx]
    return output