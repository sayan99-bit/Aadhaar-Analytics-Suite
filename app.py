import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime

# ==========================================
# 1. PAGE CONFIG & THEME
# ==========================================
st.set_page_config(
    page_title="Aadhaar Intel Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'active_view' not in st.session_state:
    st.session_state['active_view'] = 'Overview'

# CSS STYLING (Rajdhani + Inter + Glassmorphism)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Rajdhani:wght@500;700&display=swap');

    /* BASE THEME */
    .stApp {
        background: linear-gradient(-45deg, #050511, #101025, #0a0a1a);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: rgba(5, 5, 17, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* HEADERS */
    h1, h2, h3 { font-family: 'Rajdhani', sans-serif; letter-spacing: 1px; }
    
    /* GLASS CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.2s;
    }
    .glass-card:hover {
        border-color: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }

    /* KPI METRICS */
    .kpi-val { font-family: 'Rajdhani'; font-size: 2rem; font-weight: 700; color: #fff; }
    .kpi-lbl { color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }

    /* CUSTOM UPLOADER */
    .upload-zone {
        border: 2px dashed rgba(118, 75, 162, 0.5);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background: rgba(118, 75, 162, 0.05);
    }
    
    /* ANIMATIONS */
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); }
        100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA LOGIC & HELPER FUNCTIONS
# ==========================================

@st.cache_data
def generate_mock_data():
    """Generates 3 dataframes matching the user's EXACT schema"""
    dates = pd.date_range(start="2025-01-01", periods=30, freq='D')
    states = ['Maharashtra', 'Karnataka', 'Delhi', 'Uttar Pradesh', 'Bihar']
    districts = {
        'Maharashtra': ['Pune', 'Mumbai', 'Nagpur'],
        'Karnataka': ['Bangalore', 'Mysore'],
        'Delhi': ['New Delhi', 'North Delhi'],
        'Uttar Pradesh': ['Lucknow', 'Varanasi'],
        'Bihar': ['Patna', 'Gaya']
    }
    
    enrol_data = []
    demo_data = []
    bio_data = []

    for date in dates:
        for state in states:
            for dist in districts[state]:
                base = {
                    'date': date,
                    'state': state,
                    'district': dist,
                    'pincode': np.random.randint(110001, 800001)
                }
                
                # 1. Enrolment Dataset
                e_row = base.copy()
                e_row['age_0_5'] = np.random.randint(50, 200)
                e_row['age_5_17'] = np.random.randint(100, 500)
                e_row['age_18_greater'] = np.random.randint(500, 2000)
                enrol_data.append(e_row)

                # 2. Demographic Dataset
                d_row = base.copy()
                d_row['demo_age_5_17'] = np.random.randint(10, 50)
                d_row['demo_age_17_'] = np.random.randint(20, 100)
                demo_data.append(d_row)

                # 3. Biometric Dataset
                b_row = base.copy()
                b_row['bio_age_5_17'] = np.random.randint(20, 150) # Mandatory updates
                b_row['bio_age_17_'] = np.random.randint(50, 300)
                bio_data.append(b_row)

    return pd.DataFrame(enrol_data), pd.DataFrame(demo_data), pd.DataFrame(bio_data)

def normalize_columns(df):
    """
    Cleans column names to a standard format:
    - Lowercase
    - Strip whitespace
    - Replace spaces and hyphens with underscores
    """
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')
    return df

def identify_dataset(df):
    """
    Auto-detects dataset type based on fuzzy matching of keywords in columns.
    Returns: 'enrolment', 'demographic', 'biometric', or 'unknown'
    """
    cols = set(df.columns)
    
    # Check for keywords specific to each dataset type
    if any(c in cols for c in ['age_0_5', 'age_0_to_5', 'enrolment']):
        return 'enrolment'
    elif any(c in cols for c in ['demo_age_5_17', 'demographic', 'demo_update']):
        return 'demographic'
    elif any(c in cols for c in ['bio_age_5_17', 'biometric', 'bio_update']):
        return 'biometric'
    
    return 'unknown'

def process_data(uploaded_files):
    data_map = {}
    
    if uploaded_files:
        for file in uploaded_files:
            try:
                df = pd.read_csv(file)
                
                # 1. Normalize Column Names (Fixes capitalization/spacing issues)
                df = normalize_columns(df)
                
                # 2. Robust Date Parsing
                if 'date' in df.columns:
                    # dayfirst=True handles 13-09-2025 correctly
                    # errors='coerce' prevents crashes on bad data
                    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
                
                # 3. Identify Type
                dtype = identify_dataset(df)
                
                if dtype != 'unknown':
                    data_map[dtype] = df
                else:
                    st.warning(f"Could not identify file type for: {file.name}. Please check column headers.")
                    
            except Exception as e:
                st.error(f"Error processing file {file.name}: {e}")
    
    return data_map

# ==========================================
# 3. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="font-size: 2rem;">🛡️</div>
        <h2 style="font-family: 'Rajdhani'; color: white;">AADHAAR<br><span style="font-size: 0.8em; color: #94a3b8;">INTEL SUITE</span></h2>
    </div>
    """, unsafe_allow_html=True)

    # File Uploader
    st.markdown('<div class="upload-zone">📥 <strong>Data Ingestion</strong><br><span style="font-size:0.8rem">Drop Enrolment, Demo, or Bio CSVs</span></div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("", accept_multiple_files=True, label_visibility="collapsed")
    
    # Mock Data Button
    use_mock = st.checkbox("Use Mock Data Generator", value=False)

    st.markdown("---")
    
    # Navigation
    if st.button("📊 Overview & Trends", use_container_width=True): st.session_state['active_view'] = 'Overview'
    if st.button("👥 Demographics", use_container_width=True): st.session_state['active_view'] = 'Demographics'
    if st.button("🧬 Biometric Health", use_container_width=True): st.session_state['active_view'] = 'Biometrics'

# ==========================================
# 4. DATA LOADING
# ==========================================
dfs = {}

if use_mock:
    e_df, d_df, b_df = generate_mock_data()
    dfs['enrolment'] = e_df
    dfs['demographic'] = d_df
    dfs['biometric'] = b_df
    st.toast("Generated Synthetic Aadhaar Data", icon="🤖")
elif uploaded_files:
    dfs = process_data(uploaded_files)
    if dfs:
        st.toast(f"Loaded {len(dfs)} Datasets Successfully", icon="✅")

# ==========================================
# 5. MAIN DASHBOARD
# ==========================================

# HEADER
timestamp = datetime.datetime.now().strftime("%d %b %Y • %H:%M")
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
    <div>
        <h1 style="margin:0; font-family:'Rajdhani'; font-size: 2.5rem;">INTELLIGENCE <span style="color:#667eea">HUB</span></h1>
        <div style="color:#94a3b8; letter-spacing:1px;">NATIONAL BIOMETRIC OPERATIONS CENTER</div>
    </div>
    <div style="text-align:right;">
        <div style="color:#22c55e; font-weight:bold; letter-spacing:1px;">● SYSTEM ONLINE</div>
        <div style="color:#64748b; font-size:0.9rem;">{timestamp}</div>
    </div>
</div>
""", unsafe_allow_html=True)

if not dfs:
    # --- EMPTY STATE (FIXED CSS FORMAT) ---
    st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 60vh; text-align: center; background: radial-gradient(circle at center, rgba(118, 75, 162, 0.15) 0%, rgba(5, 5, 17, 0) 70%); border-radius: 30px; position: relative; overflow: hidden;">
    <div style="position: absolute; width: 100%; height: 100%; background-image: linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px); background-size: 50px 50px; z-index: 0; pointer-events: none;"></div>
    <div style="z-index: 1; position: relative;">
        <div style="font-size: 5rem; margin-bottom: 25px; text-shadow: 0 0 30px rgba(118, 75, 162, 0.6); animation: pulse-glow 3s infinite;">🔐</div>
        <h1 style="color: #fff; font-family: 'Rajdhani'; font-size: 3.5rem; letter-spacing: 4px; margin-bottom: 10px;">SECURE DATA GATEWAY</h1>
        <p style="color: #94a3b8; font-size: 1.2rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">
            Awaiting encrypted data stream. <br>
            Please initiate the handshake via the <strong style="color: #764ba2;">Data Ingestion</strong> panel.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

else:
    # --- GLOBAL FILTER ---
    # We use the first available dataframe to populate the state filter
    first_key = list(dfs.keys())[0]
    states = ['All India'] + sorted(list(dfs[first_key]['state'].unique()))
    selected_state = st.selectbox("🌍 Select Region", states)
    
    # Apply Filters to ALL datasets
    filtered_dfs = {}
    for key, df in dfs.items():
        if selected_state != 'All India':
            filtered_dfs[key] = df[df['state'] == selected_state]
        else:
            filtered_dfs[key] = df

    # --- VIEW: OVERVIEW ---
    if st.session_state['active_view'] == 'Overview':
        
        # 1. KPI SECTION
        k1, k2, k3, k4 = st.columns(4)
        
        total_enrol = 0
        total_bio = 0
        mig_flag = 0
        dist_count = 0
        
        if 'enrolment' in filtered_dfs:
            e_data = filtered_dfs['enrolment']
            # Sum up all age buckets
            # Note: Using 'get' to handle normalized column names safely
            c_0_5 = e_data.get('age_0_5', pd.Series(0)).sum()
            c_5_17 = e_data.get('age_5_17', pd.Series(0)).sum()
            c_18_plus = e_data.get('age_18_greater', pd.Series(0)).sum()
            
            total_enrol = c_0_5 + c_5_17 + c_18_plus
            mig_flag = c_18_plus
            dist_count = len(e_data['district'].unique())
            
        if 'biometric' in filtered_dfs:
            b_data = filtered_dfs['biometric']
            c_bio_5_17 = b_data.get('bio_age_5_17', pd.Series(0)).sum()
            c_bio_17_plus = b_data.get('bio_age_17_', pd.Series(0)).sum()
            total_bio = c_bio_5_17 + c_bio_17_plus

        with k1:
            st.markdown(f"<div class='glass-card'><div class='kpi-lbl'>Total Activity</div><div class='kpi-val'>{total_enrol:,}</div></div>", unsafe_allow_html=True)
        with k2:
            st.markdown(f"<div class='glass-card'><div class='kpi-lbl'>Biometric Updates</div><div class='kpi-val' style='color:#3b82f6'>{total_bio:,}</div></div>", unsafe_allow_html=True)
        with k3:
            st.markdown(f"<div class='glass-card'><div class='kpi-lbl'>Working Age (Migrant Proxy)</div><div class='kpi-val' style='color:#f97316'>{mig_flag:,}</div></div>", unsafe_allow_html=True)
        with k4:
             st.markdown(f"<div class='glass-card'><div class='kpi-lbl'>Active Districts</div><div class='kpi-val' style='color:#22c55e'>{dist_count}</div></div>", unsafe_allow_html=True)

        st.markdown("### 📈 Enrolment & Saturation Trends")
        
        if 'enrolment' in filtered_dfs:
            e_data = filtered_dfs['enrolment']
            
            # Ensure columns exist before plotting
            available_cols = [c for c in ['age_0_5', 'age_5_17', 'age_18_greater'] if c in e_data.columns]
            
            if available_cols and 'date' in e_data.columns:
                daily = e_data.groupby('date')[available_cols].sum().reset_index()
                
                fig = px.area(daily, x='date', y=available_cols,
                              color_discrete_sequence=['#22c55e', '#3b82f6', '#f97316'],
                              labels={'value': 'Enrolments', 'variable': 'Age Group'})
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#cbd5e1')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Date or Age columns missing in Enrolment data.")
            
            # Child Saturation Map (District Wise)
            if 'age_0_5' in e_data.columns:
                st.markdown("### 👶 Child Enrolment Saturation (Age 0-5)")
                dist_data = e_data.groupby('district')['age_0_5'].sum().reset_index().sort_values('age_0_5', ascending=False)
                
                fig2 = px.bar(dist_data, x='district', y='age_0_5', color='age_0_5',
                              color_continuous_scale='viridis')
                fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#cbd5e1')
                st.plotly_chart(fig2, use_container_width=True)

    # --- VIEW: DEMOGRAPHICS ---
    elif st.session_state['active_view'] == 'Demographics':
        st.markdown("### 👥 Population Split & Gaps")
        
        c1, c2 = st.columns([2, 1])
        
        with c1:
            if 'enrolment' in filtered_dfs:
                e_data = filtered_dfs['enrolment']
                
                # Check for columns safely
                cols_to_sum = [c for c in ['age_0_5', 'age_5_17', 'age_18_greater'] if c in e_data.columns]
                
                if cols_to_sum:
                    sums = e_data[cols_to_sum].sum().reset_index()
                    sums.columns = ['Age Group', 'Count']
                    
                    fig = px.pie(sums, values='Count', names='Age Group', hole=0.6,
                                 color_discrete_sequence=px.colors.sequential.RdBu,
                                 title="Overall Age Distribution")
                    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#cbd5e1')
                    st.plotly_chart(fig, use_container_width=True)
        
        with c2:
            st.markdown(f"""
            <div class='glass-card' style='height: 100%; border-left: 4px solid #f97316'>
                <h4 style="color:#f97316">💡 Demographic Insight</h4>
                <p style="color:#94a3b8; font-size:0.9rem">
                    The distribution shows the active enrolment base.
                    <br><br>
                    <strong>Action:</strong> If Age 0-5 slice is low, prioritize Anganwadi camps.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        if 'demographic' in filtered_dfs:
            st.markdown("### 📉 Demographic Updates (Corrections)")
            d_data = filtered_dfs['demographic']
            
            d_cols = [c for c in ['demo_age_5_17', 'demo_age_17_'] if c in d_data.columns]
            
            if d_cols:
                d_sums = d_data[d_cols].sum().reset_index()
                d_sums.columns = ['Category', 'Updates']
                
                fig3 = px.bar(d_sums, x='Category', y='Updates', color='Category', color_discrete_sequence=['#ef4444', '#f59e0b'])
                fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#cbd5e1')
                st.plotly_chart(fig3, use_container_width=True)

    # --- VIEW: BIOMETRICS ---
    elif st.session_state['active_view'] == 'Biometrics':
        st.markdown("### 🧬 Biometric Compliance & Anomalies")
        
        if 'biometric' in filtered_dfs:
            b_data = filtered_dfs['biometric']
            
            # 1. Mandatory Updates Trend
            if 'bio_age_5_17' in b_data.columns and 'date' in b_data.columns:
                daily_bio = b_data.groupby('date')['bio_age_5_17'].sum().reset_index()
                
                fig = px.line(daily_bio, x='date', y='bio_age_5_17', markers=True, 
                              title="Mandatory Biometric Updates (Age 5-17)",
                              line_shape='spline')
                fig.update_traces(line_color='#8b5cf6', line_width=3)
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#cbd5e1')
                st.plotly_chart(fig, use_container_width=True)
            
            # 2. Anomaly Detection (Z-Score)
            if 'bio_age_17_' in b_data.columns:
                st.markdown("### ⚠️ District Anomaly Detection")
                
                district_risk = b_data.groupby('district')['bio_age_17_'].sum().reset_index()
                district_risk['z_score'] = (district_risk['bio_age_17_'] - district_risk['bio_age_17_'].mean()) / district_risk['bio_age_17_'].std()
                anomalies = district_risk[district_risk['z_score'] > 1.5] # Threshold
                
                c1, c2 = st.columns([3, 1])
                
                with c1:
                    fig_risk = px.scatter(district_risk, x='district', y='bio_age_17_', 
                                          color='z_score', size='bio_age_17_',
                                          color_continuous_scale='reds',
                                          title="Risk Heatmap: Unusual Adult Bio Updates")
                    fig_risk.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#cbd5e1')
                    st.plotly_chart(fig_risk, use_container_width=True)
                    
                with c2:
                    if not anomalies.empty:
                        st.markdown(f"""
                        <div style="background: rgba(239, 68, 68, 0.2); padding: 15px; border-radius: 10px; border: 1px solid #ef4444;">
                            <strong style="color:#ef4444">🚨 ALERTS ({len(anomalies)})</strong><br>
                            <span style="font-size:0.8rem">Districts with abnormal update spikes:</span>
                            <ul style="font-size:0.8rem; margin-top:5px; padding-left:20px;">
                                {''.join([f"<li>{d} (Z: {z:.1f})</li>" for d, z in zip(anomalies['district'], anomalies['z_score'])])}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.success("No anomalies detected in current stream.")
        else:
            st.info("Please upload Biometric Dataset to view this module.")