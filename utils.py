from scipy import ndimage as ndi
import numpy as np
from skimage import io
from skimage.filters import threshold_triangle, threshold_yen
from skimage.morphology import label, binary_dilation, binary_erosion, remove_small_objects,watershed
from skimage.measure import marching_cubes_lewiner, regionprops, mesh_surface_area
import os
from mayavi import mlab
import csv

voxel_spacing = (1,0.198,0.198)
area_threshold = 1000

def remove_large_objects(ar, max_size=64, connectivity=1, in_place=False):

    if in_place:
        out = ar
    else:
        out = ar.copy()

    if max_size == 0:  # shortcut for efficiency
        return out

    if out.dtype == bool:
        selem = ndi.generate_binary_structure(ar.ndim, connectivity)
        ccs = np.zeros_like(ar, dtype=np.int32)
        ndi.label(ar, selem, output=ccs)
    else:
        ccs = out

    try:
        component_sizes = np.bincount(ccs.ravel())
    except ValueError:
        raise ValueError("Negative value labels are not supported. Try "
                         "relabeling the input with `scipy.ndimage.label` or "
                         "`skimage.morphology.label`.")

    too_small = component_sizes > max_size
    too_small_mask = too_small[ccs]
    out[too_small_mask] = 0

    return out


def process_img(args):
    file_path, microglia_list = args
    file_name = os.path.basename(file_path)

    dose = ''
    time = ''
    area = ''

    if '1g' in file_name:
        dose = '1g'
    elif '2g' in file_name:
        dose = '2g'
    elif '4g' in file_name:
        dose = '4g'
    elif 'Sal in file_name':
        dose = 'Sal'

    if '.25hr' in file_name:
        time = '0.25'
    elif '.5hr' in file_name:
        time = '0.5'
    elif '1hr' in file_name:
        time = '1'
    elif '2hr' in file_name:
        time = '2'
    else:
        time = '0'

    if 'nac' in file_name.lower():
        area = 'NAc'
    elif 'vta' in file_name.lower():
        area = 'VTA'
    else:
        raise Exception('You dummy')

    image = io.imread(file_path)
    thresh = threshold_yen(image)
    binary_global = (image > thresh).astype('int')
    # binary_global = restoration.denoise_nl_means(binary_global)

    kernel_dilate = np.ones((1, 5, 5))
    #
    kernel_erode = np.ones((1, 5, 5))
    # kernel_erode = np.ones((1, 1, 1))
    dilated = binary_dilation(binary_global, selem=kernel_dilate).astype('int')
    eroded = binary_erosion(dilated, selem=kernel_erode).astype('uint8')

    labeled = label(eroded, connectivity=3)
    labeled = remove_small_objects(labeled, 3000)
    labeled = remove_large_objects(labeled, 80000)

    labeled = labeled.astype('uint8')

    for i, region in enumerate(regionprops(labeled)):
        current_region = {}
        current_region['index'] = i
        current_region['volume'] = region.area
        verts, faces, normals, values = marching_cubes_lewiner(region.image, 0.0, spacing=voxel_spacing)
        current_region['surface_area'] = mesh_surface_area(verts, faces)
        current_region['filename'] = file_name
        current_region['dose'] = dose
        current_region['area'] = area
        current_region['time'] = time
        current_region['vol/sa'] = current_region['volume'] / current_region['surface_area']

        microglia_list.append(current_region)
