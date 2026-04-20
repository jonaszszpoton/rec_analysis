========================================================================
RECIDIVISM RISK ASSESSMENT & FAIRNESS ANALYSIS (RisCanvi audit)
========================================================================

This project focuses on evaluating the fairness, biases, and predictive parity of the historical 'RisCanvi' recidivism risk assessment tool used in Catalonia, and comparing it against custom machine learning approaches (Logistic Regression + XGBoost veto system).

--- DIRECTORY STRUCTURE & FILES ---

1. NOTEBOOKS:
   * pipeline_1.ipynb: 
     Exploratory Data Analysis (EDA) and fairness evaluation of the original RisCanvi scoring system. Analyzes False Positive overrepresentation, distribution biases, and identifies 'hard data' acting as proxies for protected attributes (e.g., nationality, age).

   * pipeline_2.ipynb: 
     Training and evaluation of the custom baseline model (Logistic Regression enhanced by an XGBoost negative veto system). Focuses on optimizing precision for high-risk violent recidivism and conducts a comparative fairness analysis (Performance Parity) against RisCanvi.

   * pipeline_3.ipynb: 
     Input and model experimenting. Monte Carlo simulation for real target distribution for different risk levels. 

2. PYTHON SCRIPTS:
   * utils.py: 
     Contains core helper functions for the notebooks, including `check_score_consistency` (for RisCanvi score calibration) and `check_predictive_parity` (calculating Capture Rate differences across demographic subgroups).

3. DATA (/data):
   * Contains raw and processed CPR dataset with inmate demographic data, criminal history, clinical assessments, and actual recidivism outcomes.
   * Includes audit reports and fairness literature used for reference.

4. MARKDOWN SUMMARIES:
   * summary.md: High-level performance comparison (Precision, Recall, Specificity) between RisCanvi and the custom LR+XGB model.
   * fp_comparison.md: False Positive characteristics, volume, and bias drivers between the two systems.
   * parity_summary.md: Summary of predictive parity and subgroup capture rates for the custom model.