import torch
import torch.nn as nn
from PIL import Image
import numpy as np
from io import BytesIO

import vessl


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv = nn.Conv2d(1, 32, 3, 1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2)
        self.drop1 = nn.Dropout2d(0.25)
        self.drop2 = nn.Dropout2d(0.5)
        self.fc1 = nn.Linear(5408, 128)
        self.fc2 = nn.Linear(128, 10)
        self.softmax = nn.LogSoftmax(1)

    def forward(self, x):
        x = self.relu(self.conv(x))
        x = self.pool(x)
        x = self.drop1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.drop2(x)
        x = self.fc2(x)
        return self.softmax(x)


class MNISTCNNRunner(vessl.RunnerBase):
    @staticmethod
    def load_model(props, artifacts):
        model = Net()
        model.load_state_dict(torch.load("model.pt"))
        model.eval()
        return model

    @staticmethod
    def preprocess_data(img_data):
        # receive byte data and change to image data
        image = Image.open(BytesIO(img_data))

        # change image data to numpy array
        pix = np.array(image)
        pix = pix / 255.0
        data = pix.reshape(-1, 28, 28)

        # change datatype to tensor by using TensorDataset
        infer_torch_data = torch.utils.data.TensorDataset(
            torch.from_numpy(data).unsqueeze(1))

        # load tensor data to dataloader iteration
        infer_dataloader = torch.utils.data.DataLoader(
            infer_torch_data, batch_size=128, shuffle=False)

        # save data from dataloader iteration, and change datatype of data in tensor to float(?)
        for data in infer_dataloader:
            infer_data = data[0].float()

        return infer_data

    @staticmethod
    def predict(model, data):
        with torch.no_grad():
            return model(data).argmax(dim=1, keepdim=True)

    @staticmethod
    def postprocess_data(data):
        return {"result": data.item()}
