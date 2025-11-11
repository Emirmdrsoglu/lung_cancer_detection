import os, io, zipfile, json, pathlib, requests
from dotenv import load_dotenv

load_dotenv()
BASE = os.getenv("NBIA_BASE_URL").rstrip("/")
COLL = os.getenv("LIDC_COLLECTION", "LIDC-IDRI")
API_KEY = os.getenv("TCIA_API_KEY")  # opsiyonel

def _headers():
    # TCIA/NBIA public için şart değil, varsa header’a koy
    return {"api_key": API_KEY} if API_KEY else {}

def get_series(collection=COLL, modality="CT", limit=3):
    url = f"{BASE}/getSeries"
    params = {"Collection": collection, "Modality": modality, "format": "json"}
    r = requests.get(url, params=params, headers=_headers(), timeout=60)
    r.raise_for_status()
    series = r.json()
    # küçük bir altküme dön
    return series[:limit]

def download_series_zip(series_instance_uid, out_dir):
    url = f"{BASE}/getImage"
    params = {"SeriesInstanceUID": series_instance_uid}
    r = requests.get(url, params=params, headers=_headers(), timeout=600)
    r.raise_for_status()
    out_dir = pathlib.Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    zpath = out_dir / f"{series_instance_uid}.zip"
    zpath.write_bytes(r.content)
    with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
        zf.extractall(out_dir / series_instance_uid)
    return out_dir / series_instance_uid
