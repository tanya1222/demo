from time import time

from flask import render_template, request, redirect, url_for, send_file, Blueprint

from config import BASE_DIR
from pillow.filterImage import img_filter, img_enhance, img_kernel,img_style_transfer
from utils.utils import save_file, get_kernel

filter_bp = Blueprint('filter_bp', __name__)


@filter_bp.route('/')
def index():
    return render_template('index.html')


@filter_bp.route("/filter", methods=['GET', 'POST'])
def image_filter():
    if request.method == 'POST':
        if request.form.get('filename') is None:
            # 接收图片并保存
            im = request.files['image']
            filename = save_file(im)
            if filename is None:
                return render_template('error.html', msg='不支持的文件格式!')
        else:
            filename = request.form.get('filename')
        # 获取滤波方式
        mode = request.form.get('mode', None)
        # 滤波
        res_name, olddata = img_filter(request.form, filename, mode=mode)
        # 返回结果
        print(filename)
        return redirect(url_for('filter_bp.filter_result', mode=mode, back='filter', filename=filename,
                                res_name=res_name, flag='filter', olddata=olddata))
    else:
        return render_template('filter/filter.html')


@filter_bp.route('/enhance', methods=['GET', 'POST'])
def image_enhance():
    if request.method == 'POST':
        if request.form.get('filename') is None:

            im = request.files['image']

            # 保存图像
            filename = save_file(im)
            if filename is None:
                return render_template('error.html', msg='不支持的文件格式!')
        else:
            filename = request.form.get('filename')

        enhance_type = request.form.get('enhance', None)
        factor_select = request.form.get('factor-select', None)
        factor_custom = request.form.get('factor-custom', None)
        # 设置增强因子
        if factor_custom != '':
            factor = float(factor_custom)
        else:
            factor = float(factor_select)
        # 图像增强
        res_name = img_enhance(filename, enhance_type, factor)
        return redirect(url_for('filter_bp.filter_result', mode=enhance_type, back='enhance', filename=filename, res_name=res_name,
                                flag='enhance', olddata=factor))
    else:
        return render_template('filter/enhance.html')


# 自定义卷积核:3x3 或者 5x5
@filter_bp.route('/kernel', methods=['GET', 'POST'])
def image_kernel():
    if request.method == 'POST':

        if request.form.get('filename') is None:
            # 保存图像
            im = request.files.get('image', None)
            # 保存图像
            filename = save_file(im)
            if filename is None:
                return render_template('error.html', msg='不支持的文件格式!')
        else:
            filename = request.form.get('filename')

        # 获取卷积核信息
        size = request.form.get('size', None)
        kernel_size, kernel = get_kernel(size)
        scale = request.form.get('scale', None)
        offset = request.form.get('offset', None)
        if kernel is None:
            return redirect(url_for('filter_bp.image_kernel'))

        # 处理图像
        res_name = img_kernel(filename, kernel_size, kernel, scale, offset)

        olddata = '#'.join(str(e) for e in kernel) + '#' + scale + '#' + offset
        return redirect(url_for('filter_bp.filter_result', mode='Custom Kernel', back='kernel', filename=filename,
                                res_name=res_name, olddata=olddata, flag='kernel-' + size))
    else:
        return render_template('filter/kernel.html')

@filter_bp.route("/style_transfer", methods=['GET', 'POST'])
def image_styletransfer():
    if request.method == 'POST':
        if request.form.get('filename') is None:

            # 接收图片并保存
            im = request.files['image']
            filename = save_file(im)
            im2=request.files['style_image']
            filename2=save_file(im2)
            style_name=im2.filename.split('.')[0]
            print(style_name)
            if filename is None:
                return render_template('error.html', msg='不支持的文件格式!')
        else:
            filename = request.form.get('filename')

        # 滤波
        res_name = img_style_transfer(filename,filename2)
        # 返回结果
        return redirect(url_for('filter_bp.filter_result',mode=style_name, back='style_transfer', filename=filename,
                                res_name=res_name, flag='style_transfer'))
    else:
        return render_template('filter/style_transfer.html')

@filter_bp.route('/filter_result')
def filter_result():
    mode = request.args.get('mode', None)
    filename = request.args.get('filename', None)
    res_name = request.args.get('res_name', None)
    flag = request.args.get('flag', None)
    olddata = request.args.get('olddata', None)
    back = request.args.get('back', None)
    if filename is None or res_name is None:
        return render_template('error.html', msg='不支持的文件格式')
    data = {
        'time': time(),
        'mode': mode,
        'filename': filename,
        'res_name': res_name,
        'flag': flag,
        'olddata': olddata,
        'back': back
    }
    return render_template('filter/result.html', **data)


@filter_bp.route('/download/<path:file_name>')
def sending_file(file_name):
    path = BASE_DIR + '/static/images/' + file_name
    return send_file(path, as_attachment=True, attachment_filename=file_name)


