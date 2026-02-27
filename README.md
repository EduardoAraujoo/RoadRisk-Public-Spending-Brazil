# RoadRisk-Public-Spending-Brazil

Data Science project to support decision-making for Minas Gerais (MG), Brazil stakeholders (State Government, Federal Highway Police/PRF, and SAMU MG) focusing on:
- understanding accident patterns and potential causes on MG highways;
- prioritizing enforcement and surveillance placement;
- improving emergency readiness (SAMU) with seasonal/temporal planning;
- analyzing public spending associated with accidents and operational response;
- building scenarios and forecasts (e.g., 2026) when feasible and validated by data.

> This repository follows the **CRISP-DM** methodology and enforces a strict separation between **exploration (notebooks)** and **production code (src)**.

## High-level goals
1. **EDA / Technical report**
   - Identify temporal (seasonality), geographic (highways/segments), and contextual (accident type/cause) patterns for MG.
2. **Data pipeline (ETL)**
   - Process large CSV datasets, filter to MG, standardize fields, and generate analysis/model-ready datasets.
3. **Modeling (only after data validation)**
   - Forecasting and/or risk estimation to support planning (e.g., accident risk, spending impact, enforcement scenarios).

## Methodology: CRISP-DM (mandatory)
- [x] Business Understanding (validated)
- [ ] Data Understanding
- [ ] Data Preparation
- [ ] Modeling
- [ ] Evaluation
- [ ] Deployment

Phase deliverables live in `docs/` and final outputs in `reports/`.

## Repository structure

- `data/`
  - `raw/`: immutable original data (never edit).
  - `processed/`: filtered/cleaned intermediate datasets (e.g., MG-only).
  - `final/`: final, feature-ready datasets for analysis/modeling.
- `notebooks/`: exploration and prototypes (EDA, quick checks).  
  Naming convention: `01_...`, `02_...`, etc.
- `src/`: production code (ETL, feature engineering, modeling, visualization).
- `configs/`: project configuration (paths, parameters, column mappings, filters).
- `models/`: exported trained artifacts (if applicable).
- `reports/`: final reports and figures.
- `docs/`: CRISP-DM documentation and data dictionary.
- `tests/`: automated tests (when applicable).

## Project rules (important)
- Do not mix production code into notebooks.
- Raw data stays in `data/raw/` and must not be committed (public repo).
- Every transformation outputs a new artifact into `data/processed/` or `data/final/`.

## Getting started
1. Put the raw CSV file(s) into `data/raw/`.
2. Update `configs/config.yaml` with:
   - raw file names,
   - the state/UF column name (if available),
   - the value representing Minas Gerais (e.g., `MG`),
   - key columns (date/highway/cause/type) once confirmed in the data dictionary.
3. Next CRISP-DM step: **Data Understanding**  
   Share the data dictionary so we can define critical columns and the EDA plan.

## Stakeholders
- Minas Gerais State Government
- PRF (Federal Highway Police)
- SAMU MG