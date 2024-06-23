import os

import numpy as np
import torch
import torchvision.utils
from PIL import Image
from torch.autograd import Variable

from .models import Generator
from global_variable import MODEL_PATH, DEVICE, DEVICE_ID


def get_model(model_path: str):
    net = Generator()
    net.to(DEVICE)

    net = torch.nn.DataParallel(net, device_ids=DEVICE_ID).cuda()

    model_info = torch.load(model_path)

    net.load_state_dict(model_info['state_dict'])
    net.eval()
    return net


def dehaze(haze_image_path: str, output_image_path: str, model_path: str):
    net = get_model(model_path)

    norm = lambda x: (x - 0.5) / 0.5
    denorm = lambda x: (x + 1) / 2

    haze = np.array(Image.open(haze_image_path).convert('RGB')) / 255
    with torch.no_grad():
        haze = torch.Tensor(haze.transpose(2, 0, 1)[np.newaxis, :, :, :]).cuda()
        haze = Variable(haze, requires_grad=True)
        haze = norm(haze)
        out, _ = net(haze)
        out = denorm(out)
        torchvision.utils.save_image(out, output_image_path)
