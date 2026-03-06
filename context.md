# Research Context: RisCanvi vs. TabPFN (Bias & Uncertainty)

## 1. Project Goal
The objective is to conduct an adversarial audit of the **RisCanvi** risk assessment system (Catalonia) and compare its predictive performance and fairness against **TabPFN (v2)**. A key part of the research involves **Uncertainty-based demonstration set selection** to improve fairness in an In-Context Learning (ICL) setup.

## 2. Dataset Specifics (data/CPRS.csv)
- **Observations:** 3,651 inmates released in 2015.
- **Variables:** 379 initial columns.
- **Target Variables (y):**
    - `V376_REIN_PENITENCIARIA`: General recidivism (Binary: 0/1).
    - `REINCIDENCIA_VIOLENTA`: Violent recidivism (Originally 1=Yes, 2=No; mapped to 1/0). Only ~5.8% prevalence (high imbalance).
- **Benchmarks (B):** Original RisCanvi outputs (`R3_REVI`, `R3_VIAU`, etc.). These are often sparse (e.g., 925 nulls for people who never underwent RisCanvi).

## 3. Key Findings & Methodology Adjustments
### Missing Data Leakage (The "R1/R2" Trap)
- **Problem:** Only ~300 inmates have complete First/Second evaluation data (`R1C`, `R2C`). Using these columns directly creates **proxy leakage**: the model learns that "presence of data" = "high risk" (because only high-risk inmates get the full evaluation).
- **Solution:** Follow the Eticas Audit methodology (Annex 5). Use **Alternative Variables** (consolidated factors in the `V29-V55` range / `R3C` block) which carry the 43 risk factors but are populated for the whole sample.

### Rigorous Leakage Filter
- **Future Indicators:** Removed `V15_REVOCACIO_LC` (Revocation of conditional release) and `V188_TIPUSCLASSIFICACIOLD` (Final status) as they are determined *after* or *because of* recidivism.
- **Future Events:** Removed all columns related to dates of re-arrest, survival times (`SUPERVIV`), and subsequent prison entries.

## 4. Bias Analysis (For Uncertainty Selection)
Variables identified as potential bias sources for the **Uncertainty Selection** algorithm:
- **Protected:** `SEXE`, `ESTRANGERS`, `NACIONALITAT`, `AREAGEOG`.
- **Socio-Economic:** `ESTUDIS`, `NivellEducatiu`, `MancaRecursosEconomics`, `ProblemesOcupacio`.
- **Integration:** `V23_CATALA`, `V24_CASTELLA` (Language as a proxy for discrimination).
- **Clinical/Health:** `TranstornMental`, `TranstornPersonalitat`, `BaixCI`.
- **Victimization:** `VictimaVIGE` (Penalizing victims).

## 5. Usable Features Info (Preprocessing Findings)
The dataset (154 usable features) follows specific administrative logics that dictate how NULL values should be handled to avoid bias:

### Imputation Conventions
- **Binary/Ordinal Flags (0 fill):** In fields like `V6_PROBLEMATICA_DROGUES` or `V159_HORES_...` (Treatment Hours), a NULL entry signifies the **absence of a record**, which in prison administration equates to "No problem detected" or "Zero hours attended". Filling with **0** preserves this logical signal.
- **Time-to-Event Variables (-1 fill):** In timeline fields like `V133_TEMPSFINS_1rPermís` (Days until first permit), a NULL signifies that the **event never occurred** (e.g., the inmate was never granted a permit). Filling with **-1** distinguishes these "non-events" from a "0-day wait," preventing the model from misinterpreting a denial of privileges as a rapid grant.
- **Continuous Variables (Median fill):** For strictly numeric data like age (`V27`, `V138`) or sentence duration (`V86`, `V87`) where only a few cases are missing, the **median** is used to maintain the overall distribution without introducing outliers.
- **Categorical Details (Mode/Placeholder fill):** Minor missing values in geography or education level are filled with the **mode** or a distinct "Unknown" category.

### Redundancy Note
There is significant overlap between "consolidated" factors (`R3C_F...`) and "dichotomous" factors (`_dico`). Both are kept in X, as TabPFN (Transformer-based) is robust to redundancy and can leverage the slight variance in information density between scales.

## 6. Software Architecture (venv/)
- `variable_selection.py`: Contains `VariableSelection` class. Logic for leakage removal and bias mapping.
- `execute.py`: Main entry point for data loading, target mapping, and feature preparation.
- `uncertainty_selection.py`: Script for identifying biased instances to build the demonstration set.
- **Tooling:** Using `%autoreload 2` in Jupyter to bridge with these modules.

## 6. Next Steps
1. **Model Baseline:** Train TabPFN on the 170 selected features to predict `V376` and `REINCIDENCIA_VIOLENTA`.
2. **Uncertainty Calculation:** Use TabPFN's posterior distribution to identify "uncertain" cases among biased groups.
3. **Demonstration Set Selection:** Select specific examples where the model is uncertain but the features are from protected groups to augment the ICL prompt (Fairness Augmentation).
4. **Comparison:** Measure AUC and Fairness metrics (e.g., Equalized Odds) against the benchmark variables.
