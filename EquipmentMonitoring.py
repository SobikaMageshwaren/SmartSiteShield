import streamlit as st
import pandas as pd
import random
from streamlit.components.v1 import html

# Load dataset
@st.cache_data
def load_dataset():
    return pd.read_csv("machinery_dataset.csv")

# Simulating IoT sensors and video analytics for worker safety monitoring

# Stored data for machinery suitability
STORED_MACHINERY_DATA = {
    "Machine_A": {"max_vibration": 3.0, "max_temperature": 80.0},
    "Machine_B": {"max_vibration": 2.5, "max_temperature": 75.0},
    "Machine_C": {"max_vibration": 4.0, "max_temperature": 85.0},
}

def monitor_equipment_status():
    """Simulates monitoring machinery for malfunctions."""
    equipment_data = {
        "vibration": random.uniform(0, 5),  # Abnormal vibration levels
        "temperature": random.uniform(30, 100),  # Machinery temperature in Celsius
        "air_quality": random.randint(50, 200),  # AQI index
    }
    return equipment_data

def evaluate_machinery_suitability(equipment_data):
    """Evaluates if machines can be used based on stored data."""
    suitability = {}

    for machine, thresholds in STORED_MACHINERY_DATA.items():
        reasons = []
        if equipment_data["vibration"] > thresholds["max_vibration"]:
            reasons.append(f"Vibration Level too high ({equipment_data['vibration']:.2f} > {thresholds['max_vibration']})")
        if equipment_data["temperature"] > thresholds["max_temperature"]:
            reasons.append(f"Temperature too high ({equipment_data['temperature']:.1f}°C > {thresholds['max_temperature']}°C)")
        if equipment_data["air_quality"] > 150:
            reasons.append(f"Poor Air Quality (AQI: {equipment_data['air_quality']})")

        if reasons:
            suitability[machine] = f"Not Suitable: {', '.join(reasons)}"
        else:
            suitability[machine] = "Suitable"

    return suitability

def calculate_cool_down_time(current_temp, max_temp):
    """Calculates approximate cool-down time for machinery."""
    if current_temp <= max_temp:
        return 0
    # Assuming a cooling rate of 1°C per minute
    return int(current_temp - max_temp)

def display_popup(message):
    """Displays a popup message in Streamlit."""
    popup_script = f"""
    <script>
    alert("{message}");
    </script>
    """
    html(popup_script)

# Streamlit app
st.title("Machinery Suitability Monitoring")

# Load and display dataset
st.sidebar.header("Dataset Options")
if st.sidebar.checkbox("Show Dataset"):
    df = load_dataset()
    st.subheader("Machinery Dataset")
    st.write(df)

st.sidebar.header("Select Machine")
machine = st.sidebar.selectbox("Choose a machine to evaluate", ["Machine_A", "Machine_B", "Machine_C"])

if st.sidebar.button("Evaluate Machine"):
    equipment_data = monitor_equipment_status()
    machinery_suitability = evaluate_machinery_suitability(equipment_data)

    if machine in machinery_suitability:
        st.subheader(f"Details for {machine}")
        st.write(f"**Vibration:** {equipment_data['vibration']:.2f}")
        st.write(f"**Temperature:** {equipment_data['temperature']:.1f}°C")
        st.write(f"**Air Quality (AQI):** {equipment_data['air_quality']}")
        st.write(f"**Suitability:** {machinery_suitability[machine]}")

        # Check if person can go near the machine
        max_temp = STORED_MACHINERY_DATA[machine]["max_temperature"]
        cool_down_time = calculate_cool_down_time(equipment_data["temperature"], max_temp)

        if cool_down_time == 0:
            display_popup("✅ A person can go near the machine.")
        else:
            display_popup(f"❌ A person should not go near the machine. It will take approximately {cool_down_time} minutes to cool down.")
else:
    st.write("Select a machine and click 'Evaluate Machine' to see details.")
