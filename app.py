# ==============================
# AI WORM DETECTION + RISK SYSTEM
# ==============================

import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import plotly.graph_objects as go
import plotly.express as px
# ==============================
# LOAD MODEL
# ==============================

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("worm_detector.h5")

model = load_model()

# ==============================
# IMAGE PROCESSING
# ==============================

def preprocess_image(img):
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0

    if img_array.shape[-1] == 4:
        img_array = img_array[:, :, :3]

    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def predict_worm_presence(img, model):
    processed = preprocess_image(img)
    pred = model.predict(processed)[0][0]
    return float(pred) # 0–1


# ==============================
# ENGINEERING RISK MODEL
# ==============================

def calculate_engineering_risk(frc, turbidity, temp, velocity, water_age):

    frc_risk = max(0, 0.2 - frc) * 40
    velocity_risk = max(0, 0.3 - velocity) * 30
    temp_risk = max(0, temp - 25) * 1.5
    turbidity_risk = turbidity * 2
    age_risk = water_age * 3

    total_risk = frc_risk + velocity_risk + temp_risk + turbidity_risk + age_risk

    return min(100, total_risk)


# ==============================
# FUSION MODEL
# ==============================

def final_risk_score(image_score, engineering_score):

    final_score = (0.6 * image_score * 100) + (0.4 * engineering_score)

    return min(100, final_score)


# ==============================
# SMART ACTION ENGINE
# ==============================

def generate_actions(image_score, frc, velocity, temp, turbidity, water_age):

    actions = []

    if image_score > 0.7:
        actions.append("🚨 Worms detected → Immediate flushing required")
        actions.append("🚨 Shock chlorination recommended")

    if frc < 0.2:
        actions.append("Increase chlorine dosing")
    else:
        actions.append("FRC OK → Issue may be biofilm or stagnation")

    if velocity < 0.2:
        actions.append("Low velocity zone → Flush pipeline")

    if temp > 30:
        actions.append("High temperature → Biological growth risk")

    if turbidity > 3:
        actions.append("High turbidity → Improve treatment efficiency")

    if water_age > 6:
        actions.append("High water age → Reduce stagnation")

    if image_score > 0.5 and frc >= 0.2:
        actions.append("⚠️ Worms present despite chlorine → Biofilm protection likely")

    return actions


# ==============================
# STREAMLIT UI
# ==============================

st.set_page_config(page_title="AI Worm Detection System", layout="wide")

st.title("🚀 AI-Based Worm Detection & Distribution Risk System")

col1, col2 = st.columns(2)

# ==============================
# IMAGE INPUT
# ==============================

with col1:
    st.subheader("📸 Upload Net / Raw Water Image")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

# ==============================
# PARAMETER INPUT
# ==============================

with col2:
    st.subheader("⚙️ System Parameters")

    frc = st.slider("Residual Chlorine (mg/L)", 0.0, 1.0, 0.3)
    turbidity = st.slider("Turbidity (NTU)", 0.0, 10.0, 2.0)
    temp = st.slider("Temperature (°C)", 20, 40, 30)
    velocity = st.slider("Flow Velocity (m/s)", 0.0, 1.0, 0.3)
    water_age = st.slider("Water Age (hours)", 0, 24, 4)

# ==============================
# ANALYSIS BUTTON
# ==============================

if st.button("🔍 Analyze System"):

    if uploaded_file is None:
        st.warning("Please upload an image first")
    else:

        # Image prediction
        image_score = predict_worm_presence(image, model)

        # Engineering risk
        eng_score = calculate_engineering_risk(
            frc, turbidity, temp, velocity, water_age
        )

        # Final score
        final_score = final_risk_score(image_score, eng_score)

        # ==============================
        # STATUS DISPLAY
        # ==============================

        st.subheader("📊 System Status")

        if final_score > 70:
            st.error(f"🚨 HIGH RISK ({round(final_score,2)})")
        elif final_score > 40:
            st.warning(f"⚠️ MODERATE RISK ({round(final_score,2)})")
        else:
            st.success(f"✅ SAFE ({round(final_score,2)})")

        # ==============================
        # DETAILED OUTPUT
        # ==============================

        st.subheader("🔎 Detailed Analysis")

        st.write(f"Image Worm Probability: {round(image_score*100,2)} %")
        st.write(f"Engineering Risk Score: {round(eng_score,2)}")
        st.write(f"Final Risk Score: {round(final_score,2)}")

        # ==============================
        # ACTIONS
        # ==============================

        st.subheader("🛠 Recommended Actions")

        actions = generate_actions(
            image_score, frc, velocity, temp, turbidity, water_age
        )

        for act in actions:
            st.write("•", act)


# ==============================
# FOOTER (FOR PROFESSIONAL TOUCH)
# ==============================

st.markdown("---")
st.caption("AI + Engineering Hybrid Model for Worm Risk Prediction in Water Distribution System")
# ===============================
# 🤖 AI FEEDBACK + WEATHER GRAPH
# ===============================

import streamlit as st
import smtplib
import time

st.markdown("## 🤖 AI Feedback & Learning System")

left_col, right_col = st.columns([2,1])

# ===============================
# 📧 EMAIL FUNCTION
# ===============================

def send_email_alert(message):
    sender = "alokranjan18april@gmail.com"
    password = "wpnrabqfbtkhsqpe"
    receiver = "alok.ranjan6@tatasteel.com"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)

        # 👇 IMPORTANT FIX
        server.sendmail(sender, receiver, message.encode('utf-8'))

        server.quit()
        st.success("MAIL SENT SUCCESSFULLY ✅")

    except Exception as e:
        st.error(f"Email error: {e}")

# ===============================
# ⏱ COOLDOWN SYSTEM
# ===============================
if "last_alert_time" not in st.session_state:
    st.session_state.last_alert_time = 0

ALERT_COOLDOWN = 300   # 5 min

# ===============================
# LEFT SIDE → YOUR EXISTING CODE
# ===============================
with left_col:
    
    col1, col2 = st.columns(2)

    with col1:
        dose = st.slider("Dose Applied (mg/L)", 0.0, 100.0, 10.0)
        final_turbidity = st.number_input("Final Turbidity (NTU)", 0.0, 50.0, 1.0)
        frc = st.number_input("Final Residual Chlorine (mg/L)", 0.0, 5.0, 0.5)

    with col2:
        raw_turbidity = st.number_input("Raw Water Turbidity (NTU)", 0.0, 500.0, 50.0)

    submit = st.button("Submit Feedback")

    # ===============================
    # 🤖 AI LOGIC + EMAIL ALERT
    # ===============================
    if submit:

        # Example logic (you can replace with your AI model)
        performance_index = 100 - (final_turbidity * 20)

        st.write(f"Performance Index: {performance_index:.2f}")

        # 🚨 CONDITION
        if final_turbidity > 1 or frc < 0.2:

            current_time = time.time()

            if current_time - st.session_state.last_alert_time > ALERT_COOLDOWN:

                message = f"""Subject:Water Quality Alert

Turbidity: {final_turbidity} NTU
FRC: {frc} mg/L

Immediate attention required!
"""

                send_email_alert(message)

                st.session_state.last_alert_time = current_time

                st.error("🚨 Email Alert Sent!")

            else:
                st.warning("⏳ Alert already sent recently")

        else:
            st.success("✅ System Normal")

# ===============================
# RIGHT SIDE → WEATHER GRAPH
# ===============================
with right_col:
    st.markdown("### 🌦 Live Weather")
    pass

# ==========================================
# 🖥️ WATER QUALITY AI - ADVANCED PRACTICAL VERSION
# Added: Pre-Chlorination + Oily Water Logic
# ==========================================

import streamlit as st

st.title("🖥️ Water Treatment AI Assistant")

# ===============================
# STEP 1: COMPLAINT
# ===============================
st.subheader("Step 1: Customer Complaint")

complaint = st.text_input("Enter issue (muddy, smell, worms, yellow, green layer)")

# ===============================
# STEP 2: WATER PARAMETERS
# ===============================
if complaint:

    st.subheader("Step 2: Plant Data")

    col1, col2 = st.columns(2)

    with col1:
        raw_turbidity = st.number_input("Raw Water Turbidity (NTU)", value=80.0)
        treated_turbidity = st.number_input("Treated Water Turbidity (NTU)", value=1.2)

    with col2:
        chlorine = st.number_input("Residual Chlorine (ppm)", value=0.3)
        sunlight = st.selectbox("Is storage exposed to sunlight?", ["Yes", "No"])

# ===============================
# STEP 3: DOSING + CONDITIONS
# ===============================
    st.subheader("Step 3: Chemical Dosing")

    col3, col4 = st.columns(2)

    with col3:
        alum = st.number_input("Alum Dose (ppm)", value=25.0)
        pre_chlorine = st.number_input("Pre-Chlorination Dose (ppm)", value=0.5)

    with col4:
        hypo = st.number_input("Post-Chlorination (Hypo) Dose (ppm)", value=1.0)
        oily = st.selectbox("Is oily layer observed in raw water?", ["No", "Yes"])

# ===============================
# FINAL ANALYSIS
# ===============================
    if st.button("Run Diagnosis"):

        st.subheader("🧠 Diagnosis & Action")

        text = complaint.lower()

        # -------------------------------
        # 🧪 PRE-CHLORINATION CHECK
        # -------------------------------
        st.markdown("### 🧪 Pre-Chlorination Status")

        if pre_chlorine < 0.3:
            st.warning("⚠️ Low Pre-Chlorination")

            st.write("Impact:")
            st.write("- Poor algae control")
            st.write("- Biological load entering clarifier")

            st.write("Action:")
            st.write("- Increase pre-chlorine (0.5–1 ppm typical)")
            st.write("- Reduces coagulant demand")

        elif pre_chlorine > 2:
            st.warning("⚠️ Excess Pre-Chlorination")

            st.write("Impact:")
            st.write("- Formation of chlorinated organics")
            st.write("- Taste & odor problems")

            st.write("Action:")
            st.write("- Optimize dosing (jar test / breakpoint chlorination)")

        else:
            st.success("Pre-chlorination is in optimal range")

        # -------------------------------
        # 🛢️ OILY WATER CHECK
        # -------------------------------
        if oily == "Yes":

            st.error("🛢️ Issue: Oil/Grease contamination")

            st.write("Cause:")
            st.write("- Industrial discharge / runoff")

            st.write("Impact:")
            st.write("- Poor coagulation")
            st.write("- Filter choking")
            st.write("- Odor issues")

            st.write("Action:")
            st.write("- Use oil skimmer / trap before treatment")
            st.write("- Increase coagulant dose slightly")
            st.write("- Use PAC/polymer")
            st.write("- Avoid direct chlorination before oil removal")

        # -------------------------------
        # 🟤 MUDDY / SEDIMENT
        # -------------------------------
        if "muddy" in text or "sediment" in text:

            if treated_turbidity > 1:
                st.error("Issue: Poor clarification / filtration")

                st.write("Possible reasons:")
                if raw_turbidity > 100:
                    st.write("- High river turbidity (seasonal load)")
                if alum < 20:
                    st.write("- Insufficient alum dosing")
                if oily == "Yes":
                    st.write("- Oil interfering with coagulation")

                st.write("Action:")
                st.write("- Increase alum dose (jar test)")
                st.write("- Check floc formation")
                st.write("- Backwash filter")

        # -------------------------------
        # 🪱 WORMS
        # -------------------------------
        elif "worm" in text:

            st.error("Issue: Biological growth in filter/sump")

            st.write("Cause:")
            st.write("- Organic sludge accumulation")
            st.write("- Infrequent backwashing")

            st.write("Action:")
            st.write("- Increase backwash frequency")
            st.write("- Shock chlorination")
            st.write("- Cover tanks")

        # -------------------------------
        # 🌫️ SMELL
        # -------------------------------
        elif "smell" in text or "fish" in text:

            if chlorine > 0.5:
                st.warning("Likely Cause: Over chlorination")

                st.write("Action:")
                st.write("- Reduce hypo dose")

            elif chlorine < 0.2:
                st.warning("Likely Cause: Organic contamination")

                st.write("Action:")
                st.write("- Increase chlorination")
                st.write("- Improve aeration")

            else:
                st.warning("Likely Cause: Chloramines / algae")

                st.write("Action:")
                st.write("- Improve clarification")
                st.write("- Consider PAC dosing")

        # -------------------------------
        # 🟢 GREEN LAYER
        # -------------------------------
        elif "green" in text:

            st.error("Issue: Algae growth")

            if sunlight == "Yes":
                st.write("- Sunlight exposure present")
            if chlorine < 0.2:
                st.write("- Low chlorine")

            st.write("Action:")
            st.write("- Cover tank")
            st.write("- Maintain chlorine 0.2–0.5 ppm")

        # -------------------------------
        # 🟡 YELLOW
        # -------------------------------
        elif "yellow" in text:

            if chlorine > 0.5:
                st.error("Cause: Excess chlorine")

                st.write("Action:")
                st.write("- Reduce dosing")

            elif chlorine < 0.2:
                st.warning("Cause: Biological activity")

                st.write("Action:")
                st.write("- Increase chlorine")

            else:
                st.info("Possible iron presence")

                st.write("Action:")
                st.write("- Improve aeration & filtration")

        # -------------------------------
        # DEFAULT
        # -------------------------------
        else:
            st.info("No clear issue. Check full parameters.")

        # ===============================
        # 📊 STANDARD CHECK
        # ===============================
        st.markdown("---")
        st.subheader("Standards Check (BIS/WHO)")

        if treated_turbidity <= 1:
            st.success("Turbidity OK")
        else:
            st.error("Turbidity High")

        if 0.2 <= chlorine <= 0.5:
            st.success("Chlorine OK")
        else:
            st.error("Chlorine Out of Range")
import streamlit as st
import smtplib
import pandas as pd
import os
import numpy as np
import requests
from datetime import datetime
from sklearn.linear_model import LinearRegression

# ===============================
# PAGE
# ===============================
st.set_page_config(layout="wide")
st.markdown("## 🤖 AI Water Treatment Feedback System")

left_col, right_col = st.columns([2,1])

# ===============================
# EMAIL FUNCTION (FINAL FIXED)
# ===============================
def send_email_alert(message):

    sender = "alokranjan18april@gmail.com"
    password = "wpnrabqfbtkhsqpe"
    receiver = "alok.ranjan6@tatasteel.com"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, message.encode("utf-8"))
        server.quit()

        st.success("📧 Email Sent")

    except Exception as e:
        st.error(f"Email error: {e}")

# ===============================
# ALARM STATE
# ===============================
if "alarm" not in st.session_state:
    st.session_state.alarm = False

# ===============================
# DATA
# ===============================
FILE = "feedback_data.csv"

if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=[
        "timestamp","raw_turbidity","dose","final_turbidity","frc"
    ])

# ===============================
# INPUT
# ===============================
with left_col:

    c1, c2 = st.columns(2)

    with c1:
        dose = st.slider("Dose (mg/L)", 0.0, 100.0, 10.0)
        final_turbidity = st.number_input("Final Turbidity", 0.0, 50.0, 1.0)
        frc = st.number_input("FRC", 0.0, 5.0, 0.5)

    with c2:
        raw_turbidity = st.number_input("Raw Turbidity", 0.0, 500.0, 50.0)

    submit = st.button("Submit Feedback", key="submit_btn")

# ===============================
# MAIN
# ===============================
if submit:

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new = pd.DataFrame([{
        "timestamp": now,
        "raw_turbidity": raw_turbidity,
        "dose": dose,
        "final_turbidity": final_turbidity,
        "frc": frc
    }])

    df = pd.concat([df, new], ignore_index=True)
    df.to_csv(FILE, index=False)

    st.success(f"Saved at {now}")
    st.info(f"Total Samples: {len(df)}")

    # ===============================
    # AI LOGIC
    # ===============================
    if len(df) >= 30:

        st.markdown("### 🤖 AI Smart Recommendation")

        good = df[
            (df["final_turbidity"] <= 1) &
            (df["frc"] >= 0.2) &
            (df["frc"] <= 1)
        ]

        if len(good) > 10:

            good = good.copy()
            good["diff"] = abs(good["raw_turbidity"] - raw_turbidity)

            similar = good.sort_values(by="diff").head(10)
            best = similar["dose"].mean()

            st.success(f"Recommended Dose: {best:.2f} mg/L")

        else:
            st.warning("Collect more good data")

    else:
        st.info(f"AI activates after 30 samples (Current: {len(df)})")

    # ===============================
    # 🚨 ALERT + EMAIL
    # ===============================
    if final_turbidity > 1 or frc < 0.2:

        st.session_state.alarm = True

        msg = f"""Subject: 🚨 WATER QUALITY ALERT

Time: {now}
Final Turbidity: {final_turbidity}
FRC: {frc}

Immediate action required.
"""

        send_email_alert(msg)

    else:
        st.success("Quality Achieved")

# ===============================
# 🔊 FINAL WORKING ALARM (EMBEDDED SOUND)
# ===============================

import base64

# One-time enable
if "sound_enabled" not in st.session_state:
    st.session_state.sound_enabled = False

if not st.session_state.sound_enabled:
    if st.button("🔊 Enable Alarm Sound", key="enable_sound"):
        st.session_state.sound_enabled = True
        st.success("Sound Enabled ✅")

# Alarm
if st.session_state.alarm:

    st.error("🚨 CONTINUOUS ALARM ACTIVE")

    # 🔴 Flashing UI
    st.markdown("""
    <style>
    @keyframes blink {
        0% { background-color: red; }
        50% { background-color: transparent; }
        100% { background-color: red; }
    }
    .alarm-box {
        animation: blink 1s infinite;
        padding: 20px;
        text-align: center;
        font-size: 26px;
        color: white;
        font-weight: bold;
    }
    </style>
    <div class="alarm-box">🚨 CRITICAL WATER QUALITY ALERT 🚨</div>
    """, unsafe_allow_html=True)

    # 🔊 SOUND (EMBEDDED + LOOP)
    if st.session_state.sound_enabled:
        try:
            with open("mixkit-sport-start-bleeps-918.wav", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()

            st.markdown(f"""
            <audio autoplay loop>
                <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.warning(f"⚠️ Sound issue: {e}")

    else:
        st.warning("🔊 Enable sound once")

    # Stop
    if st.button("🔴 Stop Alarm", key="stop_alarm_btn"):
        st.session_state.alarm = False
        st.success("Alarm Stopped")
# ===============================
# 📂 DATA TABLE + DELETE
# ===============================
st.markdown("### 📂 Stored Data")

if st.checkbox("Show Data Table"):

    if len(df) > 0:

        st.dataframe(df.sort_values(by="timestamp", ascending=False))

        selected_index = st.selectbox("Select row to delete", df.index)

        if st.button("🗑 Delete Selected Row", key="delete_btn"):

            df = df.drop(selected_index).reset_index(drop=True)
            df.to_csv(FILE, index=False)

            st.success("Row deleted!")
            st.rerun()

# ===============================
# WEATHER
# ===============================
with right_col:

    st.markdown("### 🌤 Weather")

    API_KEY = "f899db331049be78181d1afddbc92935"
    CITY = "Jamshedpur"

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        st.metric("Temp", f"{data['main']['temp']} °C")
        st.metric("Humidity", f"{data['main']['humidity']} %")
        st.write(data['weather'][0]['description'])

    except:
        st.error("Weather error")
# ============================================================
# IMPORTS (KEEP AT TOP OF FILE)
# ============================================================

import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# 🧠 INTELLIGENT ALUM DOSING SYSTEM
# ============================================================

st.subheader("🧠 Intelligent Alum Dosing Decision System")

# ============================================================
# SAFE TURBIDITY INPUT (USES YOUR EXISTING SLIDER)
# ============================================================

try:
    turbidity = float(intake_turb)
except:
    turbidity = st.slider("Raw Water Turbidity (NTU)", 0.0, 500.0, 50.0)

# ============================================================
# OTHER INPUTS
# ============================================================

flow_mld = 18
flow_m3_day = flow_mld * 1000

ph = st.slider("pH", 4.5, 9.0, 7.0, 0.1)

industrial = st.toggle("⚠️ Industrial Discharge Present")

# ============================================================
# 🧪 JAR TEST INPUT
# ============================================================

st.markdown("### 🧪 Jar Test Input")

jar_available = st.toggle("Use Jar Test")

if jar_available:
    jar_dose = st.number_input("Enter Jar Test Dose (mg/L)", value=25.0)
else:
    jar_dose = None

# ============================================================
# STANDARD MODELS (ENGINEERING BASED)
# ============================================================

def cpheeo_model(t):
    return 0.35*t + 5

def awwa_model(t):
    return 0.40*t + 8

def bis_model(t):
    return 0.30*t + 6

cpheeo = cpheeo_model(turbidity)
awwa = awwa_model(turbidity)
bis = bis_model(turbidity)

# ============================================================
# CORRECTION FACTORS
# ============================================================

# pH correction
if ph < 5.5:
    ph_factor = 1.2
elif ph > 7.5:
    ph_factor = 1.1
else:
    ph_factor = 1.0

# industrial load
industrial_factor = 1.25 if industrial else 1.0

# turbidity boost
if turbidity > 300:
    turb_factor = 1.35
elif turbidity > 150:
    turb_factor = 1.2
else:
    turb_factor = 1.0

# ============================================================
# AI DOSING CALCULATION (ALWAYS DEFINED)
# ============================================================

if jar_available:
    ai_dose = (
        0.6 * jar_dose +
        0.2 * cpheeo +
        0.1 * awwa +
        0.1 * bis
    )
else:
    ai_dose = (
        0.4 * cpheeo +
        0.35 * awwa +
        0.25 * bis
    )

ai_dose = ai_dose * ph_factor * industrial_factor * turb_factor
ai_dose = float(np.clip(ai_dose, 5, 150))

# ============================================================
# CHEMICAL REQUIREMENT
# ============================================================

alum_kg_day = (ai_dose * flow_m3_day) / 1000
pac_dose = 0.6 * ai_dose

# ============================================================
# STATUS BAND
# ============================================================

if ai_dose > 80:
    st.error("🔴 High Chemical Demand")
elif ai_dose > 40:
    st.warning("🟡 Moderate Condition")
else:
    st.success("🟢 Normal Operation")

# ============================================================
# LAYOUT
# ============================================================

left, right = st.columns([1.1, 1.4])

# ============================================================
# 📊 LEFT → GRAPH
# ============================================================

with left:

    st.markdown("### 📊 Dosing Decision Curve")

    x = np.linspace(0, 300, 100)
    y_ai = 0.3*x + 8 + 0.0005*(x**2)

    fig = go.Figure()

    # Optimal zone
    fig.add_hrect(y0=20, y1=30, fillcolor="green", opacity=0.15, line_width=0)

    # Warning zone
    fig.add_hrect(y0=30, y1=60, fillcolor="yellow", opacity=0.1, line_width=0)

    # Critical zone
    fig.add_hrect(y0=60, y1=120, fillcolor="red", opacity=0.08, line_width=0)

    # AI curve
    fig.add_trace(go.Scatter(
        x=x,
        y=y_ai,
        line=dict(color="cyan", width=4),
        name="AI Curve"
    ))

    # Operating point (SAFE)
    fig.add_trace(go.Scatter(
        x=[turbidity],
        y=[ai_dose],
        mode="markers+text",
        marker=dict(size=14, color="yellow"),
        text=["Operating"],
        textposition="top center"
    ))

    fig.update_layout(
        template="plotly_dark",
        height=350,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Turbidity (NTU)",
        yaxis_title="Alum Dose (mg/L)",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    st.metric("Dose", f"{ai_dose:.1f} mg/L")
    st.metric("Alum Required", f"{alum_kg_day:,.0f} kg/day")

# ============================================================
# 📘 RIGHT → EXPLANATION
# ============================================================

with right:

    st.markdown("### 📘 Recommendation Logic")

    st.markdown(f"""
**Input Conditions**
- Turbidity: **{turbidity} NTU**
- pH: **{ph}**
- Industrial Load: **{"Yes" if industrial else "No"}**
""")

    st.markdown("---")

    st.markdown(f"""
**Standard Estimates**
- CPHEEO: {cpheeo:.1f} mg/L  
- AWWA: {awwa:.1f} mg/L  
- BIS: {bis:.1f} mg/L  
""")

    if jar_available:
        st.success(f"Jar Test Used: {jar_dose:.1f} mg/L")
    else:
        st.warning("Jar Test not used")

    st.markdown("---")

    st.markdown(f"""
### 🧠 Final Decision

👉 **{ai_dose:.1f} mg/L Alum**

✔ Adjusted for:
- pH factor: {ph_factor}
- Industrial factor: {industrial_factor}
- Turbidity factor: {turb_factor}

✔ Ensures:
- Effective coagulation  
- Controlled sludge  
- Stable filtration  

📦 Alum Required: **{alum_kg_day:,.0f} kg/day**  
⚡ PAC Dose: **{pac_dose:.1f} mg/L**
""")

# ============================================================
# ALERT SYSTEM
# ============================================================

if ai_dose > 80:
    st.error("🔴 Consider PAC or Pre-treatment")

elif jar_available and abs(ai_dose - jar_dose) > 5:
    st.warning("🟡 Deviation from Jar Test")

else:
    st.success("🟢 Optimal dosing")


# ==========================================================
# WATER QUALITY EXECUTIVE DASHBOARD - PART 1
# HEADER + KPI + WQI GAUGE
# ==========================================================

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.markdown("---")

st.markdown("""
<div style="
background:linear-gradient(90deg,#0f172a,#1e3a8a);
padding:15px;
border-radius:12px;
text-align:center;
margin-bottom:15px;">
<h2 style="color:white;margin:0;">
📊 WATER QUALITY EXECUTIVE DASHBOARD
</h2>
<p style="color:#cbd5e1;margin:0;">
Moharda Water Supply Monitoring System
</p>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================

wq = pd.read_excel("mohardawaterQuality.xlsx")
# ==========================================================
# GLOBAL MONTH & YEAR FILTER
# ==========================================================

wq["created_da"] = pd.to_datetime(
    wq["created_da"],
    errors="coerce"
)

wq["Year"] = wq["created_da"].dt.year
wq["Month"] = wq["created_da"].dt.month_name()

all_months = [
    "January","February","March","April",
    "May","June","July","August",
    "September","October","November","December"
]

all_years = list(range(2026, 2036))

st.markdown("### 📅 Dashboard Time Filter")

f1, f2 = st.columns(2)

with f1:

    selected_year = st.selectbox(
        "Select Year",
        all_years,
        index=0
    )

with f2:

    selected_month = st.selectbox(
        "Select Month",
        all_months,
        index=0
    )

filtered_wq = wq[
    (wq["Year"] == selected_year)
    &
    (wq["Month"] == selected_month)
]

if filtered_wq.empty:

    st.warning(
        f"⚠️ Data Not Available for {selected_month} {selected_year}"
    )

    st.stop()

st.success(
    f"Showing Dashboard Data for {selected_month} {selected_year}"
)

# Use filtered data for entire dashboard

wq = filtered_wq.copy()
# Remove blank coordinates
wq = wq[
    (wq["Latitude"] != 0) &
    (wq["Longitude"] != 0)
].copy()

# ==========================================================
# WATER QUALITY STATUS
# ==========================================================

def classify(row):

    if str(row["Total_Coli"]).strip().lower() == "present":
        return "Critical"

    if str(row["Faecal_Col"]).strip().lower() == "present":
        return "Critical"

    if row["Turbidity"] > 1:
        return "Observation"

    if row["FRC_PPM"] < 0.2:
        return "Observation"

    return "Safe"

wq["Status"] = wq.apply(classify, axis=1)

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_samples = len(wq)

safe_samples = len(
    wq[wq["Status"] == "Safe"]
)

critical_samples = len(
    wq[wq["Status"] == "Critical"]
)

safe_percent = round(
    (safe_samples / total_samples) * 100,
    1
)

avg_rating = round(
    pd.to_numeric(
        wq["Rating"],
        errors="coerce"
    ).mean(),
    1
)

turb_fail = len(
    wq[wq["Turbidity"] > 1]
)

frc_fail = len(
    wq[wq["FRC_PPM"] < 0.2]
)

coli_fail = len(
    wq[
        wq["Total_Coli"]
        .astype(str)
        .str.lower()
        == "present"
    ]
)

faecal_fail = len(
    wq[
        wq["Faecal_Col"]
        .astype(str)
        .str.lower()
        == "present"
    ]
)

failure_dict = {
    "Turbidity": turb_fail,
    "Low FRC": frc_fail,
    "Total Coliform": coli_fail,
    "Faecal Coliform": faecal_fail
}

top_failure = max(
    failure_dict,
    key=failure_dict.get
)

# ==========================================================
# SIMPLE WQI
# ==========================================================

wqi_score = max(
    0,
    round(
        100 -
        (
            critical_samples * 2
            +
            turb_fail * 0.5
        ),
        1
    )
)

# ==========================================================
# KPI ROW
# ==========================================================

k1,k2,k3,k4,k5,k6 = st.columns(6)

k1.metric(
    "Total Samples",
    total_samples
)

k2.metric(
    "Safe %",
    f"{safe_percent}%"
)

k3.metric(
    "Critical",
    critical_samples
)

k4.metric(
    "Avg Rating",
    avg_rating
)

k5.metric(
    "Top Failure",
    top_failure
)

# ==========================================================
# WQI GAUGE
# ==========================================================

fig_wqi = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=wqi_score,
        title={
            "text":"Water Quality Index"
        },
        gauge={
            "axis":{
                "range":[0,100]
            },
            "bar":{
                "color":"#00B4D8"
            },
            "steps":[

                {
                    "range":[0,50],
                    "color":"#FF6B6B"
                },

                {
                    "range":[50,80],
                    "color":"#FFD166"
                },

                {
                    "range":[80,100],
                    "color":"#06D6A0"
                }
            ]
        }
    )
)

fig_wqi.update_layout(
    height=180,
    margin=dict(
        l=10,
        r=10,
        t=40,
        b=10
    )
)

k6.plotly_chart(
    fig_wqi,
    use_container_width=True
)

st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# WATER QUALITY EXECUTIVE DASHBOARD - PART 2
# AREA WISE COMPARISON
# ==========================================================

st.markdown("### 📊 Area-wise Water Quality Comparison")

# ==========================================================
# AREA SUMMARY
# ==========================================================

zone_summary = (
    wq.groupby("Cust_Name_")
    .agg({
        "Turbidity":"mean",
        "FRC_PPM":"mean",
        "PH":"mean",
        "Rating":"mean"
    })
    .reset_index()
)

zone_summary["Rating"] = (
    pd.to_numeric(
        zone_summary["Rating"],
        errors="coerce"
    )
)

# ==========================================================
# CHART TABS
# ==========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Turbidity",
    "FRC",
    "pH",
    "Rating"
])

# ==========================================================
# TURBIDITY
# ==========================================================

with tab1:

    fig_turb = go.Figure()

    fig_turb.add_trace(
        go.Bar(
            x=zone_summary["Cust_Name_"],
            y=zone_summary["Turbidity"],
            name="Turbidity",
            marker_color="#EF4444"
        )
    )

    fig_turb.add_hline(
        y=1,
        line_dash="dash",
        line_color="green"
    )

    fig_turb.update_layout(
        title="Average Turbidity by Area",
        height=350,
        xaxis_tickangle=-45,
        template="plotly_white",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    st.plotly_chart(
        fig_turb,
        use_container_width=True
    )

# ==========================================================
# FRC
# ==========================================================

with tab2:

    fig_frc = go.Figure()

    fig_frc.add_trace(
        go.Bar(
            x=zone_summary["Cust_Name_"],
            y=zone_summary["FRC_PPM"],
            name="FRC",
            marker_color="#00B4D8"
        )
    )

    fig_frc.add_hline(
        y=0.2,
        line_dash="dash",
        line_color="red"
    )

    fig_frc.update_layout(
        title="Average Free Residual Chlorine",
        height=350,
        xaxis_tickangle=-45,
        template="plotly_white",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    st.plotly_chart(
        fig_frc,
        use_container_width=True
    )

# ==========================================================
# PH
# ==========================================================

with tab3:

    fig_ph = go.Figure()

    fig_ph.add_trace(
        go.Bar(
            x=zone_summary["Cust_Name_"],
            y=zone_summary["PH"],
            name="pH",
            marker_color="#22C55E"
        )
    )

    fig_ph.add_hline(
        y=6.5,
        line_dash="dash",
        line_color="red"
    )

    fig_ph.add_hline(
        y=8.5,
        line_dash="dash",
        line_color="red"
    )

    fig_ph.update_layout(
        title="Average pH by Area",
        height=350,
        xaxis_tickangle=-45,
        template="plotly_white",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    st.plotly_chart(
        fig_ph,
        use_container_width=True
    )

# ==========================================================
# CUSTOMER RATING
# ==========================================================

with tab4:

    fig_rate = go.Figure()

    fig_rate.add_trace(
        go.Bar(
            x=zone_summary["Cust_Name_"],
            y=zone_summary["Rating"],
            name="Rating",
            marker_color="#F59E0B"
        )
    )

    fig_rate.update_layout(
        title="Customer Rating by Area",
        height=350,
        xaxis_tickangle=-45,
        template="plotly_white",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    st.plotly_chart(
        fig_rate,
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# WATER QUALITY EXECUTIVE DASHBOARD - PART 3
# ALERTS & NOTIFICATIONS
# ==========================================================

st.markdown("### 🚨 Alerts & Notifications")

# ==========================================================
# ALERT CALCULATIONS
# ==========================================================

high_turb_df = wq[
    wq["Turbidity"] > 1
]

low_frc_df = wq[
    wq["FRC_PPM"] < 0.2
]

total_coli_df = wq[
    wq["Total_Coli"]
    .astype(str)
    .str.lower()
    == "present"
]

faecal_coli_df = wq[
    wq["Faecal_Col"]
    .astype(str)
    .str.lower()
    == "present"
]

poor_rating_df = wq[
    pd.to_numeric(
        wq["Rating"],
        errors="coerce"
    ) < 2
]

# ==========================================================
# ALERT COUNTERS
# ==========================================================

a1,a2,a3,a4,a5 = st.columns(5)

a1.metric(
    "High Turbidity",
    len(high_turb_df)
)

a2.metric(
    "Low FRC",
    len(low_frc_df)
)

a3.metric(
    "Total Coliform",
    len(total_coli_df)
)

a4.metric(
    "Faecal Coliform",
    len(faecal_coli_df)
)

a5.metric(
    "Poor Rating",
    len(poor_rating_df)
)

st.markdown("---")

# ==========================================================
# ALERT PANELS
# ==========================================================

left_alert,right_alert = st.columns(2)

# ==========================================================
# CRITICAL ALERTS
# ==========================================================

with left_alert:

    st.markdown(
        "#### 🔴 Critical Alerts"
    )

    if len(total_coli_df) > 0:

        for _,row in total_coli_df.head(10).iterrows():

            st.error(
                f"""
                Total Coliform Present

                📍 {row['Cust_Name_']}
                """
            )

    if len(faecal_coli_df) > 0:

        for _,row in faecal_coli_df.head(10).iterrows():

            st.error(
                f"""
                Faecal Coliform Present

                📍 {row['Cust_Name_']}
                """
            )

# ==========================================================
# OBSERVATION ALERTS
# ==========================================================

with right_alert:

    st.markdown(
        "#### 🟡 Observation Alerts"
    )

    if len(high_turb_df) > 0:

        for _,row in high_turb_df.head(5).iterrows():

            st.warning(
                f"""
                High Turbidity
                ({row['Turbidity']})

                📍 {row['Cust_Name_']}
                """
            )

    if len(low_frc_df) > 0:

        for _,row in low_frc_df.head(5).iterrows():

            st.warning(
                f"""
                Low FRC
                ({row['FRC_PPM']})

                📍 {row['Cust_Name_']}
                """
            )

# ==========================================================
# SYSTEM STATUS
# ==========================================================

critical_count = (
    len(total_coli_df)
    +
    len(faecal_coli_df)
)

if critical_count == 0:

    st.success(
        "✅ System Status : Healthy"
    )

elif critical_count <= 5:

    st.warning(
        "⚠️ System Status : Moderate Risk"
    )

else:

    st.error(
        "🚨 System Status : Critical"
    )

st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# WATER QUALITY EXECUTIVE DASHBOARD - PART 4
# FAILURE CONTRIBUTION ANALYSIS
# ==========================================================

st.markdown("### 🥧 Failure Contribution Analysis")

# ==========================================================
# FAILURE COUNTS
# ==========================================================

turb_fail = len(
    wq[wq["Turbidity"] > 1]
)

frc_fail = len(
    wq[wq["FRC_PPM"] < 0.2]
)

total_coli_fail = len(
    wq[
        wq["Total_Coli"]
        .astype(str)
        .str.lower()
        == "present"
    ]
)

faecal_fail = len(
    wq[
        wq["Faecal_Col"]
        .astype(str)
        .str.lower()
        == "present"
    ]
)

ph_fail = len(
    wq[
        (wq["PH"] < 6.5)
        |
        (wq["PH"] > 8.5)
    ]
)

# ==========================================================
# DONUT + SUMMARY
# ==========================================================

left_donut,right_donut = st.columns([2,1])

with left_donut:

    fig_donut = go.Figure(
        data=[
            go.Pie(
                labels=[
                    "Turbidity",
                    "Low FRC",
                    "Total Coliform",
                    "Faecal Coliform",
                    "pH"
                ],
                values=[
                    turb_fail,
                    frc_fail,
                    total_coli_fail,
                    faecal_fail,
                    ph_fail
                ],
                hole=0.60,
                textinfo="label+percent"
            )
        ]
    )

    fig_donut.update_layout(
        height=420,
        title="Failure Contribution Distribution",
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    st.plotly_chart(
        fig_donut,
        use_container_width=True
    )

with right_donut:

    st.markdown("#### Failure Summary")

    st.metric(
        "Turbidity Failures",
        turb_fail
    )

    st.metric(
        "Low FRC Cases",
        frc_fail
    )

    st.metric(
        "Total Coliform",
        total_coli_fail
    )

    st.metric(
        "Faecal Coliform",
        faecal_fail
    )

    st.metric(
        "pH Deviation",
        ph_fail
    )

    failure_dict = {
        "Turbidity": turb_fail,
        "Low FRC": frc_fail,
        "Total Coliform": total_coli_fail,
        "Faecal Coliform": faecal_fail,
        "pH": ph_fail
    }

    dominant_failure = max(
        failure_dict,
        key=failure_dict.get
    )

    st.success(
        f"Dominant Issue: {dominant_failure}"
    )

st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# WATER QUALITY EXECUTIVE DASHBOARD - PART 5
# TREND ANALYSIS
# ==========================================================

st.markdown("### 📈 Water Quality Trend Analysis")

# ==========================================================
# TREND DATA
# ==========================================================

trend_df = wq.copy()

trend_df["created_da"] = pd.to_datetime(
    trend_df["created_da"],
    errors="coerce"
)

trend_df = trend_df.sort_values("created_da")

# ==========================================================
# TABS
# ==========================================================

t1, t2, t3, t4 = st.tabs([
    "Turbidity",
    "FRC",
    "pH",
    "Rating"
])

# ==========================================================
# TURBIDITY TREND
# ==========================================================

with t1:

    fig_turb_trend = go.Figure()

    fig_turb_trend.add_trace(

        go.Scatter(

            x=trend_df["Cust_Name_"],

            y=trend_df["Turbidity"],

            mode="lines+markers",

            marker=dict(
                size=8
            ),

            line=dict(
                color="#EF4444",
                width=3
            ),

            customdata=trend_df["created_da"],

            hovertemplate=
            "<b>%{x}</b><br>" +
            "Turbidity: %{y:.2f} NTU<br>" +
            "Date: %{customdata|%d-%b-%Y}" +
            "<extra></extra>"
        )
    )

    fig_turb_trend.add_hline(
        y=1,
        line_dash="dash",
        line_color="green"
    )

    fig_turb_trend.update_layout(
        title="Turbidity Trend by Sampling Point",
        height=450,
        template="plotly_white",
        xaxis_title="Customer / Sampling Point",
        yaxis_title="Turbidity (NTU)"
    )

    st.plotly_chart(
        fig_turb_trend,
        use_container_width=True
    )

# ==========================================================
# FRC TREND
# ==========================================================

with t2:

    fig_frc_trend = go.Figure()

    fig_frc_trend.add_trace(

        go.Scatter(

            x=trend_df["Cust_Name_"],

            y=trend_df["FRC_PPM"],

            mode="lines+markers",

            marker=dict(
                size=8
            ),

            line=dict(
                color="#00B4D8",
                width=3
            ),

            customdata=trend_df["created_da"],

            hovertemplate=
            "<b>%{x}</b><br>" +
            "FRC: %{y:.2f} ppm<br>" +
            "Date: %{customdata|%d-%b-%Y}" +
            "<extra></extra>"
        )
    )

    fig_frc_trend.add_hline(
        y=0.2,
        line_dash="dash",
        line_color="red"
    )

    fig_frc_trend.add_hline(
        y=1.0,
        line_dash="dash",
        line_color="green"
    )

    fig_frc_trend.update_layout(
        title="Free Residual Chlorine Trend by Sampling Point",
        height=450,
        template="plotly_white",
        xaxis_title="Customer / Sampling Point",
        yaxis_title="FRC (ppm)"
    )

    st.plotly_chart(
        fig_frc_trend,
        use_container_width=True
    )

# ==========================================================
# PH TREND
# ==========================================================

with t3:

    fig_ph_trend = go.Figure()

    fig_ph_trend.add_trace(

        go.Scatter(

            x=trend_df["Cust_Name_"],

            y=trend_df["PH"],

            mode="lines+markers",

            marker=dict(
                size=8
            ),

            line=dict(
                color="#22C55E",
                width=3
            ),

            customdata=trend_df["created_da"],

            hovertemplate=
            "<b>%{x}</b><br>" +
            "pH: %{y:.2f}<br>" +
            "Date: %{customdata|%d-%b-%Y}" +
            "<extra></extra>"
        )
    )

    fig_ph_trend.add_hline(
        y=6.5,
        line_dash="dash",
        line_color="red"
    )

    fig_ph_trend.add_hline(
        y=8.5,
        line_dash="dash",
        line_color="red"
    )

    fig_ph_trend.update_layout(
        title="pH Trend by Sampling Point",
        height=450,
        template="plotly_white",
        xaxis_title="Customer / Sampling Point",
        yaxis_title="pH"
    )

    st.plotly_chart(
        fig_ph_trend,
        use_container_width=True
    )

# ==========================================================
# RATING TREND
# ==========================================================

with t4:

    fig_rating = go.Figure()

    fig_rating.add_trace(

        go.Scatter(

            x=trend_df["Cust_Name_"],

            y=trend_df["Rating"],

            mode="lines+markers",

            marker=dict(
                size=8
            ),

            line=dict(
                color="#F59E0B",
                width=3
            ),

            customdata=trend_df["created_da"],

            hovertemplate=
            "<b>%{x}</b><br>" +
            "Rating: %{y:.1f}<br>" +
            "Date: %{customdata|%d-%b-%Y}" +
            "<extra></extra>"
        )
    )

    fig_rating.update_layout(
        title="Customer Rating Trend by Sampling Point",
        height=450,
        template="plotly_white",
        xaxis_title="Customer / Sampling Point",
        yaxis_title="Rating"
    )

    st.plotly_chart(
        fig_rating,
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# WATER QUALITY EXECUTIVE DASHBOARD - PART 6
# RISK RANKING & CRITICAL AREA IDENTIFICATION
# ==========================================================

st.markdown("### 🏆 Risk Ranking & Critical Area Analysis")

# ==========================================================
# RISK SCORE CALCULATION
# ==========================================================

risk_df = wq.copy()

risk_df["Turbidity_Risk"] = (
    risk_df["Turbidity"] > 1
).astype(int)

risk_df["FRC_Risk"] = (
    risk_df["FRC_PPM"] < 0.2
).astype(int)

risk_df["TotalColi_Risk"] = (
    risk_df["Total_Coli"]
    .astype(str)
    .str.lower()
    .eq("present")
).astype(int)

risk_df["Faecal_Risk"] = (
    risk_df["Faecal_Col"]
    .astype(str)
    .str.lower()
    .eq("present")
).astype(int)

risk_df["Rating_Risk"] = (
    pd.to_numeric(
        risk_df["Rating"],
        errors="coerce"
    ) < 2
).astype(int)

# Weighted Score

risk_df["Risk_Score"] = (
    risk_df["Turbidity_Risk"] * 2 +
    risk_df["FRC_Risk"] * 2 +
    risk_df["TotalColi_Risk"] * 5 +
    risk_df["Faecal_Risk"] * 5 +
    risk_df["Rating_Risk"] * 1
)

# ==========================================================
# ZONE RISK
# ==========================================================

zone_risk = (
    risk_df.groupby("Cust_Name_")
    .agg({
        "Risk_Score":"sum",
        "Turbidity":"mean",
        "FRC_PPM":"mean",
        "PH":"mean",
        "Rating":"mean"
    })
    .reset_index()
)

zone_risk = zone_risk.sort_values(
    "Risk_Score",
    ascending=False
)

# ==========================================================
# RISK CATEGORY
# ==========================================================

def risk_category(score):

    if score >= 10:
        return "🔴 Critical"

    elif score >= 5:
        return "🟡 Moderate"

    else:
        return "🟢 Safe"

zone_risk["Status"] = (
    zone_risk["Risk_Score"]
    .apply(risk_category)
)

# ==========================================================
# LAYOUT
# ==========================================================

left_rank,right_rank = st.columns([2,1])

# ==========================================================
# RANKING TABLE
# ==========================================================

with left_rank:

    st.markdown(
        "#### Risk Ranking Table"
    )

    ranking_table = zone_risk[
        [
            "Cust_Name_",
            "Risk_Score",
            "Status",
            "Turbidity",
            "FRC_PPM",
            "Rating"
        ]
    ]

    st.dataframe(
        ranking_table,
        use_container_width=True,
        height=420
    )

# ==========================================================
# TOP 5 CRITICAL AREAS
# ==========================================================

with right_rank:

    st.markdown(
        "#### Top Critical Areas"
    )

    top5 = zone_risk.head(5)

    for _,row in top5.iterrows():

        st.error(
            f"""
            📍 {row['Cust_Name_']}

            Risk Score : {row['Risk_Score']}

            Status : {row['Status']}
            """
        )

# ==========================================================
# RISK BAR CHART
# ==========================================================

fig_risk = px.bar(

    zone_risk.head(15),

    x="Cust_Name_",

    y="Risk_Score",

    color="Risk_Score",

    title="Area Risk Ranking"

)

fig_risk.update_layout(

    height=400,

    xaxis_tickangle=-45,

    margin=dict(
        l=10,
        r=10,
        t=50,
        b=10
    )
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)

st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# WATER QUALITY EXECUTIVE DASHBOARD - PART 7
# WATER QUALITY SCORE BY ZONE
# ==========================================================

st.markdown("### 💧 Water Quality Score (WQI) by Zone")

# ==========================================================
# WQI CALCULATION
# ==========================================================

wqi_df = wq.copy()

# Turbidity Score
wqi_df["Turbidity_Score"] = wqi_df["Turbidity"].apply(
    lambda x: 25 if x <= 1 else max(0, 25 - (x*5))
)

# FRC Score
wqi_df["FRC_Score"] = wqi_df["FRC_PPM"].apply(
    lambda x: 25 if 0.2 <= x <= 1.0 else 10
)

# PH Score
wqi_df["PH_Score"] = wqi_df["PH"].apply(
    lambda x: 25 if 6.5 <= x <= 8.5 else 10
)

# Coliform Score
wqi_df["Coliform_Score"] = wqi_df["Total_Coli"].astype(str).apply(
    lambda x: 25 if x.lower() == "absent" else 0
)

# Total WQI
wqi_df["WQI"] = (
    wqi_df["Turbidity_Score"] +
    wqi_df["FRC_Score"] +
    wqi_df["PH_Score"] +
    wqi_df["Coliform_Score"]
)

# ==========================================================
# ZONE WQI
# ==========================================================

zone_wqi = (
    wqi_df.groupby("Cust_Name_")["WQI"]
    .mean()
    .reset_index()
)

zone_wqi = zone_wqi.sort_values(
    "WQI",
    ascending=False
)

# ==========================================================
# CATEGORY
# ==========================================================

def wqi_status(score):

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Good"

    elif score >= 60:
        return "Moderate"

    else:
        return "Poor"

zone_wqi["Category"] = (
    zone_wqi["WQI"]
    .apply(wqi_status)
)

# ==========================================================
# LAYOUT
# ==========================================================

left_wqi,right_wqi = st.columns([2,1])

# ==========================================================
# WQI BAR CHART
# ==========================================================

with left_wqi:

    fig_wqi_zone = px.bar(

        zone_wqi,

        x="Cust_Name_",

        y="WQI",

        color="WQI",

        title="Water Quality Index by Zone",

        text_auto=".1f"
    )

    fig_wqi_zone.update_layout(

        height=450,

        xaxis_tickangle=-45,

        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    st.plotly_chart(
        fig_wqi_zone,
        use_container_width=True
    )

# ==========================================================
# BEST & WORST AREA
# ==========================================================

with right_wqi:

    best_area = zone_wqi.iloc[0]

    worst_area = zone_wqi.iloc[-1]

    st.success(
        f"""
        🏆 Best Area

        {best_area['Cust_Name_']}

        WQI : {best_area['WQI']:.1f}
        """
    )

    st.error(
        f"""
        ⚠ Worst Area

        {worst_area['Cust_Name_']}

        WQI : {worst_area['WQI']:.1f}
        """
    )

    st.markdown("#### Zone Status")

    for _,row in zone_wqi.head(10).iterrows():

        if row["Category"] == "Excellent":

            st.success(
                f"{row['Cust_Name_']} - {row['Category']}"
            )

        elif row["Category"] == "Good":

            st.info(
                f"{row['Cust_Name_']} - {row['Category']}"
            )

        elif row["Category"] == "Moderate":

            st.warning(
                f"{row['Cust_Name_']} - {row['Category']}"
            )

        else:

            st.error(
                f"{row['Cust_Name_']} - {row['Category']}"
            )

st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# WATER QUALITY EXECUTIVE DASHBOARD - PART 8
# CUSTOMER SATISFACTION ANALYSIS
# ==========================================================

st.markdown("### ⭐ Customer Satisfaction Dashboard")

# ==========================================================
# CLEAN DATA
# ==========================================================

cust_df = wq.copy()

cust_df["Rating"] = pd.to_numeric(
    cust_df["Rating"],
    errors="coerce"
)

cust_df = cust_df.dropna(
    subset=["Rating"]
)

# ==========================================================
# RATING CATEGORY
# ==========================================================

def rating_category(x):

    if x >= 4:
        return "Excellent"

    elif x >= 3:
        return "Good"

    elif x >= 2:
        return "Average"

    else:
        return "Poor"

cust_df["Rating_Category"] = (
    cust_df["Rating"]
    .apply(rating_category)
)

# ==========================================================
# SUMMARY
# ==========================================================

avg_rating = round(
    cust_df["Rating"].mean(),
    2
)

excellent = len(
    cust_df[
        cust_df["Rating_Category"]
        == "Excellent"
    ]
)

good = len(
    cust_df[
        cust_df["Rating_Category"]
        == "Good"
    ]
)

average = len(
    cust_df[
        cust_df["Rating_Category"]
        == "Average"
    ]
)

poor = len(
    cust_df[
        cust_df["Rating_Category"]
        == "Poor"
    ]
)

# ==========================================================
# KPI ROW
# ==========================================================

r1,r2,r3,r4,r5 = st.columns(5)

r1.metric(
    "Avg Rating",
    avg_rating
)

r2.metric(
    "Excellent",
    excellent
)

r3.metric(
    "Good",
    good
)

r4.metric(
    "Average",
    average
)

r5.metric(
    "Poor",
    poor
)

# ==========================================================
# LAYOUT
# ==========================================================

left_rate,right_rate = st.columns([2,1])

# ==========================================================
# DONUT CHART
# ==========================================================

with left_rate:

    fig_rating_donut = go.Figure(
        data=[
            go.Pie(
                labels=[
                    "Excellent",
                    "Good",
                    "Average",
                    "Poor"
                ],
                values=[
                    excellent,
                    good,
                    average,
                    poor
                ],
                hole=0.60,
                textinfo="label+percent"
            )
        ]
    )

    fig_rating_donut.update_layout(
        title="Customer Rating Distribution",
        height=420
    )

    st.plotly_chart(
        fig_rating_donut,
        use_container_width=True
    )

# ==========================================================
# CUSTOMER PERCEPTION
# ==========================================================

with right_rate:

    st.markdown(
        "#### Customer Perception"
    )

    if "Customer_P" in cust_df.columns:

        perception = (
            cust_df["Customer_P"]
            .astype(str)
            .value_counts()
        )

        for item,count in perception.head(10).items():

            st.info(
                f"{item} : {count}"
            )

# ==========================================================
# AREA WISE CUSTOMER SATISFACTION
# ==========================================================

st.markdown(
    "#### Area-wise Customer Rating"
)

area_rating = (
    cust_df.groupby("Cust_Name_")
    ["Rating"]
    .mean()
    .reset_index()
)

fig_area_rating = px.bar(

    area_rating,

    x="Cust_Name_",

    y="Rating",

    color="Rating",

    text_auto=".1f",

    title="Average Customer Rating by Area"

)

fig_area_rating.update_layout(

    height=420,

    xaxis_tickangle=-45,

    margin=dict(
        l=10,
        r=10,
        t=50,
        b=10
    )
)

st.plotly_chart(
    fig_area_rating,
    use_container_width=True
)

st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# WATER QUALITY EXECUTIVE DASHBOARD - PART 9
# EXECUTIVE HEATMAP ANALYSIS
# ==========================================================

st.markdown("### 🔥 Executive Heatmap Dashboard")

# ==========================================================
# PREPARE DATA
# ==========================================================

heat_df = wq.copy()

st.success(
    f"Showing Executive Heatmap for {selected_month} {selected_year}"
)
heat_df["UpdatedOn"] = pd.to_datetime(
    heat_df["UpdatedOn"],
    errors="coerce"
)

heat_df["Rating"] = pd.to_numeric(
    heat_df["Rating"],
    errors="coerce"
)

# Latest record from each area
zone_heat = (
    heat_df
    .sort_values("UpdatedOn")
    .groupby("Cust_Name_", as_index=True)
    .last()
)

# ==========================================================
# COMPLIANCE SCORING
# ==========================================================

def turbidity_score(x):

    if pd.isna(x):
        return 1

    elif x <= 1:
        return 5

    elif x <= 5:
        return 3

    else:
        return 1


def frc_score(x):

    if pd.isna(x):
        return 1

    elif 0.2 <= x <= 1.0:
        return 5

    elif (0.1 <= x < 0.2) or (1.0 < x <= 1.5):
        return 3

    else:
        return 1


def ph_score(x):

    if pd.isna(x):
        return 1

    elif 6.6 <= x <= 8.5:
        return 5

    elif (6.0 <= x < 6.6) or (8.5 < x <= 9.0):
        return 3

    else:
        return 1


def rating_score(x):

    if pd.isna(x):
        return 1

    elif x >= 4.5:
        return 5

    elif x >= 3:
        return 3

    else:
        return 1


def coliform_score(x):

    if str(x).strip().lower() == "absent":
        return 5

    return 1


# ==========================================================
# SCORE MATRIX
# ==========================================================

score_matrix = pd.DataFrame(
    index=zone_heat.index
)

score_matrix["Turbidity"] = (
    zone_heat["Turbidity"]
    .apply(turbidity_score)
)

score_matrix["FRC"] = (
    zone_heat["FRC_PPM"]
    .apply(frc_score)
)

score_matrix["pH"] = (
    zone_heat["PH"]
    .apply(ph_score)
)

score_matrix["Rating"] = (
    zone_heat["Rating"]
    .apply(rating_score)
)

score_matrix["Total Coliform"] = (
    zone_heat["Total_Coli"]
    .apply(coliform_score)
)

score_matrix["Faecal Coliform"] = (
    zone_heat["Faecal_Col"]
    .apply(coliform_score)
)

# ==========================================================
# TEXT DISPLAY MATRIX
# ==========================================================

text_matrix = []

for _, row in zone_heat.iterrows():

    text_matrix.append([

        f"{row['Turbidity']:.2f}",

        f"{row['FRC_PPM']:.2f}",

        f"{row['PH']:.2f}",

        f"{row['Rating']:.1f}",

        str(row["Total_Coli"]),

        str(row["Faecal_Col"])

    ])

# ==========================================================
# HEATMAP FIGURE
# ==========================================================

fig_heat = go.Figure(

    data=go.Heatmap(

        z=score_matrix.values,

        x=[
            "Turbidity",
            "FRC",
            "pH",
            "Rating",
            "Total Coliform",
            "Faecal Coliform"
        ],

        y=score_matrix.index,

        colorscale=[
            [0.0, "#EF4444"],
            [0.5, "#FACC15"],
            [1.0, "#22C55E"]
        ],

        zmin=1,
        zmax=5,

        text=text_matrix,

        texttemplate="%{text}",

        textfont=dict(
            size=9,
            color="black"
        ),

        hoverongaps=False

    )

)

fig_heat.update_layout(

    title="Zone-wise Water Quality Compliance Heatmap",

    height=max(
        700,
        len(score_matrix.index) * 35
    ),

    margin=dict(
        l=10,
        r=10,
        t=60,
        b=10
    )

)

st.plotly_chart(
    fig_heat,
    use_container_width=True
)

# ==========================================================
# HEATMAP LEGEND
# ==========================================================

with st.expander(
    "📘 Executive Heatmap Standards (Click to View)",
    expanded=False
):

    st.markdown(
        """
### Turbidity (NTU)
- 🟢 ≤ 1 : Desirable
- 🟡 > 1 to 5 : Acceptable / Permissible
- 🔴 > 5 : Non-Compliant

### pH
- 🟢 6.6 – 8.5 : Acceptable Range
- 🟡 6.0 – 6.5 or 8.5 – 9.0 : Observation
- 🔴 < 6.0 or > 9.0 : Non-Compliant

### Free Residual Chlorine (FRC)
- 🟢 0.2 – 1.0 ppm : Adequate Residual Chlorine
- 🟡 0.1 – 0.2 ppm or 1.0 – 1.5 ppm : Observation
- 🔴 < 0.1 ppm or > 1.5 ppm : Non-Compliant

### Customer Rating
- 🟢 5 : Excellent
- 🟡 3 – 4 : Average / Satisfactory
- 🔴 1 – 2 : Poor

### Total Coliform
- 🟢 Absent
- 🔴 Present

### Faecal Coliform
- 🟢 Absent
- 🔴 Present

### Heatmap Interpretation
- 🟢 Green = Within Standard
- 🟡 Yellow = Acceptable / Observation
- 🔴 Red = Requires Immediate Attention
"""
    )
st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# WATER QUALITY EXECUTIVE DASHBOARD - PART 10
# FILTERS + EXECUTIVE SUMMARY
# ==========================================================

st.markdown("### 🎯 Dashboard Filters & Executive Summary")

# ==========================================================
# FILTERS
# ==========================================================

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:

    zone_filter = st.multiselect(
        "Select Area",
        sorted(
            wq["Cust_Name_"]
            .dropna()
            .unique()
            .tolist()
        ),
        default=[]
    )

with filter_col2:

    if "Source" in wq.columns:

        source_filter = st.multiselect(
            "Select Source",
            sorted(
                wq["Source"]
                .dropna()
                .unique()
                .tolist()
            ),
            default=[]
        )

    else:
        source_filter = []

with filter_col3:

    if "Collect_Typ" in wq.columns:

        collect_filter = st.multiselect(
            "Collection Type",
            sorted(
                wq["Collect_Typ"]
                .dropna()
                .unique()
                .tolist()
            ),
            default=[]
        )

    else:
        collect_filter = []

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_df = wq.copy()

if zone_filter:

    filtered_df = filtered_df[
        filtered_df["Cust_Name_"]
        .isin(zone_filter)
    ]

if source_filter:

    filtered_df = filtered_df[
        filtered_df["Source"]
        .isin(source_filter)
    ]

if collect_filter:

    filtered_df = filtered_df[
        filtered_df["Collect_Typ"]
        .isin(collect_filter)
    ]

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.markdown("---")
st.markdown("## 📋 Executive Summary")

summary1, summary2 = st.columns(2)

with summary1:

    st.markdown(
        f"""
        <div style="
        background:white;
        padding:18px;
        border-radius:12px;
        border-left:6px solid #0d6efd;
        margin-bottom:10px;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">
        <h5>📊 Total Samples Analysed</h5>
        <h2>{len(filtered_df)}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
        background:white;
        padding:18px;
        border-radius:12px;
        border-left:6px solid #198754;
        margin-bottom:10px;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">
        <h5>✅ Safe Samples</h5>
        <h2>{safe_samples}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
        background:white;
        padding:18px;
        border-radius:12px;
        border-left:6px solid #dc3545;
        margin-bottom:10px;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">
        <h5>🚨 Critical Samples</h5>
        <h2>{critical_samples}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
        background:white;
        padding:18px;
        border-radius:12px;
        border-left:6px solid #fd7e14;
        margin-bottom:10px;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">
        <h5>⭐ Average Rating</h5>
        <h2>{avg_rating}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with summary2:

    st.markdown(
        f"""
        <div style="
        background:#e8f5e9;
        padding:18px;
        border-radius:12px;
        border-left:6px solid #198754;
        margin-bottom:10px;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">
        <h5>💧 Water Quality Index</h5>
        <h1>{wqi_score}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
        background:white;
        padding:18px;
        border-radius:12px;
        border-left:6px solid #6f42c1;
        margin-bottom:10px;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">
        <h5>⚠ Most Frequent Failure</h5>
        <h3>{top_failure}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
        background:white;
        padding:18px;
        border-radius:12px;
        border-left:6px solid #20c997;
        margin-bottom:10px;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">
        <h5>🦠 Total Coliform Cases</h5>
        <h2>{total_coliform}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# FINAL STATUS
# ==========================================================

st.markdown("### 🎯 Overall System Status")

if wqi_score >= 80:

    st.markdown(
        """
        <div style="
        background:#d1e7dd;
        color:#0f5132;
        padding:20px;
        border-radius:12px;
        text-align:center;
        font-size:24px;
        font-weight:bold;
        ">
        ✅ GOOD WATER QUALITY
        </div>
        """,
        unsafe_allow_html=True
    )

elif wqi_score >= 60:

    st.markdown(
        """
        <div style="
        background:#fff3cd;
        color:#664d03;
        padding:20px;
        border-radius:12px;
        text-align:center;
        font-size:24px;
        font-weight:bold;
        ">
        ⚠ MODERATE ATTENTION REQUIRED
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div style="
        background:#f8d7da;
        color:#842029;
        padding:20px;
        border-radius:12px;
        text-align:center;
        font-size:24px;
        font-weight:bold;
        ">
        🚨 IMMEDIATE ACTION REQUIRED
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# DASHBOARD FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
    """
    <div style="
    text-align:center;
    padding:18px;
    background:linear-gradient(90deg,#0d6efd,#20c997);
    color:white;
    border-radius:12px;
    font-size:16px;
    font-weight:bold;
    ">
    GIS Based Water Quality Executive Dashboard<br>
    Moharda Water Supply System Monitoring
    </div>
    """,
    unsafe_allow_html=True
)
