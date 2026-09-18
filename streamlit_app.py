import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="World & Animal Population Explorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# Data loading (cached so it only runs once)
# ----------------------------------------------------------------------
@st.cache_data
def load_population():
    return pd.read_csv("data/population.csv")

@st.cache_data
def load_animals():
    return pd.read_csv("data/animal.csv")

pop_df = load_population()
animal_df = load_animals()

# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
st.sidebar.title("🌍 Controls")
view = st.sidebar.radio(
    "Choose a view",
    ["Human Population", "Animal Population", "About"],
)

st.sidebar.markdown("---")
st.sidebar.caption("Starter kit • Replace the CSVs in /data with your own data.")

# ----------------------------------------------------------------------
# HUMAN POPULATION VIEW
# ----------------------------------------------------------------------
if view == "Human Population":
    st.title("🌍 World Human Population")

    col1, col2, col3 = st.columns(3)
    total_pop = pop_df["population"].sum()
    col1.metric("Total Population", f"{total_pop/1e9:.2f} B")
    col2.metric("Countries", f"{pop_df['country'].nunique()}")
    col3.metric("Most Populous", pop_df.loc[pop_df['population'].idxmax(), 'country'])

    st.subheader("Population by Country (Map)")
    fig_map = px.choropleth(
        pop_df,
        locations="iso_code",
        color="population",
        hover_name="country",
        color_continuous_scale="Viridis",
        projection="natural earth",
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("Top 10 Most Populous Countries")
    top10 = pop_df.nlargest(10, "population")
    fig_bar = px.bar(
        top10.sort_values("population"),
        x="population",
        y="country",
        orientation="h",
        color="population",
        color_continuous_scale="Blues",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    with st.expander("View raw data"):
        st.dataframe(pop_df, use_container_width=True)

# ----------------------------------------------------------------------
# ANIMAL POPULATION VIEW
# ----------------------------------------------------------------------
elif view == "Animal Population":
    st.title("🐾 Animal Population by Region")

    regions = st.multiselect(
        "Filter by region",
        options=sorted(animal_df["region"].unique()),
        default=sorted(animal_df["region"].unique()),
    )
    filtered = animal_df[animal_df["region"].isin(regions)]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Population by Animal")
        fig_animal = px.bar(
            filtered.groupby("animal", as_index=False)["population"].sum(),
            x="animal",
            y="population",
            color="animal",
        )
        st.plotly_chart(fig_animal, use_container_width=True)

    with col2:
        st.subheader("Share by Region")
        fig_pie = px.pie(
            filtered,
            names="region",
            values="population",
            hole=0.4,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Animal Distribution Across Regions")
    fig_sun = px.sunburst(
        filtered,
        path=["region", "animal"],
        values="population",
        color="region",
    )
    st.plotly_chart(fig_sun, use_container_width=True)

    with st.expander("View raw data"):
        st.dataframe(filtered, use_container_width=True)

# ----------------------------------------------------------------------
# ABOUT VIEW
# ----------------------------------------------------------------------
else:
    st.title("About this app")
    st.markdown(
        """
        This is a **Streamlit starter kit** that visualizes:

        - 🌍 **World human population** by country (map + charts)
        - 🐾 **Animal populations** across different regions of the globe

        ### How to customize
        1. Replace `data/population.csv` and `data/animals.csv` with your own datasets.
        2. Keep the same column names, or update the code accordingly.
        3. Push to GitHub and redeploy.

        Built with [Streamlit](https://streamlit.io) and [Plotly](https://plotly.com/python/).
        """
    )
