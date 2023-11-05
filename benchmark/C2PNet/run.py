import torch
from PIL import Image
import torchvision.transforms as tfs
import torchvision.utils as torch_utils

from benchmark.C2PNet.C2PNet import C2PNet
import os

from benchmark.C2PNet.metrics import psnr, ssim

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
# 获取当前脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))


def get_model(model_name: str):
    # 构造模型文件的绝对路径
    model_dir = os.path.join(script_dir, model_name)

    net = C2PNet(gps=3, blocks=19)
    ckp = torch.load(model_dir)
    net = net.to(device)
    net.load_state_dict(ckp['model'])
    net.eval()
    return net


def dehaze(haze_image_path: str, output_image_path: str):
    net = get_model('OTS.pkl')
    haze = Image.open(haze_image_path).convert('RGB')
    haze = tfs.ToTensor()(haze)[None, ::]
    haze = haze.to(device)
    with torch.no_grad():
        pred = net(haze)
    ts = torch.squeeze(pred.clamp(0, 1).cpu())
    torch_utils.save_image(ts, output_image_path)


def calculate(haze_image_path: str, clear_image_path: str):
    haze = Image.open(haze_image_path).convert('RGB')
    clear = Image.open(clear_image_path).convert('RGB')
    haze = tfs.ToTensor()(haze)[None, ::]
    clear = tfs.ToTensor()(clear)[None, ::]
    return psnr(haze, clear), ssim(haze, clear)
