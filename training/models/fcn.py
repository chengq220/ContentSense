import torch
import torch.nn as tnn
import torch.nn.functional as F 

def fc_layer(size_in, size_out):
    layer = tnn.Sequential(
        tnn.Linear(size_in, size_out),
        tnn.BatchNorm1d(size_out),
        tnn.ReLU()
    )
    return layer

class FCN(tnn.Module):
    def __init__(self, n_classes=7):
        super(FCN, self).__init__()

        self.layer1 = fc_layer(42, 128) 
        self.layer2 = fc_layer(128, 256) 
        self.layer3 = fc_layer(256, 1024) 
        self.layer4 = fc_layer(1024, 2048) 
        self.layer5 = fc_layer(2048, 2048) 
        self.layer6 = tnn.Linear(2048, n_classes)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)
        logit = self.layer6(out)
        return logit

if __name__ == "__main__":
    txt = torch.rand((40,42))
    fcn = FCN(n_classes=11)
    classfication = fcn(txt)
    print(classfication.shape)