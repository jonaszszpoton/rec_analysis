import pandas as pd
import numpy as np

class PreProcessing:
    """
    Class for batch-based preprocessing of the CPRS dataset features.
    Each method processes a distinct subset of variables and returns a new DataFrame.
    """

    def _convert_to_numeric(self, df):
        """Helper to explicitly convert columns to numeric where possible."""
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                continue
        return df

    def v4_v27_prep(self, df_fragment):
        """
        Processes Batch 1: Administrative & Demographics (V4 to V27).
        """
        df = df_fragment.copy()

        target_zero_fill = ['V6_PROBLEMATICA_DROGUES', 'V7_PROBLEMÀTICA_SALUTMENTAL_DROGUES']
        for col in target_zero_fill:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        if 'V5_SORTIDA_ESGLAONADA' in df.columns:
            df['V5_SORTIDA_ESGLAONADA'] = df['V5_SORTIDA_ESGLAONADA'].fillna(-1)
        if 'V27_EDAT_PB_AGRUPADA' in df.columns:
            median_val = df['V27_EDAT_PB_AGRUPADA'].median()
            df['V27_EDAT_PB_AGRUPADA'] = df['V27_EDAT_PB_AGRUPADA'].fillna(median_val)
        return self._convert_to_numeric(df)

    def v28_v47_prep(self, df_fragment):
        """
        Processes Batch 2: Consolidated Risk Factors (V28 to V47).
        """
        df = df_fragment.copy()
        if 'V28_EDAT_SORTIDAPB_AGRUPADA' in df.columns:
            median_val = df['V28_EDAT_SORTIDAPB_AGRUPADA'].median()
            df['V28_EDAT_SORTIDAPB_AGRUPADA'] = df['V28_EDAT_SORTIDAPB_AGRUPADA'].fillna(median_val)
        return self._convert_to_numeric(df)

    def v48_v67_prep(self, df_fragment):
        """
        Processes Batch 3: Consolidated Risk Factors & Dico (V48 to V67).
        """
        df = df_fragment.copy()
        return self._convert_to_numeric(df)

    def v68_v87_prep(self, df_fragment):
        """
        Processes Batch 4: Crime Details & Sentence Duration (V68 to V87).
        """
        df = df_fragment.copy()
        sentence_cols = ['V86_DURADA_PENA_RisCanvi', 'V87_DURADA_PENA_PENITENCIARI']
        for col in sentence_cols:
            if col in df.columns:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
        return self._convert_to_numeric(df)

    def v88_v107_prep(self, df_fragment):
        """
        Processes Batch 5: Prison Conduct & Conduct Risk Factors (V88 to V107).
        """
        df = df_fragment.copy()
        duration_cols = ['V88_DURADA_PENA_ESTUDISANTER', 'V89_TEMPSCONDEMNA_ANUAL']
        for col in duration_cols:
            if col in df.columns:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
        return self._convert_to_numeric(df)

    def v108_v135_prep(self, df_fragment):
        """
        Processes Batch 6: Treatment & Timeline Variables (V108 to V135).
        """
        df = df_fragment.copy()
        if 'V132_TEMPSCONDEMNA_TOTAL' in df.columns:
            median_val = df['V132_TEMPSCONDEMNA_TOTAL'].median()
            df['V132_TEMPSCONDEMNA_TOTAL'] = df['V132_TEMPSCONDEMNA_TOTAL'].fillna(median_val)
        timeline_cols = ['V133_TEMPSFINS_1rPermís', 'V134_TEMPSFINS_3rGrau', 'V135_TEMPSFINS_LC']
        for col in timeline_cols:
            if col in df.columns:
                df[col] = df[col].fillna(-1)
        return self._convert_to_numeric(df)

    def v136_v158_prep(self, df_fragment):
        """
        Processes Batch 7: Special Timelines & Age Metrics (V136 to V158).
        """
        df = df_fragment.copy()
        special_timeline = ['V136_TEMPSFINS_86.4', 'V137_TEMPSFINS_UD']
        for col in special_timeline:
            if col in df.columns:
                df[col] = df[col].fillna(-1)
        age_cols = ['V138_EDAT_1RINGRÉS', 'V139_EDAT_DELICTEPBASE', 'V140_EDAT_PENABASE', 'V141_EDAT_SORTIDAPBASE']
        for col in age_cols:
            if col in df.columns:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
        return self._convert_to_numeric(df)

    def v159_v194_prep(self, df_fragment):
        """
        Processes Batch 8: Treatment Hours & Detailed Demographics (V159 to V194).
        Total features: ~16
        
        Logic:
        - Treatment Hours (V159-V168): NULL means 0 hours attended.
        - Demographics (V190-V194): Use mode or placeholder for minor missing data.
        """
        df = df_fragment.copy()

        # 1. TREATMENT HOURS (Fill with 0)
        hour_cols = [c for c in df.columns if c.startswith('V1') and '_H' in c]
        for col in hour_cols:
            df[col] = df[col].fillna(0)

        # 2. DEMOGRAPHICS (Fill with mode or distinct placeholder)
        cat_cols = ['V190_MUNICIPI', 'V191_COMARCA', 'V194_INSTRUCCIO']
        for col in cat_cols:
            if col in df.columns:
                mode_val = df[col].mode()[0] if not df[col].mode().empty else "Unknown"
                df[col] = df[col].fillna(mode_val)

        return self._convert_to_numeric(df)
