# ==============================
# AI WORM DETECTION + RISK SYSTEM
# ==============================

import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

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
# ==============================
# 🌊 AI INTAKE DEBRIS MODULE
# ==============================

from ultralytics import YOLO
from PIL import Image
import numpy as np
import streamlit as st

@st.cache_resource
def load_model():
    return YOLO("best.pt")

debris_model = load_model()

st.markdown("---")
st.header("🌊 AI Intake Monitoring System")

uploaded_img = st.file_uploader("Upload Intake Image", type=["jpg","png","jpeg"], key="intake")

if uploaded_img:
    img = Image.open(uploaded_img)
    st.image(img, caption="Intake Image", use_container_width=True)

    if st.button("🔍 Run AI Analysis"):

        # Convert image to numpy (important for YOLO stability)
        img_np = np.array(img)

        results = debris_model(img_np)

        detected = []
        total_area = 0.0 # ensure float

        for r in results:
            if r.boxes is not None:
                for box in r.boxes:

                    label = r.names[int(box.cls[0])]
                    detected.append(label)

                    # Convert tensor → float
                    x1, y1, x2, y2 = box.xyxy[0].tolist()

                    area = (x2 - x1) * (y2 - y1)
                    total_area += float(area)

        # ==========================
        # 📊 INTELLIGENT ANALYSIS
        # ==========================
        st.subheader("📊 AI Detection Summary")
        st.write("Detected Objects:", detected)

        debris_count = len(detected)

        # Avoid division by zero
        img_area = img.size[0] * img.size[1]

        if img_area > 0:
            density = total_area / img_area
        else:
            density = 0

        st.write(f"Debris Density: {round(float(density),3)}")

        # ==========================
        #  AI DECISION ENGINE
        # ==========================
        st.subheader("⚠️ AI Identified Issues")

        issues = []
        actions = []

        # --- Plastic detection ---
        if any(x in detected for x in ["plastic", "bottle", "bag"]):
            issues.append("Plastic accumulation → Intake blockage risk")
            actions.append("Install / clean trash racks immediately")

        # --- Organic load ---
        if any(x in detected for x in ["leaf", "plant"]):
            issues.append("High organic load → Increased coagulant demand")
            actions.append("Increase alum/PAC dosing temporarily")

        # --- High density ---
        if density > 0.15:
            issues.append("High debris density → Clarifier overload risk")
            actions.append("Reduce intake flow rate")

        # --- Extreme condition ---
        if density > 0.25 or debris_count > 8:
            issues.append("Extreme debris condition → Filter choking risk")
            actions.append("Prepare for frequent backwashing")

        # --- No detection ---
        if debris_count == 0:
            issues.append("No visible debris → System stable")
            actions.append("Maintain normal operation")

        # ==========================
        # OUTPUT
        # ==========================
        for i in issues:
            st.write("•", i)

        st.subheader("🛠 Recommended Actions")

        for a in actions:
            st.write("•", a)

        # ==========================
        # IMAGE OUTPUT
        # ==========================
        st.subheader("📦 Detection Output")

        for r in results:
            st.image(r.plot(), use_container_width=True)

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
# 🔊 CONTINUOUS ALARM (FINAL FIX)
# ===============================

# One-time enable (browser restriction)
if "sound_enabled" not in st.session_state:
    st.session_state.sound_enabled = False

if not st.session_state.sound_enabled:
    if st.button("🔊 Enable Alarm Sound", key="enable_sound"):
        st.session_state.sound_enabled = True
        st.success("Sound Enabled ✅")

# Alarm
if st.session_state.alarm:

    st.error("🚨 CONTINUOUS ALARM ACTIVE")

    # Flashing UI
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

    # 🔊 LOOP SOUND (BEST METHOD)
    if st.session_state.sound_enabled:
        st.markdown("""
        <audio autoplay loop>
        <source src="mixkit-sport-start-bleeps-918.wav" type="audio/wav">
        </audio>
        """, unsafe_allow_html=True)
    else:
        st.warning("🔊 Enable sound once")

    # Stop button
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
