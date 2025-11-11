import os
import SimpleITK as sitk
import numpy as np
from skimage import morphology, measure

def basic_lung_mask(in_nii, out_mask_nii):
    img = sitk.ReadImage(in_nii)
    vol = sitk.GetArrayFromImage(img)  # z,y,x (HU)

    # 1) HU eşiği: akciğer hava alanı ~ [-1000, -320]
    lung = (vol >= -1000) & (vol <= -320)

    # 2) Her dilimde morfolojik açma ve en büyük 2 bileşeni tut (iki akciğer)
    mask = np.zeros_like(lung, dtype=np.uint8)
    for z in range(lung.shape[0]):
        sl = lung[z].astype(np.uint8)
        sl = morphology.opening(sl, morphology.disk(3))
        labels = measure.label(sl, connectivity=1)
        # en büyük iki bölgeyi seç
        if labels.max() > 0:
            regions = sorted(measure.regionprops(labels), key=lambda r: r.area, reverse=True)
            keep = np.isin(labels, [r.label for r in regions[:2]])
            mask[z] = keep.astype(np.uint8)

    # 3) Küçük delikleri doldurma
    mask = morphology.remove_small_holes(mask.astype(bool), area_threshold=64).astype(np.uint8)

    # 4) NIfTI olarak yaz
    mask_img = sitk.GetImageFromArray(mask)
    mask_img.CopyInformation(img)
    sitk.WriteImage(mask_img, out_mask_nii)
    return True
