import os, zipfile, glob

CACHE_DIR = "data_cache/raw"

def discover_series_paths(cache_dir=CACHE_DIR):
    # hem klasör hem zip varsa ikisini de döndür
    zips = glob.glob(os.path.join(cache_dir, "*.zip"))
    dirs = [d for d in glob.glob(os.path.join(cache_dir, "*")) if os.path.isdir(d)]
    return dirs, zips

def unzip_series(zippath, out_dir=CACHE_DIR):
    with zipfile.ZipFile(zippath, 'r') as zf:
        # Bazı paketler tek klasör içinde, bazısı doğrudan DICOM’lar; ikisini de destekle
        top = os.path.splitext(os.path.basename(zippath))[0]
        target = os.path.join(out_dir, top)
        os.makedirs(target, exist_ok=True)
        zf.extractall(target)
    return target
