### **Predictive Parity Analysis (LR+XGB Model)**

**Methodology:**
To evaluate predictive disparity across subgroups, we use the **Capture Rate** (or Yield), defined as the total number of positive predictions divided by the total number of actual positives (`pred_rate / target_rate`). 

*Note: The global Capture Rate for the model is **~40%** (8 total positive predictions / 20 actual positives), which differs from the positive class Recall of **15%** (3 true positives / 20 actual positives). Capture Rate measures the model's total propensity to assign high-risk scores (strictness/volume), including False Positives, making it the appropriate metric for bias analysis.*

**Key Findings:**
The analysis reveals significant variance in how the model distributes its high-risk predictions relative to the actual recidivism rates of different subgroups.

*   **Disproportionate Strictness (Over-classification):**
    The model assigns high-risk scores at a substantially higher rate than its global baseline (40%) to the following groups:
    *   **Lowest Education (`V30_R3C_F18_NivellEducatiu == 1`):** Capture Rate of **66.7%** (+66.67% deviation from baseline).
    *   **Youngest Inmates (`V27_EDAT_PB_AGRUPADA == 1.0`):** Capture Rate of **54.5%** (+36.36% deviation from baseline).
    *   **Foreigners (`V19_ESTRANGERS == 2`):** Capture Rate of **50.0%** (+25.00% deviation from baseline).
    
    *Conclusion:* Belonging to these subgroups significantly increases the likelihood of receiving a high-risk score relative to the actual underlying risk of the group.

*   **Disproportionate Leniency (Under-classification):**
    The model is significantly more hesitant to assign high-risk scores to certain groups compared to its global baseline:
    *   **Older Inmates (`V27_EDAT_PB_AGRUPADA == 2.0`):** Capture Rate of **28.6%** (-28.57% deviation from baseline).
    
    *Conclusion:* The model exhibits a protective bias (leniency) toward older inmates, classifying them as high-risk less often than their actual recidivism rate would globally dictate.