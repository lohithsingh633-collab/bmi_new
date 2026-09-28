import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="⚖️",
    layout="centered"
)

# File used to store records
DATA_FILE = Path("bmi_records.csv")

# ---------------------------------------------------------
# Functions
# ---------------------------------------------------------
def calculate_bmi(weight_kg, height_cm):
    """Calculate BMI using weight in kg and height in cm."""
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)


def get_bmi_category(bmi):
    """Return the adult BMI category."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def get_meal_plan(category):
    """Return general, non-medical meal suggestions."""
    plans = {
        "Underweight": {
            "Breakfast": "Oats with milk/curd, banana, nuts and seeds",
            "Mid-morning": "Fruit + handful of nuts",
            "Lunch": "Rice/roti + dal + vegetables + curd + paneer/egg/chicken",
            "Evening": "Milk or smoothie + roasted chana",
            "Dinner": "Roti/rice + vegetables + dal/paneer/lean protein",
        },
        "Normal": {
            "Breakfast": "Vegetable upma/poha or oats + fruit",
            "Mid-morning": "One fruit",
            "Lunch": "Roti/rice + dal + vegetables + curd + protein",
            "Evening": "Buttermilk/tea without excess sugar + nuts",
            "Dinner": "Roti + vegetables + dal/paneer/lean protein",
        },
        "Overweight": {
            "Breakfast": "Vegetable oats/poha/upma + protein such as eggs or curd",
            "Mid-morning": "Whole fruit",
            "Lunch": "More vegetables + dal/protein + moderate rice/roti + curd",
            "Evening": "Buttermilk or unsweetened tea + a small portion of nuts",
            "Dinner": "Vegetables + dal/paneer/lean protein + moderate roti",
        },
        "Obese": {
            "Breakfast": "Vegetable oats/poha + eggs/curd or another protein source",
            "Mid-morning": "Whole fruit",
            "Lunch": "Large serving of vegetables + dal/lean protein + controlled portion of rice/roti",
            "Evening": "Buttermilk/unsweetened beverage + small portion of nuts",
            "Dinner": "Vegetables + dal/lean protein + controlled portion of roti",
        },
    }
    return plans[category]


def get_exercises(category):
    """Return light/general exercise suggestions."""
    exercises = {
        "Underweight": [
            "10–20 minutes of easy walking",
            "Light stretching",
            "Beginner bodyweight exercises 2–3 times/week",
        ],
        "Normal": [
            "20–30 minutes of brisk walking",
            "Light stretching or yoga",
            "Basic strength exercises 2–3 times/week",
        ],
        "Overweight": [
            "20–30 minutes of comfortable-paced walking",
            "Light cycling if comfortable",
            "Gentle stretching or beginner yoga",
        ],
        "Obese": [
            "Start with 10–15 minutes of comfortable walking",
            "Chair-based or low-impact exercises",
            "Gentle stretching; gradually increase duration",
        ],
    }
    return exercises[category]


def load_records():
    """Load saved records if the CSV exists."""
    if DATA_FILE.exists():
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame()


def save_record(record):
    """Append one BMI record to the CSV file."""
    new_record = pd.DataFrame([record])

    if DATA_FILE.exists():
        existing = pd.read_csv(DATA_FILE)
        updated = pd.concat([existing, new_record], ignore_index=True)
    else:
        updated = new_record

    updated.to_csv(DATA_FILE, index=False)


# ---------------------------------------------------------
# App UI
# ---------------------------------------------------------
st.title("⚖️ BMI Calculator & Wellness Guide")
st.write("Calculate BMI, view a general category, and get simple meal and activity suggestions.")

st.info(
    "This app is intended for adults aged 18+. BMI is a screening measure and "
    "does not diagnose health conditions. Meal and exercise suggestions are general "
    "educational information, not medical advice."
)

tab1, tab2 = st.tabs(["🧮 BMI Calculator", "📋 Saved Records"])

# ---------------------------------------------------------
# Calculator tab
# ---------------------------------------------------------
with tab1:
    st.subheader("Enter your details")

    with st.form("bmi_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=18, max_value=120, value=25, step=1)
        gender = st.selectbox("Gender", ["Female", "Male", "Other / Prefer not to say"])
        height = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            value=165.0,
            step=0.5
        )
        weight = st.number_input(
            "Weight (kg)",
            min_value=10.0,
            max_value=300.0,
            value=60.0,
            step=0.5
        )

        submitted = st.form_submit_button("Calculate BMI")

    if submitted:
        if not name.strip():
            st.error("Please enter your name.")
        else:
            bmi = calculate_bmi(weight, height)
            category = get_bmi_category(bmi)

            st.success(f"Hello {name}! Your BMI calculation is complete.")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("BMI", f"{bmi:.2f}")
            with col2:
                st.metric("Category", category)

            st.divider()

            st.subheader("🍽️ General Meal Suggestions")

            meal_plan = get_meal_plan(category)

            for meal, suggestion in meal_plan.items():
                st.markdown(f"**{meal}:** {suggestion}")

            st.subheader("🚶 Light Exercise Suggestions")

            for exercise in get_exercises(category):
                st.write(f"• {exercise}")

            # Save record
            record = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Name": name.strip(),
                "Age": int(age),
                "Gender": gender,
                "Height_cm": height,
                "Weight_kg": weight,
                "BMI": round(bmi, 2),
                "Category": category,
            }

            save_record(record)
            st.success("✅ Your record has been saved.")

# ---------------------------------------------------------
# Saved records tab
# ---------------------------------------------------------
with tab2:
    st.subheader("Saved BMI Records")

    records = load_records()

    if records.empty:
        st.info("No records have been saved yet.")
    else:
        st.dataframe(records, use_container_width=True)

        csv_data = records.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Records as CSV",
            data=csv_data,
            file_name="bmi_records_backup.csv",
            mime="text/csv"
        )

        st.caption(f"Total saved records: {len(records)}")
