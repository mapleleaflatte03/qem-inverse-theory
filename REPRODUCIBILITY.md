# Reproducibility

## Setup

```bash
git clone https://github.com/mapleleaflatte03/qem-inverse-theory.git
cd qem-inverse-theory
pip install -e ".[dev]"
```

## Run tests

```bash
python -m pytest tests/ -q
```

Expected: 41 tests pass.

## Run all experiments

```bash
python experiments/01_constrained_inverse_zne.py
python experiments/02_aicc_small_sample_failure.py
python experiments/03_finite_shot_phase_diagram.py
python experiments/04_bayesian_credible_intervals.py
python experiments/05_structured_escape_hatches.py
python experiments/06_n_sensitivity.py
python experiments/07_bias_ambiguity_tradeoff.py
```

## Generate figures

```bash
python experiments/generate_figures.py
```

Output: `figures/*.pdf` and `figures/*.png`

## Build paper

```bash
cd paper
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Expected: `paper/main.pdf` (3+ pages). Citation warnings for unverified entries are expected.

## Smoke check (all-in-one)

```bash
bash scripts/smoke_check.sh
```

## Known limitations

- All experiments use synthetic data (no quantum hardware)
- Results directory is gitignored; regenerate with experiment scripts
- Some citations in `paper/literature.md` are marked VERIFY
- Paper is a draft skeleton, not a finished manuscript
- Python 3.10+ required
