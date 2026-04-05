COMMON_FILES = src/header.tex src/bibdb.bib
DRY_RUN_FLAG = $(if $(DRY_RUN),--dry-run)

all: output/case-studies/2-flight-delay.pdf

output/case-studies/2-flight-delay.pdf: src/case-studies/2-flight-delay.tex $(COMMON_FILES)
	./buildTex.py $< $@ --has-bib $(DRY_RUN_FLAG) --build-dir=build/case-studies

.PHONY: index
index:
	./auto-index.py .
