#!/usr/bin/env python
# encoding: utf-8
'''
@author: lurenjia
@contact: 1499418300@qq.com
@file: cutImg.py
@time: 2018/7/17 14:50
@desc:图片裁剪测试,原文链接：https://zhuanlan.zhihu.com/p/38974520?utm_source=wechat_timeline&utm_medium=social&utm_oi=31489056047104&from=timeline
'''

import sys

import numpy as np
from imageio import imread, imwrite
from scipy.ndimage.filters import convolve

# tqdm并非必需，但能为提供很美观的进度条，方便我们查看进度
from tqdm import trange

# 计算能量图
def calc_energy(img):
    filter_du = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])
    # 这会将它从2D滤波转换为3D滤波器
    # 为每个通道：R，G，B复制相同的滤波器
    filter_du = np.stack([filter_du] * 3, axis=2)

    filter_dv = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])
    # 这会将它从2D滤波转换为3D滤波器
    # 为每个通道：R，G，B复制相同的滤波器
    filter_dv = np.stack([filter_dv] * 3, axis=2)

    img = img.astype('float32')
    convolved = np.absolute(convolve(img, filter_du)) + np.absolute(convolve(img, filter_dv))

    # 我们将红，绿，蓝通道中的能量相加
    energy_map = convolved.sum(axis=2)
    return energy_map


# 找到能量值最小的缝隙
def minimum_seam(img):
    r, c, _ = img.shape
    energy_map = calc_energy(img)

    M = energy_map.copy()
    backtrack = np.zeros_like(M, dtype=np.int)

    for i in range(1, r):
        for j in range(0, c):
            # 处理图像的左侧边缘，确保我们不会索引-1
            if j == 0:
                idx = np.argmin(M[i - 1, j:j + 2])
                backtrack[i, j] = idx + j
                min_energy = M[i - 1, idx + j]
            else:
                idx = np.argmin(M[i - 1, j - 1:j + 2])
                backtrack[i, j] = idx + j - 1
                min_energy = M[i - 1, idx + j - 1]

            M[i, j] += min_energy

    return M, backtrack

# 从具有最小能量值的缝隙中删除像素
def carve_column(img):
    r, c, _ = img.shape

    M, backtrack = minimum_seam(img)

    # 创建一个(r,c)矩阵，填充值为True
    # 后面会从值为False的图像中移除所有像素
    mask = np.ones((r, c), dtype=np.bool)

    # 找到M的最后一行中的最小元素的位置
    j = np.argmin(M[-1])

    for i in reversed(range(r)):
        # 标记出需要删除的像素
        mask[i, j] = False
        j = backtrack[i, j]

    # 因为图像有3个通道，我们将蒙版转换为3D
    mask = np.stack([mask] * 3, axis=2)

    # 删除蒙版中所有标记为False的像素，
    # 将其大小重新调整为新图像的维度
    img = img[mask].reshape((r, c - 1, 3))

    return img

# 在每一列重复此项操作
def crop_c(img, scale_c):
    r, c, _ = img.shape
    new_c = int(scale_c * c)

    for i in trange(c - new_c): # use range if you don't want to use tqdm
        img = carve_column(img)

    return img


def main():
    scale = float(0.5)
    in_filename = '1.jpg'
    out_filename = '1-1.jpg'
    # out_filename = sys.argv[3]

    img = imread(in_filename)
    out = crop_c(img, scale)
    imwrite(out_filename, out)

if __name__ == '__main__':
    main()
