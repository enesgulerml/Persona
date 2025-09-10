import streamlit as st
import json
import os

FILE_PATH = "watched_data.json"

def load_data():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    else:
        return {"movies": [], "series": []}

def save_data():
    with open(FILE_PATH, "w") as f:
        json.dump({
            "movies": st.session_state.watched_movies,
            "series": st.session_state.watched_series
        }, f)

def show():
    st.title("Movie Section")

    # Load data into session state
    data = load_data()
    if "watched_movies" not in st.session_state:
        st.session_state.watched_movies = data["movies"]
    if "watched_series" not in st.session_state:
        st.session_state.watched_series = data["series"]

    # User input
    title = st.text_input("Enter a Movie/Series Name:")
    category = st.selectbox("Choose category:", ["Movie", "Series"])
    rating = st.number_input("Rate (1-5):", min_value=1.0, max_value=5.0, step=0.5, value=3.0)
    note = st.text_area("Optional note:")

    # Add button
    if st.button("Mark as Watched"):
        if title.strip() != "":
            new_entry = {"title": title.strip(), "rating": rating, "note": note.strip()}
            if category == "Movie":
                st.session_state.watched_movies.append(new_entry)
            else:
                st.session_state.watched_series.append(new_entry)
            save_data()
            st.success(f"'{title}' added to {category.lower()} list!")
        else:
            st.warning("Please enter a movie/series name.")

    # Display Movies and Series
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Movies")
        if st.session_state.watched_movies:
            for idx, movie in enumerate(st.session_state.watched_movies):
                st.markdown(f"**{idx+1}. {movie['title']}**")
                st.markdown(f"Rating: {movie['rating']}")
                if movie["note"]:
                    st.caption(f"{movie['note']}")
                if st.button("Delete", key=f"del_movie_{idx}"):
                    st.session_state.watched_movies.pop(idx)
                    save_data()
                    st.rerun()
        else:
            st.info("No movies added yet.")

    with col2:
        st.subheader("Series")
        if st.session_state.watched_series:
            for idx, series in enumerate(st.session_state.watched_series):
                st.markdown(f"**{idx+1}. {series['title']}**")
                st.markdown(f"Rating: {series['rating']}")
                if series["note"]:
                    st.caption(f"{series['note']}")
                if st.button("Delete", key=f"del_series_{idx}"):
                    st.session_state.watched_series.pop(idx)
                    save_data()
                    st.rerun()
        else:
            st.info("No series added yet.")
