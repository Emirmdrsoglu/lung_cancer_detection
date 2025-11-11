from tcia_nbia import get_series, download_series_zip

# 1) LIDC-IDRI içinden birkaç CT serisi listele
series_list = get_series(limit=2)
for s in series_list:
    print("Series:", s["SeriesInstanceUID"], "| Study:", s["StudyInstanceUID"])

# 2) İlk seriyi indir ve aç
first = series_list[0]["SeriesInstanceUID"]
out = download_series_zip(first, out_dir="data_cache/raw")
print("Extracted to:", out)
