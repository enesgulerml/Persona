import streamlit as st
from sections import Investment, Movie, Sport, Nutrition

st.set_page_config(page_title="Multi-Section App", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Movie", "Sport", "Nutrition", "Investment"])


if page == "Investment":
    Investment.show()
elif page == "Movie":
    Movie.show()
elif page == "Sport":
    Sport.show()
elif page == "Nutrition":
    Nutrition.show()

