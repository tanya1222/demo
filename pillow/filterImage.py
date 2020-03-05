from PIL import ImageFilter, ImageEnhance
from exception import NotExistEnhanceError
from utils.utils import get_img, get_filter, save_img
from Style_Transfer import style_transfer,load_image

import os
# 项目根目录
BASE_DIR = basedir = os.path.abspath(os.path.dirname(__file__))


def img_filter(form, filename, **kwargs):
    mode = kwargs.get('mode', None)

    img = get_img(filename)

    # 读取滤波方式
    im_filter, olddata = get_filter(mode, form)

    # 滤波处理
    res = img.filter(im_filter)
    # 返回处理后文件名称和原始参数
    return save_img(res, filename), olddata


def img_enhance(filename, enhance_type, factor):
    im = get_img(filename)
    if enhance_type == 'Color':
        enhancer = ImageEnhance.Color(im)
    elif enhance_type == 'Contrast':
        enhancer = ImageEnhance.Contrast(im)
    elif enhance_type == 'Brightness':
        enhancer = ImageEnhance.Brightness(im)
    elif enhance_type == 'Sharpness':
        enhancer = ImageEnhance.Sharpness(im)
    else:
        raise NotExistEnhanceError()
    res = enhancer.enhance(factor)
    return save_img(res, filename)


def img_kernel(filename, size, kernel, scale=None, offset=None):
    im = get_img(filename)
    if scale is not None and scale.strip() != '':
        scale = float(scale)
    else:
        scale = None
    if offset is not None and offset.strip() != '':
        offset = float(offset)
    else:
        offset = 0
    im_filter = ImageFilter.Kernel(size, kernel, scale, offset)
    res = im.filter(im_filter)
    return save_img(res, filename)

def img_style_transfer(filename,filename2):

    img = get_img(filename)
    filename_dir = '/Users/tanya/PycharmProjects/image6/static/images/'
    content_filename = filename_dir + filename
    content_image = load_image(content_filename, max_size=None)


    style_filename = filename_dir + filename2
    style_image = load_image(style_filename, max_size=300)

    content_layer_ids = [4]
    style_layer_ids = list(range(13))
    res = style_transfer(content_image=content_image,
                         style_image=style_image,
                         content_layer_ids=content_layer_ids,
                         style_layer_ids=style_layer_ids,
                         weight_content=5,
                         weight_style=10.0,
                         weight_denoise=0.3,
                         num_iterations=60,
                         step_size=10.0)
    # 滤波处理

    # 返回处理后文件名称和原始参数
    return save_img(res, filename)

if __name__ == '__main__':
    pass
    # i = get_img('jpg')
    # filter_type = ImageFilter.GaussianBlur(radius=-1)
    # res = i.pillow(filter_type)
    # i.show()
    # res.show()
