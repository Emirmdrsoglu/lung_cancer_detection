# ===========================================
# LUNG-AI PROJECT MAKEFILE
# ===========================================

PYTHON = python
DATA_RAW = data_cache/raw
DATA_PROCESSED = data/processed

# UNIX ortamında ilk seri klasörünü otomatik seç
FIRST_SERIES_DIR := $(shell ls -d $(DATA_RAW)/*/ 2>/dev/null | head -n 1)
FIRST_NIFTI := $(DATA_PROCESSED)/first_series.nii.gz
FIRST_MASK := $(DATA_PROCESSED)/first_series_lungmask.nii.gz

.DEFAULT_GOAL := help

# ===========================================
# Görevler
# ===========================================

help:
	@echo ""
	@echo "LUNG-AI Make Komutları:"
	@echo "  make pull           → LIDC-IDRI serisi indir (API üzerinden)"
	@echo "  make nifti          → İlk indirilen seriyi HU + NIfTI formatına çevir"
	@echo "  make mask           → Akciğer maskesi oluştur"
	@echo "  make qc             → Orta slice görüntüle (quick QC)"
	@echo "  make pipeline       → Hepsini sırayla çalıştır"
	@echo "  make clean          → İşlenmiş veri ve cache'i temizle"
	@echo ""

# 1) LIDC serilerini indir
pull:
	@echo "📥 LIDC-IDRI serileri indiriliyor..."
	@$(PYTHON) -m src.api.example_pull
	@echo "✅ Download finished!"

# 2) DICOM serisini HU + NIfTI'ye dönüştür
nifti:
	@if [ -z "$(FIRST_SERIES_DIR)" ]; then \
		echo "❌ Hata: data_cache/raw içinde seri bulunamadı."; \
		echo "Önce: make pull"; \
		exit 1; \
	fi
	@echo "🔄 DICOM → HU → NIfTI"
	@echo "  Girdi klasörü: $(FIRST_SERIES_DIR)"
	@$(PYTHON) -m src.io.dicom_to_nifti "$(FIRST_SERIES_DIR)" "$(FIRST_NIFTI)"
	@echo "✅ NIfTI kaydedildi: $(FIRST_NIFTI)"

# 3) Akciğer maskesi oluştur
mask: nifti
	@echo "🫁 Akciğer maskesi oluşturuluyor..."
	@$(PYTHON) -c "from src.preprocessing.lung_mask import basic_lung_mask; basic_lung_mask('$(FIRST_NIFTI)','$(FIRST_MASK)')"
	@echo "✅ Mask oluşturuldu: $(FIRST_MASK)"

# 4) QC – orta slice göster
qc: nifti
	@echo "🔍 QC: orta slice görüntüleniyor..."
	@$(PYTHON) -m src.eval.quick_qc "$(FIRST_NIFTI)"

# 5) Hepsi bir arada
pipeline: pull nifti mask qc
	@echo "✅ Tüm pipeline başarıyla tamamlandı!"

# Temizlik
clean:
	@echo "🧹 Veri temizleniyor..."
	rm -rf $(DATA_RAW)/*
	rm -rf $(DATA_PROCESSED)/*
	@echo "✅ Temizlendi!"

