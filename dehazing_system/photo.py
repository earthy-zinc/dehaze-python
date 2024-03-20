import json
import os.path
import traceback
import uuid

from django.http import HttpResponse, HttpRequest

import benchmark.AECRNet.run
import benchmark.AODNet.run
import benchmark.C2PNet.run
import benchmark.CMFNet.run
import benchmark.D4.run
import benchmark.DCPDN.run
import benchmark.DEANet.run
import benchmark.Dehamer.run
import benchmark.DehazeFormer.run
import benchmark.DehazeNet.run
import benchmark.FFANet.run
import benchmark.FogRemoval.run
import benchmark.GCANet.run
import benchmark.GridDehazeNet.run
import benchmark.ITBdehaze.run
import benchmark.LKDNet.run
import benchmark.MADN.run
import benchmark.MSFNet.run
import benchmark.MixDehazeNet.run
import benchmark.PSD.run
# import benchmark.RIDCP.run
import benchmark.LightDehazeNet.run
import benchmark.SCANet.run
import benchmark.SGIDPFF.run
import benchmark.TSDNet.run
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
    'CMFNet/dehaze_I_OHaze_CMFNet.pth': benchmark.CMFNet.run.dehaze,
    'DEA-Net/HAZE4K/PSNR3426_SSIM9885.pth': benchmark.DEANet.run.dehaze,
    'DEA-Net/ITS/PSNR4131_SSIM9945.pth': benchmark.DEANet.run.dehaze,
    'DEA-Net/OTS/PSNR3659_SSIM9897.pth': benchmark.DEANet.run.dehaze,
    'FogRemoval/NH-HAZE_params_0100000.pt': benchmark.FogRemoval.run.dehaze,
    'ITBdehaze/best.pkl': benchmark.ITBdehaze.run.dehaze,
    # 'RIDCP/pretrained_RIDCP.pth': benchmark.RIDCP.run.dehaze,
    'SCANet/Gmodel_40.tar': benchmark.SCANet.run.dehaze,
    'SCANet/Gmodel_105.tar': benchmark.SCANet.run.dehaze,
    'SCANet/Gmodel_120.tar': benchmark.SCANet.run.dehaze,
    'Dehamer/dense/PSNR1662_SSIM05602.pt': benchmark.Dehamer.run.dehaze,
    'Dehamer/indoor/PSNR3663_ssim09881.pt': benchmark.Dehamer.run.dehaze,
    'Dehamer/NH/PSNR2066_SSIM06844.pt': benchmark.Dehamer.run.dehaze,
    'Dehamer/outdoor/PSNR3518_SSIM09860.pt': benchmark.Dehamer.run.dehaze,
    'AODNet/dehazer.pth': benchmark.AODNet.run.dehaze,
    'GridDehazeNet/indoor_haze_best_3_6': benchmark.GridDehazeNet.run.dehaze,
    'GridDehazeNet/outdoor_haze_best_3_6': benchmark.GridDehazeNet.run.dehaze,
    'DCPDN/netG_epoch_8.pth': benchmark.DCPDN.run.dehaze,
    'DehazeNet/defog4_noaug.pth': benchmark.DehazeNet.run.dehaze,
    'GCANet/wacv_gcanet_dehaze.pth': benchmark.GCANet.run.dehaze,
    'FFA-Net/its_train_ffa_3_19.pk': benchmark.FFANet.run.dehaze,
    'FFA-Net/ots_train_ffa_3_19.pk': benchmark.FFANet.run.dehaze,
    'LightDehazeNet/trained_LDNet.pth': benchmark.LightDehazeNet.run.dehaze,
    'AECR-Net/DH_train.pk': benchmark.AECRNet.run.dehaze,
    'AECR-Net/ITS_train.pk': benchmark.AECRNet.run.dehaze,
    'AECR-Net/NH_train.pk': benchmark.AECRNet.run.dehaze,
    'PSD/PSB-MSBDN': benchmark.PSD.run.dehaze,
    'PSD/PSD-FFANET': benchmark.PSD.run.dehaze,
    'PSD/PSD-GCANET': benchmark.PSD.run.dehaze,
    'D4': benchmark.D4.run.dehaze,
    'LKDNet/ITS/LKD-b/LKD-b.pth': benchmark.LKDNet.run.dehaze,
    'LKDNet/ITS/LKD-l/LKD-l.pth': benchmark.LKDNet.run.dehaze,
    'LKDNet/ITS/LKD-s/LKD-s.pth': benchmark.LKDNet.run.dehaze,
    'LKDNet/ITS/LKD-t/LKD-t.pth': benchmark.LKDNet.run.dehaze,
    'LKDNet/OTS/LKD-b/LKD-b.pth': benchmark.LKDNet.run.dehaze,
    'LKDNet/OTS/LKD-l/LKD-l.pth': benchmark.LKDNet.run.dehaze,
    'LKDNet/OTS/LKD-s/LKD-s.pth': benchmark.LKDNet.run.dehaze,
    'LKDNet/OTS/LKD-t/LKD-t.pth': benchmark.LKDNet.run.dehaze,
    'MSFNet/indoor.pth': benchmark.MSFNet.run.dehaze,
    'MSFNet/outdoor.pth': benchmark.MSFNet.run.dehaze,
    'TSDNet/GNet.tar': benchmark.TSDNet.run.dehaze,
    'MADN/model.pth': benchmark.MADN.run.dehaze,
    'SGID-PFF/SOTS_indoor.pt': benchmark.SGIDPFF.run.dehaze,
    'SGID-PFF/SOTS_outdoor.pt': benchmark.SGIDPFF.run.dehaze,
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
        traceback.print_exc()
        return error_response('1', e.__str__())

    return ok_response({'image_name': output_image_name})


def calculate_dehaze_index(request: HttpRequest):
    data = json.loads(request.body)
    haze_image_name = data["haze_image"]
    clear_image_name = data["clear_image"]
    haze_image_path = os.path.join(DATA_PATH, haze_image_name)
    clear_image_path = os.path.join(DATA_PATH, clear_image_name)

    psnr, ssim = calculate(haze_image_path, clear_image_path)
    return ok_response({'psnr': psnr, 'ssim': ssim})

