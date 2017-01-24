# -*- coding: UTF-8 -*-
"""
截取网页中的图片水印
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
可以提供参数指定获取范围、截取范围
将图片原图及裁剪后的修改名称后放置
"""

import os
import argparse
import urllib
from urlparse import parse_qs, urlparse

from PIL import Image
from pyquery import PyQuery as pq

parser = argparse.ArgumentParser(description='裁剪网页中的图片，可以指定图片dom范围及截取范围')
parser.add_argument('--url', dest='url', required=True)
parser.add_argument('--selector', dest='selector', default='img')
parser.add_argument('--crop_bottom', dest='crop_bottom', default=50)
parser.add_argument('--imgdir', dest='imgdir', default='crop_mp_images')
args = parser.parse_args()


if __name__ == '__main__':
    selector = args.selector
    url = args.url
    d = pq(url)

    # 保存获取到的图片地址
    src_list = []

    img_dom_list = d(selector)
    for img in img_dom_list:
        this = pq(img)
        src = this.attr('data-src')
        src_list.append(src) if src else None

    # 创建目录
    # 将原图和裁剪后的分别存储
    imgdir = args.imgdir
    if not os.path.exists(imgdir):
        os.mkdir(imgdir)

    imgdir_croped = imgdir + "_croped"
    if not os.path.exists(imgdir_croped):
        os.mkdir(imgdir_croped)

    print '工获取%s张图片' % len(img_dom_list)

    # 将文件保存到目录
    for i, src in enumerate(src_list):

        # 获取url中参数
        query = urlparse(url).query
        query_dict = parse_qs(query, keep_blank_values=True)

        mid = query_dict.get('mid')[0]
        idx = query_dict.get('idx')[0]

        # 构建图片名称
        file_name = '%s_%s_%s' % (mid, idx, i)
        img_path = imgdir + "/%s.jpg" % file_name

        # 裁剪后的图片名称
        crop_img_path = imgdir_croped + "/%s_crop.jpg" % file_name

        print '正在保存第%s张图片' % (i+1)
        urllib.urlretrieve(src, img_path)

        # 创建图片处理对象
        # 获取宽、高，确定裁剪区域
        im = Image.open(img_path)
        w, h = im.size

        # 只有高度超过200的才进行裁剪
        if h > 200:
            box = (0, 0, w, h-args.crop_bottom)
            im = im.crop(box)
            im.save(crop_img_path)

    print '处理完毕'
