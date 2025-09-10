import streamlit as st
import json
import os
import pandas as pd
import altair as alt
from datetime import date

FILE_PATH = "sport_data.json"
EXERCISES = ["Squat", "Bench Press", "Deadlift", "Overhead Press", "Barbell Row"]

# Loading JSON and creating default structures
def load_data():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
    else:
        data = {}
    data.setdefault("records", {ex: [] for ex in EXERCISES})
    data.setdefault("daily_programs", {})
    return data

def save_data():
    with open(FILE_PATH, "w") as f:
        json.dump(st.session_state.data, f)

def show():
    st.title("Sport Section")

    # Session state setup
    if "data" not in st.session_state:
        st.session_state.data = load_data()

    # daily schedule
    st.subheader("Daily Program")
    selected_day = st.date_input("Select date", date.today())
    day_key = str(selected_day)

    if day_key not in st.session_state.data["daily_programs"]:
        st.session_state.data["daily_programs"][day_key] = EXERCISES.copy()

    # Add new gesture
    new_ex = st.text_input("Add new exercise to today's program:")
    if st.button("Add Exercise"):
        if new_ex.strip():
            ex_name = new_ex.strip()
            st.session_state.data["daily_programs"][day_key].append(ex_name)
            # Add to records section
            st.session_state.data["records"].setdefault(ex_name, [])
            save_data()
            st.rerun()

    # Show current transactions with checkbox + delete button
    st.write("Today's Exercises:")
    exercises_copy = st.session_state.data["daily_programs"][day_key].copy()
    for idx, ex in enumerate(exercises_copy):
        cols = st.columns([0.8, 0.2])
        done = cols[0].checkbox(ex, key=f"{day_key}_{idx}")
        if cols[1].button("Delete", key=f"del_{day_key}_{idx}"):
            st.session_state.data["daily_programs"][day_key].pop(idx)
            
            st.session_state.data["records"].pop(ex, None)
            save_data()
            st.rerun()

    st.markdown("---")

    # records
    st.subheader("Records")

    # Dropdown: all recorded moves + newly added moves
    all_exercises = list(st.session_state.data["records"].keys())
    ex_choice = st.selectbox("Select Exercise:", all_exercises)

    weight = st.number_input(f"Enter max weight for {ex_choice} (kg):", min_value=0.0, step=0.5)

    if st.button("Save Record", key=f"save_{ex_choice}_{selected_day}"):
        if weight > 0:
            st.session_state.data["records"].setdefault(ex_choice, []).append({
                "date": str(selected_day),
                "weight": weight
            })
            save_data()
            st.rerun()

    # Show and delete existing records
    if st.session_state.data["records"].get(ex_choice):
        records_copy = st.session_state.data["records"][ex_choice].copy()
        for idx, rec in enumerate(records_copy):
            cols = st.columns([0.8, 0.2])
            cols[0].write(f"{rec['date']}: {rec['weight']} kg")
            if cols[1].button("Delete", key=f"del_record_{ex_choice}_{idx}"):
                st.session_state.data["records"][ex_choice].pop(idx)
                save_data()
                st.rerun()

        # graph
        st.subheader("📊 Progress Graph")
        df = pd.DataFrame(st.session_state.data["records"][ex_choice])
        df["date"] = pd.to_datetime(df["date"])
        chart = alt.Chart(df).mark_line(point=True).encode(
            x="date:T",
            y="weight:Q"
        ).properties(
            width=700,
            height=400,
            title=f"{ex_choice} Progress Over Time"
        )
        st.altair_chart(chart)
    else:
        st.info("No records yet for this exercise.")
