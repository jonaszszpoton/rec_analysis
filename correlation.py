import pandas as pd
import numpy as np
from variable_selection import VariableSelection

def calculate_correlations(features_path):

    raw_data_path = '../data/CPRS_mapped_targets.csv'

    # 1. Get Target Variables using VariableSelection
    selector = VariableSelection(raw_data_path)
    _, y_targets, _, _, _, _ = selector.select_variables()

    # 2. Load Cleaned Features and Raw Targets
    X = pd.read_csv(features_path)
    # Load targets from raw data
    y_df = pd.read_csv(raw_data_path, usecols=y_targets)

    # 3. Filter only numeric variables
    X_numeric = X.select_dtypes(include=[np.number])
    y_numeric = y_df.select_dtypes(include=[np.number])

    # Combine for correlation matrix
    combined = pd.concat([X_numeric, y_numeric], axis=1)

    # 4. Calculate Correlation Matrix (Pearson)
    # Only care about X vs Y correlations
    corr_matrix = combined.corr()
    target_corrs = corr_matrix.loc[X_numeric.columns, y_numeric.columns]

    # 5. Save results
    output_path = '../data/feature_target_correlations.csv'
    target_corrs.to_csv(output_path)

    return target_corrs

