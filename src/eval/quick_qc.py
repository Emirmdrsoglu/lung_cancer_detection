import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

def show_middle_slice(nii_path, window_center=-600, window_width=1500):
    img = sitk.ReadImage(nii_path)
    vol = sitk.GetArrayFromImage(img)  # z,y,x  (HU)
    zmid = vol.shape[0] // 2
    slice_hu = vol[zmid]

    # windowing: W/L → [L - W/2, L + W/2]
    low = window_center - window_width/2
    high = window_center + window_width/2
    slice_w = np.clip(slice_hu, low, high)
    slice_w = (slice_w - low) / (high - low)  # 0-1
    plt.imshow(slice_w, cmap='gray')
    plt.title(f"{nii_path} | z={zmid}")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    import sys
    show_middle_slice(sys.argv[1])
