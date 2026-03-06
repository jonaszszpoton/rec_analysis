from variable_selection import VariableSelection

def main():
    path = 'data/CPRS.csv'
    selector = VariableSelection(path)

    # 1. Get filtered features
    features, y_val, leakage, sparse, benchmarks, dates = selector.select_variables()

    # 2. Get bias variables
    bias_columns = selector.get_bias_column_list(features)
    print(f"--- UNCERTAINTY SELECTION: BIAS VARIABLES ---")
    print(f"Total potential bias columns found: {len(bias_columns)}")
    print("\nFull list of bias-prone variables:")
    for col in sorted(bias_columns):
        print(f"- {col}")

if __name__ == "__main__":
    main()
