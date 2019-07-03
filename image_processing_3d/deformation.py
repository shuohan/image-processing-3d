# -*- coding: utf-8 -*-

import numpy as np
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.interpolation import map_coordinates

from .utils import convert_grid_to_coords


def deform3d(image, x_deformation, y_deformation, z_deformation, order=1):
    """Transforms an image using a deformation field.
    
    Args:
        image (numpy.ndarray, 3D or 4D): The image to deform. Channel first if
            it is 4D.
        x_deformation (numpy.ndarray, 3D): The x deformation. Per-voxel
            translation along the x axis.
        y_deformation (numpy.ndarray, 3D): The y deformation. Per-voxel
            translation along the y axis
        z_deformation (numpy.ndarray, 3D): The z deformation. Per-voxel
            translation along the z axis
        order (int): The interpolation order. See
            :func:`scipy.ndimage.interpolation.map_coordinates`

    Returns:
        numpy.ndarray, 3D: The deformed image

    """
    target_grid = np.meshgrid(*[np.arange(s) for s in image.shape[-3:]],
                              indexing='ij')
    deformation = [x_deformation, y_deformation, z_deformation]
    source_grid = [g - d for g, d in zip(target_grid, deformation)]
    source_coords = convert_grid_to_coords(source_grid)
    if len(image.shape) == 4:
        interpolation = [map_coordinates(im, source_coords, order=order)
                         for im in image]
        interpolation = np.vstack(interpolation)
    else:
        interpolation = map_coordinates(image, source_coords, order=order)
    deformed_image = np.reshape(interpolation, image.shape)
    return deformed_image


def calc_random_deformation3d(image_shape, sigma, scale):
    """Calculates a component of a random deformation field

    This deformation is along one axis. Call this function three times from
    deformation along x, y, and z axes. Check the source code for details of the
    computation.

    Args:
        image_shape (tuple of int, 3D): The shape of the image
        sigma (float): The value controling the smoothness of the deformation
            field. Larger the value is, smoother the field.
        scale (float): The deformation is supposed to draw from a uniform
            distribution [-eps, +eps]. Use this value to specify the upper bound
            of the sampling distribution. Larger the value is, stronger the
            deformation.

    Returns:
        result (numpy.ndarray, 3D): The component of the deformation filed 

    """
    random_state = np.random.RandomState(None)
    result = random_state.rand(*image_shape) * 2 - 1
    result = gaussian_filter(result, sigma)
    result = result / np.max(result) * scale
    return result
