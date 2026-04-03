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
    receiver = "alokranjanjha18april@gmail.com"

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
