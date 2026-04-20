**False Positives Overrepresentation: RisCanvi vs. Final Model (LR+XGB)**<br><br>

| Feature Category | RisCanvi | Final Model (LR + XGB) |
| :--- | :--- | :--- |
| **Primary Drivers** | Subjective / clinical assessment (e.g., *V50 Actituds Procriminals*, *V47 Transtorn Personalitat*) | Objective / historical data (e.g., *V79 Inici Activitat Delictiva*, *V78 Historia Violencia*) |
| **Bias Ratio Baseline** | ~7.5% | ~1.3% |
| **Bias Ratio Peaks** | Moderate (up to ~4.7x overrepresentation) | Extreme (up to ~18.1x overrepresentation) |
| **FP Count (Volume)** | High (counts of 20-70 per subgroup) | Very low (counts of 3-5 per subgroup) |

**Key analytical issues:**

* **Statistical insignificance (sample size):**
The final model yields a total of 5 False Positives on the test set. Consequently, the extreme bias ratio (18.1x for early criminal onset) is driven by just 4 individual cases. This implies a more statistically unstable error distribution compared to RisCanvi's broader FP volume.

* **Hard data as protected attribute proxies:**
While the final model avoids human-in-the-loop subjectivity (human-based assesment) by relying on static variables (age of onset, criminal record), these variables often serve as strong proxies for protected attributes (e.g., socio-economic background, ethnicity), as has been shown in pipeline_1. This shifts the model from individual subjective bias to systemic historical bias, but increases standarization potential. 

* **The static risk (impossible rehabilitation):**
RisCanvi incorporates dynamic clinical factors, theoretically allowing an inmate's risk score to decrease upon behavioral improvement. The final model relies predominantly on static variables (past events). Consequently, it creates a feedback loop where an inmate's high-risk classification becomes permanent, negating the measurable impact of rehabilitation.