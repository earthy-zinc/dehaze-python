import os

import torch
import torchvision.transforms as tfs
import torchvision.utils as torch_utils
from PIL import Image

from .models.AECRNet import Dehaze
from global_variable import MODEL_PATH, DEVICE, DEVICE_ID


def get_model(model_path: str):
    net = Dehaze(3, 3)
    net = net.to(DEVICE)
    net = torch.nn.DataParallel(net, device_ids=DEVICE_ID)
    ckp = torch.load(model_path)
    net.load_state_dict(ckp['model'])
    net.eval()
    return net


# TODO DCNv2 可变形卷积缺失 问题无法运行
def dehaze(haze_image_path: str, output_image_path: str, model_path: str):
    net = get_model(model_path)
    haze = Image.open(haze_image_path).convert('RGB')
    haze = tfs.ToTensor()(haze)[None, ::]
    haze = haze.to(DEVICE)
    with torch.no_grad():
        pred, _, _, _ = net(haze)
    ts = torch.squeeze(pred.clamp(0, 1).cpu())
    torch_utils.save_image(ts, output_image_path)
