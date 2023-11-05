import json
import os.path
import uuid

from django.http import HttpResponse, HttpRequest

import benchmark.C2PNet.run
from benchmark.C2PNet.run import calculate
from global_variable import DATA_PATH

dehaze_model = {
    'C2PNet/OTS.pkl': benchmark.C2PNet.run.dehaze,
}


def upload_image(request: HttpRequest):
    image_name = str(uuid.uuid4()) + ".png"
    image_path = os.path.join(DATA_PATH, image_name)
    image = request.body
    # 保存前端传来的图片
    with open(image_path, "wb") as destination:
        destination.write(image)
    return HttpResponse(json.dumps({'image_name': image_name}), content_type='application/json')


def download_image(request: HttpRequest, image_name: str):
    image_path = os.path.join(DATA_PATH, image_name)
    with open(image_path, "rb") as destination:
        return HttpResponse(destination.read(), content_type="image/png")


def dehaze_image(request: HttpRequest):
    data = json.loads(request.body)
    haze_image_name = data["haze_image"]
    model_name = data["model_name"]

    output_image_name = str(uuid.uuid4()) + ".png"
    haze_image_path = os.path.join(DATA_PATH, haze_image_name)
    output_image_path = os.path.join(DATA_PATH, output_image_name)

    try:
        dehaze = dehaze_model.get(model_name, None)
        if dehaze is not None:
            dehaze(haze_image_path, output_image_path)
        else:
            return HttpResponse("无法找到模型")
    except RuntimeError as e:
        return HttpResponse(e)

    return HttpResponse(json.dumps({'image_name': output_image_name}), content_type='application/json')


def calculate_dehaze_index(request: HttpRequest):
    data = json.loads(request.body)
    haze_image_name = data["haze_image"]
    clear_image_name = data["clear_image"]
    haze_image_path = os.path.join(DATA_PATH, haze_image_name)
    clear_image_path = os.path.join(DATA_PATH, clear_image_name)

    psnr, ssim = calculate(haze_image_path, clear_image_path)
    return HttpResponse(
        json.dumps(
            {'psnr': psnr, 'ssim': ssim}
        ), content_type='application/json')
