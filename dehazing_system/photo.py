import json
import os.path
import uuid

from django.http import HttpResponse, HttpRequest

import benchmark.C2PNet.run
import benchmark.DehazeFormer.run
import benchmark.MixDehazeNet.run
from benchmark.metrics import calculate
from global_variable import DATA_PATH

dehaze_model = {
    'C2PNet/OTS.pkl': benchmark.C2PNet.run.dehaze,
    'C2PNet/ITS.pkl': benchmark.C2PNet.run.dehaze,
    'DehazeFormer/indoor/dehazeformer-b.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/indoor/dehazeformer-d.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/indoor/dehazeformer-l.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/indoor/dehazeformer-m.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/indoor/dehazeformer-s.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/indoor/dehazeformer-t.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/indoor/dehazeformer-w.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/outdoor/dehazeformer-b.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/outdoor/dehazeformer-m.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/outdoor/dehazeformer-s.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/outdoor/dehazeformer-t.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/reside6k/dehazeformer-b.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/reside6k/dehazeformer-m.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/reside6k/dehazeformer-s.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/reside6k/dehazeformer-t.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/rshaze/dehazeformer-b.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/rshaze/dehazeformer-m.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/rshaze/dehazeformer-s.pth': benchmark.DehazeFormer.run.dehaze,
    'DehazeFormer/rshaze/dehazeformer-t.pth': benchmark.DehazeFormer.run.dehaze,
    'MixDehazeNet/haze4k/MixDehazeNet-l.pth': benchmark.MixDehazeNet.run.dehaze,
    'MixDehazeNet/indoor/MixDehazeNet-l.pth': benchmark.MixDehazeNet.run.dehaze,
    'MixDehazeNet/indoor/MixDehazeNet-b.pth': benchmark.MixDehazeNet.run.dehaze,
    'MixDehazeNet/outdoor/MixDehazeNet-b.pth': benchmark.MixDehazeNet.run.dehaze,
    'MixDehazeNet/outdoor/MixDehazeNet-l.pth': benchmark.MixDehazeNet.run.dehaze,
    'MixDehazeNet/outdoor/MixDehazeNet-s.pth': benchmark.MixDehazeNet.run.dehaze,
    # 'MB-TaylorFormer/densehaze-MB-TaylorFormer-B.pth': benchmark..run.dehaze,
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
    result = []
    for index, key in enumerate(dehaze_model):
        # 首先将字符串按照 / 分割成数组
        parts = key.split('/')
        # 然后获取当前已经组装好的结果，准备继续向内部添加当前结点
        current = result
        # 遍历该数组，创建嵌套的数组
        for i, part in enumerate(parts):
            # 如果当前元素是数组的最后一个元素，也就是'DehazeFormer/indoor/dehazeformer-b.pth' 中的 'dehazeformer-b.pth'
            # 那么就将当前元素放入结果数组中
            if i == len(parts) - 1:
                current.append({'value': key, 'label': part.split(".")[0]})
            else:
                # 如果不是最后一个元素，则遍历结果数组，直到找到一个key和当前的元素一样的
                # 就更改当前结果数组
                found = False
                for child in current:
                    if child['value'] == part:
                        current = child['children']
                        found = True
                        break
                # 如果没有找到则创建一个新元素，插入到结果数组中，并且更新当前结果数组
                if not found:
                    new_node = {'value': part, 'label': part, 'children': []}
                    current.append(new_node)
                    current = new_node['children']
    return ok_response(result)


def get_model2(request: HttpRequest):
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

if __name__ == '__main__':
    print(get_model2())
