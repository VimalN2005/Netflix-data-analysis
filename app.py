 import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Netflix Movie Analytics",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Netflix Movie Analytics Dashboard")
st.write("Interactive analysis of movie data")

uploaded_file = st.file_uploader(
    "Upload Movie Dataset (CSV)",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Please upload your CSV dataset to start.")
    st.stop()

# Read CSV safely
try:
    df = pd.read_csv(uploaded_file)
except UnicodeDecodeError:
    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file, encoding="latin1")
except pd.errors.ParserError:
    uploaded_file.seek(0)
    df = pd.read_csv(
        uploaded_file,
        encoding="latin1",
        on_bad_lines="skip"
    )

st.success("Dataset loaded successfully!")

# Show columns
st.sidebar.header("🔎 Filters")

# Convert Release_Date to numeric if present
if "Release_Date" in df.columns:
    df["Release_Date"] = pd.to_numeric(
        df["Release_Date"],
        errors="coerce"
    )

    years = sorted(
        df["Release_Date"]
        .dropna()
        .unique()
    )

    if years:
        selected_years = st.sidebar.multiselect(
            "Release Year",
            years,
            default=years
        )

        df = df[
            df["Release_Date"].isin(selected_years)
        ]

# Genre filter
if "Genre" in df.columns:

    df["Genre"] = df["Genre"].fillna("Unknown")

    genres = sorted(
        df["Genre"]
        .astype(str)
        .unique()
    )

    selected_genres = st.sidebar.multiselect(
        "Genre",
        genres,
        default=genres
    )

    df = df[
        df["Genre"].astype(str).isin(selected_genres)
    ]

# KPIs
col1, col2, col3, col4 = st.columns(4)

if "Title" in df.columns:
    col1.metric("🎬 Total Titles", df["Title"].nunique())
else:
    col1.metric("📊 Total Rows", len(df))

if "Popularity" in df.columns:
    col2.metric(
        "🔥 Highest Popularity",
        round(
            pd.to_numeric(
                df["Popularity"],
                errors="coerce"
            ).max(),
            2
        )
    )

if "Vote_Count" in df.columns:
    col3.metric(
        "🗳️ Total Votes",
        int(
            pd.to_numeric(
                df["Vote_Count"],
                errors="coerce"
            ).fillna(0).sum()
        )
    )

if "Genre" in df.columns:
    col4.metric(
        "🎭 Genres",
        df["Genre"].nunique()
    )

st.divider()

# Most popular movies
if "Title" in df.columns and "Popularity" in df.columns:

    st.subheader("🔥 Top 10 Movies by Popularity")

    df["Popularity"] = pd.to_numeric(
        df["Popularity"],
        errors="coerce"
    )

    top_movies = (
        df.groupby("Title", as_index=False)["Popularity"]
        .max()
        .sort_values("Popularity", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_movies,
        x="Popularity",
        y="Title",
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)

# Genre distribution
if "Genre" in df.columns:

    st.subheader("🎭 Genre Distribution")

    genre_count = (
        df["Genre"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    genre_count.columns = ["Genre", "Count"]

    fig = px.bar(
        genre_count,
        x="Genre",
        y="Count"
    )

    st.plotly_chart(fig, use_container_width=True)

# Movies by year
if "Release_Date" in df.columns and "Title" in df.columns:

    st.subheader("📅 Movies by Release Year")

    yearly = (
        df.groupby("Release_Date")["Title"]
        .nunique()
        .reset_index()
    )

    yearly.columns = ["Release_Date", "Movies"]

    fig = px.line(
        yearly,
        x="Release_Date",
        y="Movies",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

# Search
if "Title" in df.columns:

    st.subheader("🔍 Search Movie")

    search = st.text_input("Enter movie title")

    if search:

        result = df[
            df["Title"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

        st.dataframe(
            result,
            use_container_width=True
        )

# Dataset preview
with st.expander("📊 View Dataset"):
    st.dataframe(df, use_container_width=True)