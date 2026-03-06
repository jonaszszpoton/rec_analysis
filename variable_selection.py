import pandas as pd
import re

class VariableSelection:
    def __init__(self, file_path):
        self.file_path = file_path

    def select_variables(self):
        """
        Selects variables from CPRS.csv based on the Adversarial Audit methodology.
        Returns: usable_features, y_val, excluded_leakage, excluded_sparse, benchmarks, metadata_dates
        """
        df_head = pd.read_csv(self.file_path, nrows=0)
        all_cols = df_head.columns.tolist()

        # Target variables (y)
        y_targets = [
            'V376_REIN_PENITENCIARIA', 
            'REINCIDENCIA_VIOLENTA', 
            'V374_REIN_JUDICIAL_19', 
            'V373_REIN_JUDICIAL_2021'
        ]

        # 1. OVERT LEAKAGE (Information from the future)
        # Note: Patterns V4 and V5 removed to keep 'Type of Exit' features.
        leakage_patterns = [
            r'ID_', r'^V[1-3]_', r'REINCID', r'REIN_', r'DATA_REIN', 
            r'POSTERIOR', r'SUPERVIV', r'TEMPS_REIN', r'DETENCI', 
            r'XXXXXXXXX', r'V3[0-9][0-9]', r'EDAT_REIN', r'INGRES_POST', 
            r'EVO_', r'LCPB', r'DATASORTIDA', r'REVOCACIO_LC', r'TIPUSCLASSIFICACIOLD'
        ]

        # 2. SPARSE EVALUATION BLOCKS (Missing Data Leakage)
        sparse_eval_blocks = [r'R1C_', r'R1S_', r'R2C_', r'R2S_', r'R3S_']

        # 3. BENCHMARKS (Final and Prior RisCanvi outputs)
        riscanvi_benchmarks = [
            r'R[1-3]_REVI', r'R[1-3]_VIAU', r'R[1-3]_VIIN', r'R[1-3]_TRCO', r'R[1-3]_VICT',
            r'R_EVO_', r'R2_CP_AVA', r'R1_CP_AVA', r'TIPUS_AVALUACIONS'
        ]

        y_val = []
        excluded_leakage = []
        excluded_sparse = []
        benchmarks = []
        metadata_dates = []
        usable_features = []

        for col in all_cols:
            # Check if it is a target first to prevent it from being marked as leakage
            if col in y_targets:
                y_val.append(col)
                continue

            is_leakage = any(re.search(p, col, re.IGNORECASE) for p in leakage_patterns)
            is_sparse = any(re.search(p, col, re.IGNORECASE) for p in sparse_eval_blocks)
            is_benchmark = any(re.search(p, col, re.IGNORECASE) for p in riscanvi_benchmarks)
            is_date = re.search(r'DATA', col, re.IGNORECASE) # Broad match for DATANAIX, etc.

            if is_leakage:
                excluded_leakage.append(col)
            elif is_sparse:
                excluded_sparse.append(col)
            elif is_benchmark:
                benchmarks.append(col)
            elif is_date:
                metadata_dates.append(col)
            else:
                usable_features.append(col)

        return usable_features, y_val, excluded_leakage, excluded_sparse, benchmarks, metadata_dates

    def bias_variables(self, usable_features):
        """
        Identifies variables prone to data bias within the usable features set.
        Used for Uncertainty-based demonstration set selection (fairness augmenting).
        """
        bias_categories = {
            'protected_attributes': [
                r'SEXE', r'ESTRANGERS', r'NACIONALITAT', r'AREAGEOG', r'RESIDENCIA', r'EXPULSIO'
            ],
            'socio_economic': [
                r'ESTUDIS', r'NivellEducatiu', r'ProblemesOcupacio', 
                r'MancaRecursosEconomics', r'CarreguesFamiliars', r'INSTRUCCIO'
            ],
            'static_biographical': [
                r'DesajustInfantil', r'AntecedentsFamilia', 
                r'SocialitzacioProblematica', r'PertinençaGrupRisc'
            ],
            'age_bias': [
                r'EDAT'
            ],
            'health_clinical_bias': [
                r'TranstornMental', r'TranstornPersonalitat', r'BaixCI', 
                r'DROGUES', r'ALCOHOL', r'SALUTMENTAL'
            ],
            'integration_language': [
                r'CATALA', r'CASTELLA'
            ],
            'institutional_bias': [
                r'INCIDENTS', r'EXPEDIENTS', r'ConflictesAmbInterns', r'Incompliments', r'REGRESSIONS'
            ],
            'victimization_bias': [
                r'VictimaVIGE'
            ]
        }

        bias_map = {cat: [] for cat in bias_categories}
        
        for col in usable_features:
            for cat, patterns in bias_categories.items():
                if any(re.search(p, col, re.IGNORECASE) for p in patterns):
                    bias_map[cat].append(col)
        
        return bias_map

    def get_bias_column_list(self, usable_features):
        """
        Returns a flat list of all unique columns identified as potential bias sources.
        """
        bias_map = self.bias_variables(usable_features)
        flat_list = []
        for cols in bias_map.values():
            flat_list.extend(cols)
        return list(set(flat_list))
