import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random
import time

st.set_page_config(layout="wide")

# -------------------------
# INDUSTRIAL THEME
# -------------------------
st.markdown("""
<style>
body {background-color: #0E1117; color: white;}
.big-font {font-size:22px !important;}
.green {color: #00FF00;}
.red {color: #FF4B4B;}
.bluepipe {color: #00BFFF;}
</style>
""", unsafe_allow_html=True)

st.title("🏭 MOHARADA WTP - SCADA HMI")

# -------------------------
# SESSION STATE
# -------------------------
if "pump" not in st.session_state:
    st.session_state.pump = True

# -------------------------
# SIMULATION VALUES
# -------------------------
flow = 684 if st.session_state.pump else 0
pressure = random.randint(4,8) if st.session_state.pump else 0
turbidity = random.randint(8,25)
chlorine = round(random.uniform(0.2,1.2),2)
tank_level = random.randint(30,95)

turb_alarm = turbidity > 20
chlor_alarm = chlorine < 0.3 or chlorine > 1.0

# -------------------------
# SCADA MIMIC SECTION
# -------------------------
st.markdown("## 🖥 Process Mimic")

col1, col2, col3, col4 = st.columns(4)

# Intake Pump
with col1:
    st.markdown("### Intake Pump")
    if st.session_state.pump:
        st.markdown("<h3 class='green'>● RUNNING</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 class='red'>● STOPPED</h3>", unsafe_allow_html=True)
    st.metric("Flow (m³/hr)", flow)

# Clarifier Tank
with col2:
    st.markdown("### Clarifier")
    st.progress(tank_level)
    if turb_alarm:
        st.markdown("<h4 class='red'>⚠ High Turbidity</h4>", unsafe_allow_html=True)
    st.metric("Turbidity (NTU)", turbidity)

# Filter Unit
with col3:
    st.markdown("### Filter Bed")
    st.markdown("<span class='bluepipe'>══════ Flowing Water ══════></span>", unsafe_allow_html=True)
    st.metric("Pressure (Bar)", pressure)

# Chlorination
with col4:
    st.markdown("### Chlorination")
    if chlor_alarm:
        st.markdown("<h4 class='red'>⚠ Chlorine Out of Range</h4>", unsafe_allow_html=True)
    st.metric("Chlorine (ppm)", chlorine)

# -------------------------
# CONTROL PANEL
# -------------------------
st.markdown("---")
st.markdown("## 🎛 Control Panel")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Start Plant"):
        st.session_state.pump = True

with c2:
    if st.button("Stop Plant"):
        st.session_state.pump = False

with c3:
    dosing = st.slider("Chemical Dosing (mg/L)", 10, 100, 40)

recommended_dose = turbidity * 2
st.markdown(f"### ⚗ Recommended Dose: **{recommended_dose} mg/L**")

# -------------------------
# TREND GRAPH
# -------------------------
st.markdown("---")
st.markdown("## 📈 Turbidity Trend")

time_series = pd.date_range(end=pd.Timestamp.now(), periods=20, freq="min")
values = np.random.randint(8,25,size=20)

fig = go.Figure()
fig.add_trace(go.Scatter(x=time_series, y=values, mode='lines'))
fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# DAILY PRODUCTION
# -------------------------
daily = flow * 24
st.markdown(f"## 🏗 Total Production: **{daily} m³/day**")

st.markdown("---")
st.caption("Industrial SCADA Simulation - Moharada WTP")

       

