import torch
from torch import nn

class Model(nn.Module):
    def __init__(self, inchannel, output_size):
        super().__init__()
        self.conv1 = nn.Conv2d(inchannel,32,3)
        self.conv1_bn = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32,64,3)
        self.conv2_bn = nn.BatchNorm2d(64)
        self.max_pool = nn.MaxPool2d(2)
        self.relu = nn.ReLU()
        self.linear = nn.Linear(64*6*6, output_size)
        self.softmax = nn.Softmax(dim=-1)
    
    def forward(self, x):
        x = self.relu(self.conv1(x))
        # print(x.size())
        x = self.conv1_bn(x)
        x = self.max_pool(x)
        x = self.relu(self.conv2(x))
        x = self.conv2_bn(x)
        x = self.max_pool(x)
        x = torch.flatten(x, start_dim=1)
        x = self.linear(x)
        x = self.softmax(x)

        return x