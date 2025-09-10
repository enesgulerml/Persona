import streamlit as st
import pandas as pd
import altair as alt

def calculate_macros(weight, height, age, gender, activity, goal):
    # BMR Calculation
    if gender == "Male":
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

    # Activity coefficient
    activity_factors = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }
    tdee = bmr * activity_factors[activity]

    # Calorie and protein adjustment according to target
    if goal == "Bulk":
        calories = tdee * 1.15
        protein = 1.8 * weight
    elif goal == "Cut":
        calories = tdee * 0.8
        protein = 2.2 * weight
    else:  # Maintain
        calories = tdee
        protein = 1.6 * weight

    # Macros
    fat = 0.9 * weight
    carbs = (calories - (protein * 4 + fat * 9)) / 4
    water = weight * 35 / 1000  # liter

    return {
        "Calories": round(calories),
        "Protein (g)": round(protein),
        "Fat (g)": round(fat),
        "Carbs (g)": round(carbs),
        "Water (L)": round(water, 2)
    }

def show():
    st.title("Nutrition & Hydration Calculator")

    # User inputs
    weight = st.number_input("Weight (kg):", min_value=30, max_value=200, value=70)
    height = st.number_input("Height (cm):", min_value=120, max_value=220, value=175)
    age = st.number_input("Age:", min_value=10, max_value=80, value=25)
    gender = st.selectbox("Gender:", ["Male", "Female"])
    activity = st.selectbox("Activity Level:", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    goal = st.selectbox("Goal:", ["Bulk", "Cut", "Maintain"])

    if st.button("Calculate"):
        result = calculate_macros(weight, height, age, gender, activity, goal)

        # Show results in tabular form
        st.subheader("Your Daily Targets")
        st.table(pd.DataFrame([result]))

        # Data for Pie Chart
        macro_data = pd.DataFrame({
            "Macro": ["Protein", "Fat", "Carbs"],
            "Grams": [result["Protein (g)"], result["Fat (g)"], result["Carbs (g)"]]
        })

        # Pie Chart
        chart = alt.Chart(macro_data).mark_arc().encode(
            theta="Grams",
            color="Macro",
            tooltip=["Macro", "Grams"]
        ).properties(
            width=400,
            height=400,
            title="Macronutrient Distribution"
        )

        st.altair_chart(chart, use_container_width=True)

        # Let's also show the amount of water
        st.info(f"You should drink about **{result['Water (L)']} L** of water per day.")

