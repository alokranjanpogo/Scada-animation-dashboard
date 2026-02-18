import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random
import os
import time

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Moharada WTP SCADA",
    layout="wide"
)

# -------------------------------------------------
# INDUSTRIAL DARK THEME
# -------------------------------------------------
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .stMetric {
        background-color: #1c1f26;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏭 MOHARADA WTP - SCADA HMI Dashboard")
st.markdown("### Real-Time Monitoring & Control System")

# -------------------------------------------------
# SESSION STATE FOR PUMP STATUS
# -------------------------------------------------
if "pump_running" not in st.session_state:
    st.session_state.pump_running = True

# -------------------------------------------------
# SIMULATED REAL-TIME VALUES
# -------------------------------------------------
flow = 684 if st.session_state.pump_running else 0
pressure = random.randint(4, 8) if st.session_state.pump_running else 0
turbidity = random.randint(8, 25)
chlorine = round(random.uniform(0.2, 1.2), 2)
ugr_level = random.randint(35, 95)

# -------------------------------------------------
# ALARM CONDITIONS
# -------------------------------------------------
turbidity_alarm = turbidity > 20
chlorine_alarm = chlorine < 0.3 or chlorine > 1.0
level_alarm = ugr_level < 30

# -------------------------------------------------
# MAIN LAYOUT
# -------------------------------------------------
col1, col2 = st.columns([3, 1])

# -------------------------------------------------
# PROCESS IMAGE SECTION (SAFE IMAGE LOADING)
# -------------------------------------------------
with col1:
    st.subheader("Process Mimic Diagram")

    if os.path.exists("plant_layout.png"):
        st.image("plant_layout.png", use_container_width=True)
    else:
        st.warning("plant_layout.png not found in project folder.")

    if st.session_state.pump_running:
        st.success("Plant Status: RUNNING")
    else:
        st.error("Plant Status: STOPPED")

# -------------------------------------------------
# LIVE PARAMETER PANEL
# -------------------------------------------------
with col2:
    st.subheader("Live Parameters")

    st.metric("Raw Water Flow (m³/hr)", flow)
    st.metric("Pressure (Bar)", pressure)

    if turbidity_alarm:
        st.metric("Turbidity (NTU)", turbidity, "HIGH")
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

# -------------------------------------------------
# CONTROL PANEL
# -------------------------------------------------
st.markdown("---")
st.subheader("🎛 Control Panel")

col3, col4, col5 = st.columns(3)

with col3:
    if st.button("Start Pumps"):
        st.session_state.pump_running = True

with col4:
    if st.button("Stop Pumps"):
        st.session_state.pump_running = False

with col5:
    dosing_rate = st.slider("Chemical Dosing (mg/L)", 10, 100, 40)

# -------------------------------------------------
# CHEMICAL OPTIMIZATION LOGIC
# -------------------------------------------------
recommended_dose = turbidity * 2
st.markdown(f"### ⚗ Recommended Coagulant Dose: **{recommended_dose} mg/L**")

# -------------------------------------------------
# TREND GRAPH SECTION
# -------------------------------------------------
st.markdown("---")
st.subheader("📈 Turbidity Trend (Last 20 Minutes)")

time_series = pd.date_range(end=pd.Timestamp.now(), periods=20, freq="min")
turb_series = np.random.randint(8, 25, size=20)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=time_series,
    y=turb_series,
    mode='lines',
    name='Turbidity'
))
fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# DAILY PRODUCTION CALCULATION
# -------------------------------------------------
daily_production = flow * 24
st.markdown(f"## 🏗 Total Production: **{daily_production} m³/day**")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.caption("Industrial SCADA Simulation | Moharada Water Treatment Plant")




