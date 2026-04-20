### Performance Comparison: RisCanvi vs. Veto model

| Metric | Historical RisCanvi (Audit) | LR+XGB (veto model) |
| :--- | :--- | :--- |
| **Precision (PPV)** | ~17.9% / ~8% | 38.0% |
| **Recall (TPR)** | ~77.0% | 15.0% |
| **Specificity (TNR)** | ~57.0% | 99.0% |

### Results Interpretation:
1. **Precision vs. Recall**: The original RisCanvi may have been optimized for sensitivity (Recall: 77%), which resulted in very low precision (PPV: 17.9% for medium or high risk violent recidivism or 8% for high risk violent recidivism-only). The LR+XGB model was optimized for precision, resulting in 38% high risk violent recidivism precision.
2. **Selectivity**: The LR+XGB model (even without pre-processing de-biasing) is significantly more selective. While it *"catches"* fewer recidivists (only 15% of real recidivists are correctly classified as high-risk) and issues high-risk scores far less frequently (a Capture Rate of 40%, meaning it issues 4 high-risk scores for every 10 actual recidivists), its predictions for high risk violent recidivism are almost 5 times more reliable (PPV: 38.0% vs. 8%).
3. **Fairness (Specificity)**: The higher specificity of LR+XGB (99% vs 57.0%) means the model is much less likely to misclassify low-risk individuals as potential violent recidivists, which is crucial from an ethical and legal standpoint.