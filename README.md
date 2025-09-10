# Persona

**Persona** is a comprehensive personal tracking application built with **Streamlit**. It allows you to monitor and manage your lifestyle, fitness, nutrition, entertainment, and investments all in one place.

---

## 🚀 Features

### 1️⃣ Movie & Series Tracking
- Add movies or TV series you've watched.
- Rate them using a flexible numeric rating (supports decimal values, e.g., 3.5).
- Optional notes for each entry.
- Delete entries easily.
- Organized display for movies and series separately.

### 2️⃣ Daily Workout & Records
- Track your daily workout routines.
- Add exercises to your daily program.
- Log your records for each exercise (weight lifted, repetitions, etc.).
- Visualize progress with charts.
- Easily delete exercises or records.
- All data is saved persistently using JSON files.

### 3️⃣ Nutrition & Hydration
- Input your weight, height, and goal type (Bulk, Cut, Maintenance).
- Calculate daily requirements for:
  - Water intake
  - Protein
  - Carbohydrates
  - Fats
- Pie chart visualization for macronutrient distribution.
- Designed as daily goals – no persistent storage needed.

### 4️⃣ Investment Portfolio
- Track stocks, cryptocurrencies, and gold assets.
- Input asset type, symbol, amount, and optional notes.
- View portfolio in a clean 3-column layout:
  - Asset name & type
  - Amount & notes
  - Delete button
- Predict future prices using simple linear regression.
- Display historical and predicted data in an Altair chart.
- Calculate and display **total portfolio value in USD**.
- ⚠️ Includes a clear disclaimer: predictions are for educational purposes only and **not financial advice**.

---

## 💻 Installation

1. Clone the repository:

```bash
git clone https://github.com/<your_username>/Persona.git
```
2. cd Persona
```bash
pip install -r requirements.txt

streamlit run app.py
```

## 🎯 Notes

All personal data is stored locally in JSON files.

The application is designed to be simple, interactive, and educational.

Predictions in the Investment section are for learning purposes only.

## 💡 Future Improvements

Add authentication to support multiple users.

Include more advanced financial models for investments.

Add reminders and notifications for workouts and nutrition.


Enhance visualization with more charts and interactive dashboards.

