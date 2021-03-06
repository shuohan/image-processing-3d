#!/usr/bin/env python

import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from improc3d.reslice import reslice3d, calc_transformed_shape
from improc3d.reslice import transform_to_axial
from improc3d.reslice import transform_to_coronal
from improc3d.reslice import transform_to_sagittal
from improc3d.crop import calc_bbox3d


obj = nib.load('image.nii.gz')
image = obj.get_data()
affine = obj.affine

mask = nib.load('mask.nii.gz').get_data()
bbox = calc_bbox3d(mask > 0)
pivot = tuple([int((s.stop + s.start) / 2) for s in bbox])

LPIm1 = reslice3d(image, affine)
shape = calc_transformed_shape(image.shape, affine)
assert np.array_equal(shape, LPIm1.shape)

LPIm2 = reslice3d(image, affine, target_shape=(100, 100, 100))
LPIm3 = reslice3d(image, affine, target_shape=(128, 96, 96), pivot=pivot)

axial = transform_to_axial(image, affine)
coronal = transform_to_coronal(image, affine)
sagittal = transform_to_sagittal(image, affine)

images = (image, LPIm1, LPIm2, LPIm3, axial, coronal, sagittal)
plt.figure()
for i, im in enumerate(images):
    im = np.transpose(im, axes=[1, 0, 2])
    plt.subplot(3, len(images), len(images) * 0 + i + 1)
    plt.imshow(im[:, :, im.shape[2]//2], cmap='gray')
    plt.subplot(3, len(images), len(images) * 1 + i + 1)
    plt.imshow(im[:, im.shape[1]//2, :], cmap='gray')
    plt.subplot(3, len(images), len(images) * 2 + i + 1)
    plt.imshow(im[im.shape[0]//2, :, :], cmap='gray')
plt.show()
