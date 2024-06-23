import os

import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image

from .model.networks import ResnetGenerator
from global_variable import MODEL_PATH, DEVICE


def get_model(model_path: str, img_size):
    params = torch.load(model_path)
    genA2B = ResnetGenerator(input_nc=3, output_nc=3, ngf=64, n_blocks=4, img_size=img_size,
                             light=True).to(DEVICE)
    genA2B.load_state_dict(params['genA2B'])
    genA2B.eval()
    return genA2B


def dehaze(haze_image_path: str, output_image_path: str, model_path: str):
    haze = Image.open(haze_image_path).convert('RGB')
    img_size = min(haze.width, haze.height)
    haze = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
    ])(haze).unsqueeze(0).to(DEVICE)
    net = get_model(model_path, img_size)
    output, _, _ = net(haze)
    torchvision.utils.save_image(output, output_image_path, normalize=True)
