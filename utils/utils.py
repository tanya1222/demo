import os
from random import random
from time import time

from PIL import Image
from flask import request

from config import FIlTER_DICT, img_dir, upload_dir, ALLOW_FILE


def save_file(im):
    if im is None:
        return None
    suffix = im.filename.split('.')[-1].lower()
    if suffix not in ALLOW_FILE:
        return None
    # 创建文件夹
    parent_dir = upload_dir
    if not os.path.exists(parent_dir) and not os.path.isfile(parent_dir):
        os.mkdir(parent_dir)

    # 保存图片
    filename = ''.join(str(time()).split('.')) + '-' + str(random()).split('.')[-1] + '.' + suffix
    save_path = parent_dir + '/' + filename
    im.save(save_path)
    return filename


def get_img(filename) -> Image:
    im = Image.open(img_dir + filename, 'r')
    return im


def get_filter(mode, form):
    im_filter = FIlTER_DICT.get(mode, None)
    olddata = ''
    if mode == 'GaussianBlur':
        radius = form.get('GaussianBlur-radius', None)
        im_filter = im_filter(radius=float(radius))
        olddata = radius
    elif mode == 'UnsharpMask':
        radius = form.get('UnsharpMask-radius', None)
        percent = form.get('UnsharpMask-percent', None)
        threshold = form.get('UnsharpMask-threshold', None)
        im_filter = im_filter(float(radius), int(percent), int(threshold))
        olddata = radius + '#' + percent + '#' + threshold
    elif mode == 'RankFilter':
        size = form.get('RankFilter-size', None)
        rank = form.get('RankFilter-rank', None)
        im_filter = im_filter(size=int(size), rank=int(rank))
        olddata = size + '#' + rank
    elif mode in ["MedianFilter", "MinFilter", "MaxFilter", "ModeFilter"]:
        size = form.get('MFilter-size', None)
        im_filter = im_filter(int(size))
        olddata = size

    return im_filter, olddata


def save_img(res, filename):
    filename = filename.split('.')[-2] + '-res.' + filename.split('.')[-1]
    file_path = img_dir + filename
    res.save(file_path)
    return filename


def resize(filename, proportion=1.0):
    im = get_img(filename)
    width, height = im.size
    new_size = int(width * proportion), int(height * proportion)
    new_im = im.resize(new_size)
    return save_img(new_im, filename)


def get_kernel(size):
    if size is None:
        return None
    kernel = []
    if size == 'txt':
        size = (3, 3)
        for i in range(1, 4):
            for j in range(1, 4):
                element = request.form.get('r{}c{}'.format(i, j), None)
                if element is None:
                    return None
                kernel.append(float(element))

    elif size == 'fxf':
        size = (5, 5)
        for i in range(1, 6):
            for j in range(1, 6):
                element = request.form.get('fr{}c{}'.format(i, j), None)
                if element is None:
                    return None
                kernel.append(float(element))
    return size, kernel


if __name__ == '__main__':
    resize('jjy2.jpg', 0.5)