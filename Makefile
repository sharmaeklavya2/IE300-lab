COMMON_FILES = src/header.tex src/bibdb.bib
DRY_RUN_FLAG = $(if $(DRY_RUN),--dry-run)
SCS = src/case-studies
BCS = build/case-studies
OCS = output/case-studies

all: $(OCS)/2-flight-delay.pdf $(OCS)/3-reinsurance.pdf

$(OCS)/2-flight-delay.pdf: $(SCS)/2-flight-delay.tex $(COMMON_FILES)
	./buildTex.py $< $@ --has-bib $(DRY_RUN_FLAG) --build-dir=$(BCS)
$(BCS)/3-reinsurance-plots/binom1.pdf: $(SCS)/3-reinsurance-plots.py
	python3 $< $(dir $@)
$(OCS)/3-reinsurance.pdf: $(SCS)/3-reinsurance.tex $(COMMON_FILES) $(BCS)/3-reinsurance-plots/binom1.pdf
	./buildTex.py $< $@ --has-bib $(DRY_RUN_FLAG) --build-dir=$(BCS)

.PHONY: index
index:
	./auto-index.py .
