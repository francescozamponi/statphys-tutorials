# Introduction to statistical physics for non-physicists — programming tutorials

Notebooks of the programming sections of

> R. Kühn, P. Vivo and F. Zamponi, *Introduction to statistical physics for non-physicists*,
> Oxford University Press.

Each folder `Tutorial_N` contains the notebook `Tutorial_N.ipynb` that solves the programming problem
of chapter N, together with its data, and reproduces the figures and numbers of that section of the book.

| Notebook | Chapter | Run online |
|---|---|---|
| `Tutorial_2/Tutorial_2.ipynb` | 2 — Averages and extremes | [Colab](https://colab.research.google.com/github/OWNER/REPO/blob/main/Tutorial_2/Tutorial_2.ipynb) |
| `Tutorial_3/Tutorial_3.ipynb` | 3 — Data compression | [Colab](https://colab.research.google.com/github/OWNER/REPO/blob/main/Tutorial_3/Tutorial_3.ipynb) |
| `Tutorial_4/Tutorial_4.ipynb` | 4 — Inferring a distribution from a small dataset | [Colab](https://colab.research.google.com/github/OWNER/REPO/blob/main/Tutorial_4/Tutorial_4.ipynb) |
| `Tutorial_6/Tutorial_6.ipynb` | 6 — Correlations and compression in DNA sequences | [Colab](https://colab.research.google.com/github/OWNER/REPO/blob/main/Tutorial_6/Tutorial_6.ipynb) |
| `Tutorial_7/Tutorial_7.ipynb` | 7 — Sudden shifts in collective opinion | [Colab](https://colab.research.google.com/github/OWNER/REPO/blob/main/Tutorial_7/Tutorial_7.ipynb) |
| `Tutorial_8/Tutorial_8.ipynb` | 8 — Catastrophic forgetting in the Hopfield model | [Colab](https://colab.research.google.com/github/OWNER/REPO/blob/main/Tutorial_8/Tutorial_8.ipynb) |
| `Tutorial_10/Tutorial_10.ipynb` | 10 — Spectrum of a sparse graph | [Colab](https://colab.research.google.com/github/OWNER/REPO/blob/main/Tutorial_10/Tutorial_10.ipynb) |

## Running the notebooks

* **Online, on Google Colab:** follow the link in the table and run all cells. Data files are
  downloaded automatically from this repository or from their original source; when that is not
  possible (data that we cannot redistribute) the notebook explains where to get them and asks you
  to upload them.
* **Locally:** `pip install -r requirements.txt`, then `jupyter notebook`, and run a notebook from its
  own folder.

The random number generators are seeded, so that the notebooks reproduce the figures and numbers of
the book. Figures are saved as PDF next to the notebook through `bookfig.py`, which only sets their size
and fonts as in the book.

## Data

* **Tutorial 2.** T-cell receptor repertoires (Emerson *et al.*, Nat. Genet. 49, 659 (2017)), subset
  distributed with [MetaTCR](https://github.com/deepomicslab/MetaTCR): `tcr_clone_sizes.csv` (rebuilt
  by the notebook if missing). Heights and weights (SOCR, Dinov 2008), from
  [Kaggle](https://www.kaggle.com/datasets/burnoutminer/heights-and-weights-dataset/). City populations
  (appendix), from [simplemaps](https://simplemaps.com/data/world-cities) (basic version, CC BY 4.0).
* **Tutorial 3.** Text files generated as described in the book.
* **Tutorial 4.** International football results by Mart Jürisoo (CC0),
  [Kaggle](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017) /
  [GitHub](https://github.com/martj42/international_results); `results.csv` is the version of
  5 January 2025 used in the book.
* **Tutorial 6.** Bacteriophage λ (GenBank J02459), influenza A H1N1 PB2 segments (ENA DQ208309,
  GenBank CY044380), and two artificial sequences generated in the notebook.
* **Tutorial 8.** Images of the Kaggle competition [Dogs vs. Cats](https://www.kaggle.com/c/dogs-vs-cats),
  downloaded by the notebook with the Kaggle API (requires a Kaggle account and accepting the
  competition rules).
