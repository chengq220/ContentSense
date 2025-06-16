import torch

def load(path, model, optimizer):
    checkpoint = torch.load(path, map_location=torch.device('cpu'))
    if(model):
        model.load_state_dict(checkpoint['model'])
    if(optimizer):
        optimizer.load_state_dict(checkpoint['optimizer'])
    epoch = checkpoint['epoch']
    return epoch

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