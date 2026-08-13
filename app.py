import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Netflix Movie Analytics",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Netflix Movie Analytics Dashboard")
st.write("Interactive analysis of Netflix movie data")

# Upload dataset
uploaded_file = st.file_uploader(
    "Upload Netflix CSV file",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Please upload the Netflix CSV dataset to start.")
    st.stop()

df = pd.read_csv(uploaded_file)

# Basic cleaning
df = df.dropna(subset=["Title"])

if "Genre" in df.columns:
    df["Genre"] = df["Genre"].fillna("Unknown")

# Sidebar filters
st.sidebar.header("🔎 Filters")

if "Release_Date" in df.columns:
    years = sorted(df["Release_Date"].dropna().unique())
    selected_years = st.sidebar.multiselect(
        "Release Year",
        years,
        default=years
    )
    df = df[df["Release_Date"].isin(selected_years)]

if "Genre" in df.columns:
    genres = sorted(df["Genre"].dropna().unique())
    selected_genres = st.sidebar.multiselect(
        "Genre",
        genres,
        default=genres
    )
    df = df[df["Genre"].isin(selected_genres)]

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("🎬 Total Titles", df["Title"].nunique())

if "Popularity" in df.columns:
    col2.metric(
        "🔥 Highest Popularity",
        round(df["Popularity"].max(), 2)
    )

if "Vote_Count" in df.columns:
    col3.metric(
        "🗳️ Total Votes",
        int(df["Vote_Count"].sum())
    )

if "Genre" in df.columns:
    col4.metric(
        "🎭 Genres",
        df["Genre"].nunique()
    )

st.divider()

# Top movies
st.subheader("🔥 Most Popular Movies")

if "Popularity" in df.columns:
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
        orientation="h",
        title="Top 10 Movies by Popularity"
    )

    st.plotly_chart(fig, use_container_width=True)

# Genre analysis
if "Genre" in df.columns:
    st.subheader("🎭 Genre Distribution")

    genre_count = (
        df["Genre"]
        .value_counts()
        .reset_index()
    )

    genre_count.columns = ["Genre", "Count"]

    fig = px.bar(
        genre_count.head(15),
        x="Genre",
        y="Count",
        title="Most Frequent Genres"
    )

    st.plotly_chart(fig, use_container_width=True)

# Release year
if "Release_Date" in df.columns:
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
        markers=True,
        title="Movies Released by Year"
    )

    st.plotly_chart(fig, use_container_width=True)

# Vote average
if "Vote_Average" in df.columns:
    st.subheader("⭐ Vote Distribution")

    vote_count = (
        df["Vote_Average"]
        .value_counts()
        .reset_index()
    )

    vote_count.columns = ["Vote_Average", "Count"]

    fig = px.bar(
        vote_count,
        x="Vote_Average",
        y="Count",
        title="Vote Average Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# Search
st.subheader("🔍 Search Movies")

search = st.text_input("Enter movie title")

if search:
    result = df[
        df["Title"]
        .astype(str)
        .str.contains(search, case=False, na=False)
    ]

    st.dataframe(
        result,
        use_container_width=True
    )

# Raw data
with st.expander("📊 View Dataset"):
    st.dataframe(df, use_container_width=True)