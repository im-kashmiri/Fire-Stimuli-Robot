# fire_detection_robot.py

import streamlit as st
import random

# ----- Simulation + Detection Logic -----
def simulate_room_sensor_data():
    return {
        "light": random.randint(100, 1000),
        "temp": random.randint(20, 100)
    }

def detect_fire(light, temp, light_thresh=700, temp_thresh=60):
    return light > light_thresh or temp > temp_thresh

# ----- Session State Setup -----
if 'visited_rooms_with_fire' not in st.session_state:
    st.session_state.visited_rooms_with_fire = set()
if 'scanned_rooms' not in st.session_state:
    st.session_state.scanned_rooms = set()

# ----- Streamlit UI -----
st.set_page_config(page_title="Fire Detection Robot", layout="wide")
st.title("🤖🔥 Fire Detection Robot Simulator")
st.markdown("Simulating a 10x10 room grid with light & temperature sensors.")

room_id = st.number_input("Enter Room ID (0 - 99)", min_value=0, max_value=99, value=0, step=1)
scan_button = st.button("Scan Room")

# ----- Scan Logic -----
if scan_button:
    sensor_data = simulate_room_sensor_data()
    light = sensor_data['light']
    temp = sensor_data['temp']
    st.write(f"**Sensor Readings →** Light: `{light} lux`, Temperature: `{temp}°C`")

    fire_present = detect_fire(light, temp)
    st.session_state.scanned_rooms.add(room_id)

    if fire_present:
        if room_id not in st.session_state.visited_rooms_with_fire:
            st.session_state.visited_rooms_with_fire.add(room_id)
            st.error("🚨 Fire detected! Alarm sounding...")
        else:
            st.warning("⚠️ Fire already detected in this room. No re-alarm.")
    else:
        st.success("✅ No fire detected. Continuing scan...")

# ----- Grid Display -----
st.markdown("---")
st.subheader("🗺️ Room Grid Map (0–99)")

def get_room_display(i):
    if i in st.session_state.visited_rooms_with_fire:
        return "🔥"
    elif i in st.session_state.scanned_rooms:
        return "✅"
    else:
        return "⬜️"

cols = st.columns(10)
for i in range(100):
    with cols[i % 10]:
        st.markdown(f"**{i}**<br>{get_room_display(i)}", unsafe_allow_html=True)

# ----- Debug Info (Optional) -----
with st.expander("Debug Info"):
    st.write("Visited Rooms with Fire:", st.session_state.visited_rooms_with_fire)
    st.write("Scanned Rooms:", st.session_state.scanned_rooms)
