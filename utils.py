import pandas as pd
import streamlit as st
import numpy as np

@st.cache_data
def load_data(uploaded_files):
    """
    Loads one or multiple CSV files and combines them into a single DataFrame.
    Safe for Streamlit caching and multi-file uploads.
    """
    try:
        data_frames = []

        # Normalize input
        if not isinstance(uploaded_files, list):
            uploaded_files = [uploaded_files]

        for file in uploaded_files:
            try:
                # 🔥 CRITICAL FIX
                file.seek(0)

                # Skip empty files
                if file.size == 0:
                    st.warning(f"{file.name} is empty and was skipped.")
                    continue

                df_part = pd.read_csv(file, low_memory=False)

                # Skip invalid CSVs
                if df_part.empty or df_part.columns.size == 0:
                    st.warning(f"{file.name} has no usable data and was skipped.")
                    continue

                data_frames.append(df_part)

            except Exception as file_error:
                st.warning(f"Skipping {file.name}: {file_error}")

        if not data_frames:
            st.error("No valid CSV data found in uploaded files.")
            return None

        # Combine all uploaded files
        df = pd.concat(data_frames, ignore_index=True)

        # --- DATA CLEANING & STANDARDIZATION ---

        # 1. Standardize column names
        df.columns = [col.strip().capitalize() for col in df.columns]

        # 2. Date handling
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df['Year'] = df['Date'].dt.year
            df['Month_name'] = df['Date'].dt.month_name()

        # 3. Numeric conversion
        for col in df.columns:
            if any(x in col.lower() for x in ['age', 'count', 'total', 'enrolment', 'bio']):
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        return df

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


def calculate_kpis(df):
    total_records = len(df)
    unique_states = df['State'].nunique() if 'State' in df.columns else 0
    unique_districts = df['District'].nunique() if 'District' in df.columns else 0

    total_updates = 0
    for col in df.select_dtypes(include=['number']).columns:
        if 'bio' in col.lower():
            total_updates += df[col].sum()

    return total_records, unique_states, unique_districts, total_updates


def detect_anomalies(df, metric_col, threshold=2):
    if df is None or df.empty or metric_col not in df.columns:
        return None

    mean = df[metric_col].mean()
    std = df[metric_col].std()

    if std == 0 or np.isnan(std):
        df['Z_Score'] = 0
        df['Is_Anomaly'] = False
        return df

    df['Z_Score'] = (df[metric_col] - mean) / std
    df['Is_Anomaly'] = np.abs(df['Z_Score']) > threshold

    return df
