from tcia_utils import nbia

# 1) LIDC-IDRI içinden birkaç CT serisi listele
series_list = nbia.getSeries(collection="LIDC-IDRI")
if series_list:
    # İlk 2 seriyi göster
    for s in series_list[:2]:
        print("Series:", s["SeriesInstanceUID"], "| Study:", s["StudyInstanceUID"])
    
    # 2) İlk seriyi indir
    first_series_uid = series_list[0]["SeriesInstanceUID"]
    print(f"\nDownloading series: {first_series_uid}")
    out = nbia.downloadSeries(
        series_data=[first_series_uid], 
        input_type='list',
        path="data_cache/raw"
    )
    print("Download complete!")
    if out is not None:
        print("Downloaded series info:")
        print(out)
else:
    print("No series found")
