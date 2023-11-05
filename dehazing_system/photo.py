import json
import os.path
import uuid

from django.http import HttpResponse, HttpRequest
from benchmark.C2PNet.run import dehaze, calculate

# 获取当前脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))


def uploadImage(request: HttpRequest):
    image_name = str(uuid.uuid4()) + ".png"
    image_path = os.path.join(script_dir, "../data/" + image_name)
    image = request.body
    # 保存前端传来的图片
    with open(image_path, "wb") as destination:
        destination.write(image)
    return HttpResponse(image_name)


def downloadImage(request: HttpRequest, image_name: str):
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/" + image_name)
    with open(image_path, "rb") as destination:
        return HttpResponse(destination.read(), content_type="image/png")


def dehazeImage(request: HttpRequest):
    haze_image_name = request.POST["haze_image"]
    if isinstance(haze_image_name, str):
        output_image_name = str(uuid.uuid4()) + ".png"
        haze_image_path = os.path.join(script_dir, "../data/" + haze_image_name)
        output_image_path = os.path.join(script_dir, "../data/" + output_image_name)
        try:
            dehaze(haze_image_path, output_image_path)
        except RuntimeError as e:
            return HttpResponse(e)
        return HttpResponse(output_image_name)
    else:
        return HttpResponse("参数错误")


def calculateDehazeIndex(request: HttpRequest):
    haze_image_name = request.POST["haze_image"]
    clear_image_name = request.POST["clear_image"]
    haze_image_path = os.path.join(script_dir, "../data/" + haze_image_name)
    clear_image_path = os.path.join(script_dir, "../data/" + clear_image_name)

    psnr, ssim = calculate(haze_image_path, clear_image_path)
    return HttpResponse(
        json.dumps(
            {'psnr': psnr, 'ssim': ssim}
        ), content_type='application/json')
