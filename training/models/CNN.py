import torch
import torch.nn as tnn
from config import N_CLASSES, TOKEN_MAX_LENGTH

def conv_layer(channel_in, channel_out):
    layer = tnn.Sequential(
        tnn.Conv1d(channel_in, channel_out, kernel_size=3, padding="same"),
        tnn.BatchNorm1d(channel_out),
        tnn.ReLU(),
        tnn.Dropout(p=0.4)
    )
    return layer

def fc_layer(size_in, size_out):
    layer = tnn.Sequential(
        tnn.Linear(size_in, size_out),
        tnn.BatchNorm1d(size_out),
        tnn.ReLU()
    )
    return layer

class CNN(tnn.Module):
    def __init__(self, embedding_size = 36, kernel_size = 2, stride = 2):
        super(CNN, self).__init__()
        self.pooling = tnn.MaxPool1d(kernel_size=kernel_size, stride=stride)
        self.embedding = tnn.Embedding(TOKEN_MAX_LENGTH, embedding_size) 
        
        self.conv1 = conv_layer(embedding_size, 64) 
        self.conv2 = conv_layer(64, 128) 
        self.conv3 = conv_layer(128, 256) 
        self.conv4 = conv_layer(256, 256)
        
        self.fc1 = fc_layer(256 * 16, 2048) 
        self.fc2 = fc_layer(2048, 2048) 
        self.fc3 = tnn.Linear(2048, N_CLASSES)

    def forward(self, x):
        embed = self.embedding(x).permute(0,2,1) # b x 36 x 64 
        
        out = self.conv1(embed) # b x 64 x 64
        out = self.conv2(out) # b x 128 x 64
        out = self.pooling(out) #b x 128 x 32
       
        out = self.conv3(out) #b x 256 x 32
        out = self.conv4(out) # b x 256 x  32
        out = self.pooling(out) # b x 256 x 16
        
        flat = out.reshape((out.shape[0], -1)) # b x 256 * 16
        
        out = self.fc1(flat) # b x 2048
        out = self.fc2(out) # b x 2048
        logit = self.fc3(out) # b x num_classes
        return logit

if __name__ == "__main__":
    txt = torch.rand((40,64)).long()
    fcn = CNN(n_classes=11)
    classfication = fcn(txt)
    print(classfication.shape)