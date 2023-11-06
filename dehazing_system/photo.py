import json
import os.path
import uuid

from django.http import HttpResponse, HttpRequest

import benchmark.C2PNet.run
from benchmark.metrics import calculate
from global_variable import DATA_PATH

dehaze_model = {
    'C2PNet/OTS.pkl': benchmark.C2PNet.run.dehaze,
    'C2PNet/ITS.pkl': benchmark.C2PNet.run.dehaze,
}


def ok_response(data):
    message = {
        'code': '00000',
        'msg': '一切ok',
        'data': data
    }
    return HttpResponse(json.dumps(message), content_type='application/json')


def error_response(code, msg):
    message = {
        'code': code,
        'msg': msg,
        'data': None
    }
    return HttpResponse(json.dumps(message), content_type='application/json')


def get_model(request: HttpRequest):
    data = []
    for index, key in enumerate(dehaze_model):
        model = {
            'id': index,
            'model_name': key,
            'description': ''
        }
        data.append(model)
    return ok_response(data)


def upload_image(request: HttpRequest):
    image_name = str(uuid.uuid4()) + ".png"
    image_path = os.path.join(DATA_PATH, image_name)
    image = request.body
    # 保存前端传来的图片
    with open(image_path, "wb") as destination:
        destination.write(image)
    return ok_response({'image_name': image_name})


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
            dehaze(haze_image_path, output_image_path, model_name)
        else:
            return error_response('1', "无法找到模型")
    except RuntimeError as e:
        return error_response('1', e)

    return ok_response({'image_name': output_image_name})


def calculate_dehaze_index(request: HttpRequest):
    data = json.loads(request.body)
    haze_image_name = data["haze_image"]
    clear_image_name = data["clear_image"]
    haze_image_path = os.path.join(DATA_PATH, haze_image_name)
    clear_image_path = os.path.join(DATA_PATH, clear_image_name)

    psnr, ssim = calculate(haze_image_path, clear_image_path)
    return ok_response({'psnr': psnr, 'ssim': ssim})
