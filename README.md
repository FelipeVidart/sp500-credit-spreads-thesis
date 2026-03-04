
# S&P 500 – Structural Identification of Systematic and Aggregate Credit Risk

This repository contains the full data pipeline and econometric implementation for my Undergraduate Thesis in Finance.

The project studies how aggregate market and credit shocks — and heterogeneous firm-level exposure to those shocks — are reflected in corporate bond credit spreads of large S&P 500 firms.

All financial data are sourced exclusively from Refinitiv (Eikon / RDP) and processed in Python.

---

## Research Question

How are aggregate market and credit shocks, and firm-level heterogeneity in exposure to those shocks, reflected in corporate bond credit spreads of S&P 500 firms?

---

## Repository Structure

```
.
├── notebooks/
│   ├── 01_descarga_datos.ipynb
│   ├── 02_construccion_panel.ipynb
│   └── 03_runer_econometrico.ipynb
│
├── data/
│   ├── inputs/
│   │   └── bonds_empresas/
│   ├── raw/            (not versioned)
│   ├── clean/          (not versioned)
│   └── sample/
│
├── outputs/
│   ├── tables/
│   ├── figures/
│   └── logs/
│
├── docs/
├── src/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Data Source

All financial and market data are obtained exclusively from Refinitiv (Eikon / RDP).

Due to licensing restrictions, raw and processed datasets are not versioned in this repository.

If manual exports from Refinitiv Workspace are required, they must be placed in:

```
data/inputs/
```

---

## Data Access and Licensing

This project relies on data obtained from **LSEG Workspace / Refinitiv**.

Due to licensing restrictions, raw financial datasets cannot be redistributed through this repository.

Some datasets used in the analysis were exported manually from LSEG Workspace (for example, bond-level yields and metadata). These files must be placed locally inside:

```
data/inputs/
```

Detailed instructions for regenerating these files are provided in:

```
data/inputs/README_inputs.md
```

As a result, the repository is fully reproducible **conditional on having valid access to LSEG Workspace / Refinitiv**.

## Setup Instructions

### 1) Clone the repository

```bash
git clone <your_repository_url>
cd tesis-sp500-panel
```

### 2) Create a virtual environment

**Mac / Linux**

```bash
python -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure Refinitiv API Key

Create a file named `.env` in the project root directory and include:

```
EIKON_APP_KEY=YOUR_API_KEY_HERE
```

Do not commit this file to GitHub.

---

## Execution Order

The pipeline must be executed sequentially.

### Step 1 – Data Download

Run:

```bash
notebooks/01_descarga_datos.ipynb
```

This notebook downloads raw financial and market data from Refinitiv and stores them in:

```
data/raw/
```

---

### Step 2 – Panel Construction

Run:

```bash
notebooks/02_construccion_panel.ipynb
```

This notebook cleans, merges and constructs the final firm–month panel dataset.

Output generated:

```
data/clean/panel_master.parquet
```

---

### Step 3 – Econometric Estimation

Run:

```bash
notebooks/03_runer_econometrico.ipynb
```

This notebook estimates panel regressions (Models M0–M6) including firm and time fixed effects.

Outputs generated:

```
outputs/tables/
outputs/figures/
outputs/logs/
```

---

## Econometric Framework

The baseline structural specification estimated in the thesis is:

```
spread_{i,t} = α
             + β1 · market_shock_t
             + β2 · credit_shock_t
             + β3 · (exposure_i × market_shock_t)
             + β4 · (exposure_i × credit_shock_t)
             + controls_{i,t}
             + μ_i + τ_t + ε_{i,t}
```

Where:

- μ_i = firm fixed effects  
- τ_t = time fixed effects  
- Standard errors clustered at the firm level  

Robustness checks include alternative specifications and additional fixed-effect structures.

## Econometric Models

The empirical analysis estimates a sequence of panel models designed to progressively identify aggregate market and credit shocks and firm-level heterogeneity in exposure to these shocks.

The models follow the structure below:

| Model | Description |
|------|-------------|
| **M0** | Baseline specification with firm and time fixed effects. |
| **M1** | Macro-saturated specification including observable aggregate factors. |
| **M2** | Panel CAPM specification with an explicit aggregate market return. |
| **M3** | Heterogeneous CAPM specification allowing firm-level exposure to the market shock through interactions with firm characteristics. |
| **M4** | Model including an explicit aggregate credit factor capturing common credit market conditions. |
| **M5** | Heterogeneous credit specification allowing firm-level exposure to credit shocks. |
| **M6** | Full model including both market and credit channels jointly. |

All models include firm fixed effects and appropriate clustered standard errors.

---

## Reproducibility Notes

- Raw Refinitiv data cannot be redistributed.
- The repository contains the complete transformation and estimation pipeline.
- All empirical tables included in the thesis are generated directly from this codebase.

---

## Author

Undergraduate Thesis in Finance  
Universidad de San Andrés  
2025–2026
