
# Manual Data Inputs

This folder contains datasets that must be exported manually from LSEG Workspace (Refinitiv) and therefore cannot be redistributed in this repository due to licensing restrictions.

The Python pipeline expects these files to exist locally in order to construct the final dataset.

These files are **not included in the GitHub repository**.

---

# Why manual inputs are required

Some datasets used in this project are not accessible through the Refinitiv Python API or require Workspace exports.

Examples include:

- Historical bond yields for specific corporate bonds
- Certain bond-level metadata
- Data exported directly from LSEG Workspace Excel tools

Because these datasets originate from licensed sources, they cannot be redistributed publicly.

---

# Folder structure

The expected structure inside this directory is:

```
data/inputs/
│
└── bonds_empresas/
    ├── (manual Excel exports placed here)
```

The Python pipeline will read files located in this folder when constructing the panel dataset.

---

# Required files

You must export the necessary datasets from **LSEG Workspace** and place them inside:

```
data/inputs/bonds_empresas/
```

These exports typically include bond-level information such as:

- Yield to maturity
- Bond identifier (ISIN / CUSIP)
- Issuer identifier
- Pricing information
- Maturity and coupon characteristics

The exact fields depend on the query used in LSEG Workspace.

---

# How to regenerate the files

1. Open **LSEG Workspace (Refinitiv)**.
2. Navigate to the bond search or data export tools.
3. Query the corporate bonds corresponding to the firms in the project universe.
4. Export the results to **Excel (.xlsx)**.
5. Save the files inside:

```
data/inputs/bonds_empresas/
```

Do **not rename columns** expected by the pipeline.

---

# Important notes

- These files are required for the panel construction notebook:

```
notebooks/02_construccion_panel.ipynb
```

- If the files are missing, the pipeline will fail with a file-not-found error.

- These datasets are not distributed due to Refinitiv licensing restrictions.

---

# Reproducibility statement

The repository provides the full code required to process the data and estimate the econometric models.

However, users must have valid access to **LSEG Workspace / Refinitiv** in order to regenerate the raw datasets used in the analysis.