# fire_detection_robot.py

import streamlit as st
import random

# Simulate environment: each "room" has a simulated temp and light intensity
def simulate_room_sensor_data():
    return {
        "light": random.randint(100, 1000),  # Light intensity in lux
        "temp": random.randint(20, 100)      # Temperature in Celsius
    }

# Determine if fire is present
def detect_fire(light, temp, light_thresh=700, temp_thresh=60):
    return light > light_thresh or temp > temp_thresh

# Initialize or get previous session state
if 'visited_rooms_with_fire' not in st.session_state:
    st.session_state.visited_rooms_with_fire = set()

# Streamlit App UI
st.title("🔥 Fire Detection Robot")
st.markdown("Simulated environment with light & temperature sensors.")

room_id = st.number_input("Enter Room ID (numeric)", min_value=0, value=0, step=1)
scan_button = st.button("Scan Room")

if scan_button:
    sensor_data = simulate_room_sensor_data()
    light = sensor_data['light']
    temp = sensor_data['temp']
    st.write(f"Sensor Readings → Light: {light} lux, Temperature: {temp}°C")

    fire_present = detect_fire(light, temp)

    if fire_present:
        if room_id not in st.session_state.visited_rooms_with_fire:
            st.session_state.visited_rooms_with_fire.add(room_id)
            st.error("🚨 Fire detected! Alarm sounding...")
        else:
            st.warning("⚠️ Fire previously detected in this room. No new alarm.")
    else:
        st.success("✅ No fire detected. Continuing scan...")

# Display state for debugging
with st.expander("Visited Rooms with Fire (Debug)"):
    st.write(st.session_state.visited_rooms_with_fire)
