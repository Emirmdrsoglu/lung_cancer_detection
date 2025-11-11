import os, glob
import SimpleITK as sitk

def dicom_series_to_nifti(dicom_dir, out_nii_path):
    reader = sitk.ImageSeriesReader()
    # DICOM dizinindeki dosyaları seri halinde bul
    series_IDs = reader.GetGDCMSeriesIDs(dicom_dir)
    if not series_IDs:
        raise RuntimeError(f"Seri bulunamadı: {dicom_dir}")

    # Tek bir klasörde birden fazla seri olabilir; ilkini alıyoruz (istersen filtre ekleyebilirsin)
    series_files = reader.GetGDCMSeriesFileNames(dicom_dir, series_IDs[0])
    reader.SetFileNames(series_files)

    # OKUMA: slope/intercept uygulanır → intensiteler HU’dur
    image = reader.Execute()

    # NIfTI yaz
    sitk.WriteImage(image, out_nii_path)
    # metadata’yı not et
    spacing = image.GetSpacing()   # (sx, sy, sz)
    origin  = image.GetOrigin()
    direction = image.GetDirection()
    return {"spacing": spacing, "origin": origin, "direction": direction, "num_slices": image.GetSize()[2]}

if __name__ == "__main__":
    import sys, json
    dicom_dir = sys.argv[1]
    out_nii   = sys.argv[2]
    os.makedirs(os.path.dirname(out_nii), exist_ok=True)
    info = dicom_series_to_nifti(dicom_dir, out_nii)
    print(json.dumps(info, indent=2))
