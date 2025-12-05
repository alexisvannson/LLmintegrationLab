import streamlit as st
import subprocess
import json
from emissions import EMISSIONS
from prompts import carbon_prompt

# ---- UI ----
st.title("🌱 Carbon Footprint Estimator (using Ollama + Llama3:8b)")
st.write("Estimate your daily CO₂ emissions and get reduction tips.")

# COMMUTING
st.header("🚗 Commuting")
transport_mode = st.selectbox(
    "Choose your transport type:",
    list(EMISSIONS["transport"].keys())
)
distance = st.slider("Daily commuting distance (km/day):", 0, 100, 10)

# DIET
st.header("🥗 Diet")
diet_type = st.selectbox(
    "Your diet type:",
    list(EMISSIONS["diet"].keys())
)

# HEATING
st.header("🔥 Heating")
heating_type = st.selectbox(
    "Heating method:",
    list(EMISSIONS["heating"].keys())
)
heating_hours = st.slider("Hours of heating per day:", 0, 24, 4)

# ELECTRICITY
st.header("⚡ Electricity Use")
kwh = st.slider("Daily electricity use (kWh/day):", 0, 50, 10)

# ---- CALCULATIONS ----
transport_emissions = EMISSIONS["transport"][transport_mode] * distance
diet_emissions = EMISSIONS["diet"][diet_type]
heating_emissions = EMISSIONS["heating"][heating_type] * heating_hours
electricity_emissions = EMISSIONS["electricity"]["kwh"] * kwh

total = (
    transport_emissions +
    diet_emissions +
    heating_emissions +
    electricity_emissions
)

st.subheader(f"Your estimated daily footprint: **{total:.2f} kg CO₂/day**")

details = json.dumps({
    "transport_mode": transport_mode,
    "distance_km": distance,
    "diet_type": diet_type,
    "heating": heating_type,
    "heating_hours": heating_hours,
    "electricity_kwh": kwh
}, indent=2)

# ---- LLM ANALYSIS ----
if st.button("Get Sustainability Advice (Llama3:8b)"):
    st.write("Generating analysis...")

    prompt = carbon_prompt(total, details)

    # Run Ollama
    result = subprocess.run(
        ["ollama", "run", "llama3:8b"],
        input=prompt,
        text=True,
        capture_output=True
    )

    st.markdown(result.stdout)
