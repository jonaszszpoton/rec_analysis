import pandas as pd
from scipy.stats import chi2_contingency

def check_score_consistency(df, score_col, target_col, counts_threshold=20, subgroups=None):
    """
    Checks if the mean recidivism increases with RisCanvi scores in the selected subgroups.
    """
    def evaluate_trend(data, label):
        
        # ignoring small subgroups
        counts = data.groupby(score_col)[target_col].count()
        if (counts < counts_threshold).any():
            return None

        # real recidivism rate by score grouping
        trend = data.groupby(score_col)[target_col].mean()
        
        # monotonity checking ('True' if every next element >=)
        is_consistent = trend.is_monotonic_increasing
        
        # trend calculation
        diffs = trend.diff().dropna()
        violations = diffs[diffs < 0]
        
        return {
            'subgroup': label,
            'col': col,
            'val': val,
            'consistent': is_consistent,
            'violations_count': len(violations),
            'max_drop': violations.min() if not violations.empty else 0,
            'trend_values': trend.round(5).to_dict(),
            'counts': counts.to_dict()
        }

    results = []
    
    # value grouping
    for col in subgroups:
        for val in df[col].unique():
            subset = df[df[col] == val]
            
            res = evaluate_trend(subset, f"{col} == {val}")
            if res is not None:
                results.append(res)
    
    return pd.DataFrame(results)

def compare_features(data, group_col, target_group_val, feature_cols):
    results = []
    
    for col in feature_cols:
    
        contingency_table = pd.crosstab(data[group_col] == target_group_val, data[col])
        
        # chi-square test for differences
        chi2, p, dof, ex = chi2_contingency(contingency_table)
        
        # mean perentage difference (better interpretability)
        group_dist = data[data[group_col] == target_group_val][col].value_counts(normalize=True).round(2).to_dict()
        global_dist = data[data[group_col] != target_group_val][col].value_counts(normalize=True).round(2).to_dict()
        
        results.append({
            'feature': col,
            'p_value': p,
            'is_different': p < 0.05,
            'foreigner': group_dist,
            'others': global_dist
        })
        
    return pd.DataFrame(results)

def check_predictive_parity(df, pred_col, target_col, min_target_count=5, subgroups=None):
    """
    Evaluates predictive parity and differentiation capability of a binary classification model across subgroups.
    
    Methodology:
    Instead of checking raw prediction rates, this function calculates the 'Capture Rate' (or Yield) 
    for the global population and for each specified subgroup. The Capture Rate is defined as the 
    ratio of the predicted positive rate to the actual positive rate (pred_rate / target_rate).
    
    This approach normalizes the evaluation against the subgroup's inherent base rate. A subgroup with 
    a naturally higher prevalence of the positive class will naturally receive more positive predictions. 
    By looking at the Capture Rate, we measure how well the model proportionally identifies the positive 
    class relative to its true presence in that specific subgroup.
    
    The final metric, 'capture_diff_pct', calculates the absolute percentage difference between 
    the subgroup's Capture Rate and the global Capture Rate. 
    
    Interpretation:
    - A 'capture_diff_pct' close to 0% means the model differentiates the positive class in the 
      subgroup exactly as well as it does globally (high parity).
    - A high 'capture_diff_pct' indicates poor differentiation and potential bias: the model is either 
      severely under-predicting or over-predicting the positive class for this subgroup compared to 
      its global average behavior.
    """
    global_pred_rate = df[pred_col].mean()
    global_target_rate = df[target_col].mean()
    
    # Global ratio of predictions to actual positives
    global_capture_rate = global_pred_rate / global_target_rate if global_target_rate > 0 else 0
    
    results = []
    
    for col in subgroups:
        for val in df[col].dropna().unique():
            subset = df[df[col] == val]
            
            # ignoring subgroups with too few real positive cases
            target_count = subset[target_col].sum()
            if target_count < min_target_count:
                continue
                
            pred_rate = subset[pred_col].mean()
            
            # ignoring subgroups with no positive predictions
            if pred_rate == 0:
                continue
                
            target_rate = subset[target_col].mean()
            
            # Capture rate for the subgroup
            capture_rate = pred_rate / target_rate if target_rate > 0 else 0
            
            # Percentage difference from the global capture rate
            if global_capture_rate > 0:
                capture_diff_pct = (abs(capture_rate - global_capture_rate) / global_capture_rate) * 100
            else:
                capture_diff_pct = 0
            
            results.append({
                'subgroup': f"{col} == {val}",
                'col': col,
                'val': val,
                'size': len(subset),
                'target_count': target_count,
                'target_rate': target_rate.round(5),
                'pred_rate': pred_rate.round(5),
                'capture_rate': round(capture_rate, 5),
                'capture_diff_pct': round(capture_diff_pct, 2)
            })
            
    if not results:
        return pd.DataFrame()
        
    res_df = pd.DataFrame(results)
    # sorting by difference (ascending) - the closer to 0%, the closer to global differentiation
    # sorting by difference (descending) - the larger the %, the worse the disparity
    res_df = res_df.sort_values('capture_diff_pct', ascending=False).reset_index(drop=True)
    
    return res_df