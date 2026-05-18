COMMON_FILES = src/header.tex src/bibdb.bib
EXTRA_FLAGS = $(if $(DRY_RUN),--dry-run)$(if $(SILENT), --silent)
SCS = src/case-studies
BCS = build/case-studies
OCS = output/case-studies

all: $(OCS)/2-flight-delay.pdf $(OCS)/3-reinsurance.pdf

$(OCS)/2-flight-delay.pdf: $(SCS)/2-flight-delay.tex $(COMMON_FILES)
	./buildTex.py $< $@ --has-bib $(EXTRA_FLAGS) --build-dir=$(BCS)
$(BCS)/3-reinsurance-plots/binom1.pdf: $(SCS)/3-reinsurance-plots.py
	python3 $< $(dir $@)
$(OCS)/3-reinsurance.pdf: $(SCS)/3-reinsurance.tex $(COMMON_FILES) $(BCS)/3-reinsurance-plots/binom1.pdf
	./buildTex.py $< $@ --has-bib $(EXTRA_FLAGS) --build-dir=$(BCS)

.PHONY: index
index:
	rm -f output/datasets
	ln -sf ../datasets output/datasets
	./auto-index.py output
