import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import random

st.set_page_config(layout="wide")

# -------------------------------
# INDUSTRIAL DARK THEME
# -------------------------------
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .stMetric {
        background-color: #1c1f26;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏭 MOHARADA WTP - SCADA HMI Dashboard")
st.markdown("### Real-Time Monitoring & Control System")

# -------------------------------
# SIMULATION VALUES
# -------------------------------
flow = 684
turbidity = random.randint(8, 25)
chlorine = round(random.uniform(0.3, 1.0), 2)
ugr_level = random.randint(40, 95)
pressure = random.randint(3, 8)

# Alarm Logic
turbidity_alarm = turbidity > 20
chlorine_alarm = chlorine < 0.3 or chlorine > 1.0
level_alarm = ugr_level < 30

# -------------------------------
# LAYOUT
# -------------------------------
col1, col2 = st.columns([3, 1])

# -------------------------------
# PROCESS MIMIC
# -------------------------------
with col1:
    st.image("assets/plant_layout.png", use_column_width=True)
    st.markdown("### 🔄 Plant Running Status")
    st.success("All Pumps Running") if not turbidity_alarm else st.error("Turbidity Alarm Active!")

# -------------------------------
# LIVE PARAMETERS PANEL
# -------------------------------
with col2:
    st.markdown("## 📊 Live Parameters")

    st.metric("Raw Water Flow (m³/hr)", flow)
    st.metric("Pressure (Bar)", pressure)

    if turbidity_alarm:
        st.metric("Turbidity (NTU)", turbidity, "ALARM", delta_color="inverse")
    else:
        st.metric("Turbidity (NTU)", turbidity)

    if chlorine_alarm:
        st.metric("Chlorine (ppm)", chlorine, "CHECK")
    else:
        st.metric("Chlorine (ppm)", chlorine)

    if level_alarm:
        st.metric("UGR Level (%)", ugr_level, "LOW")
    else:
        st.metric("UGR Level (%)", ugr_level)

# -------------------------------
# CONTROL PANEL
# -------------------------------
st.markdown("---")
st.markdown("## 🎛 Control Panel")

col3, col4, col5 = st.columns(3)

with col3:
    if st.button("Start Pumps"):
        st.success("Pumps Started")

with col4:
    if st.button("Stop Pumps"):
        st.warning("Pumps Stopped")

with col5:
    dosing_rate = st.slider("Chemical Dosing Rate (mg/L)", 10, 100, 40)

# -------------------------------
# CHEMICAL OPTIMIZATION LOGIC
# -------------------------------
optimized_dose = turbidity * 2
st.markdown(f"### ⚗ Recommended Coagulant Dose: {optimized_dose} mg/L")

# -------------------------------
# TREND GRAPH
# -------------------------------
st.markdown("---")
st.markdown("## 📈 Process Trend")

time_series = pd.date_range(end=pd.Timestamp.now(), periods=20, freq='T')
turb_series = np.random.randint(8, 25, size=20)

fig = go.Figure()
fig.add_trace(go.Scatter(x=time_series, y=turb_series, mode='lines', name='Turbidity'))
fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# PRODUCTION COUNTER
# -------------------------------
production = flow * 24
st.markdown(f"## 🏗 Total Production (m³/day): {production}")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("SCADA System Developed for Moharada WTP | Industrial Simulation Mode")
