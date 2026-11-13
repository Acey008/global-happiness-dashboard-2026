
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Global Happiness Dashboard 2026",
    page_icon="🌍",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("happiness_2026_clean.csv")

df = load_data()

indicators = [
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "generosity",
    "corruption"
]

st.title("Global Happiness & Quality of Life Dashboard")
st.caption("2026 | Cross-Country Exploratory Analysis")

st.info(
    "Data-quality note: 17 countries with conflicting "
    "duplicate observations were excluded. "
    "Results cover 113 countries, not the full original "
    "147-record dataset. Rankings are recalculated "
    "within the retained sample."
)

st.sidebar.header("Dashboard Filters")

selected_countries = st.sidebar.multiselect(
    "Select countries",
    sorted(df["country"].unique()),
    default=sorted(df["country"].unique())
)

filtered = df[df["country"].isin(selected_countries)]

if filtered.empty:
    st.warning("Select at least one country.")
    st.stop()

# -------------------------------------------------------------------------
# OVERVIEW METRICS
# -------------------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Countries", len(filtered))
col2.metric("Average Happiness", f"{filtered['score'].mean():.2f}")
col3.metric("Highest Score", f"{filtered['score'].max():.2f}")
col4.metric("Lowest Score", f"{filtered['score'].min():.2f}")

# -------------------------------------------------------------------------
# INTERACTIVE WORLD MAP
# -------------------------------------------------------------------------

st.subheader("Global Happiness Distribution")

fig_map = px.choropleth(
    filtered,
    locations="country",
    locationmode="country names",
    color="score",
    hover_name="country",
    hover_data=["analysis_rank"],
    color_continuous_scale="Tealgrn",
    projection="natural earth",
    labels={"score": "Happiness Score"}
)

fig_map.update_layout(
    height=550,
    margin=dict(l=0, r=0, t=10, b=0)
)

st.plotly_chart(fig_map, use_container_width=True)

# -------------------------------------------------------------------------
# COUNTRY RANKINGS
# -------------------------------------------------------------------------

st.subheader("Country Rankings")

left, right = st.columns(2)

top_countries = filtered.nlargest(10, "score")
bottom_countries = filtered.nsmallest(10, "score")

with left:
    fig_top = px.bar(
        top_countries.sort_values("score"),
        x="score",
        y="country",
        orientation="h",
        title="Top 10 Countries",
        color="score",
        color_continuous_scale="Tealgrn"
    )
    st.plotly_chart(fig_top, use_container_width=True)

with right:
    fig_bottom = px.bar(
        bottom_countries.sort_values("score"),
        x="score",
        y="country",
        orientation="h",
        title="Bottom 10 Countries",
        color="score",
        color_continuous_scale="OrRd"
    )
    st.plotly_chart(fig_bottom, use_container_width=True)

# -------------------------------------------------------------------------
# HAPPINESS SCORE DISTRIBUTION
# -------------------------------------------------------------------------

st.subheader("Distribution of Happiness Scores")

fig_hist = px.histogram(
    filtered,
    x="score",
    nbins=15,
    marginal="box",
    title="Happiness Score Distribution",
    labels={"score": "Happiness Score"}
)

st.plotly_chart(fig_hist, use_container_width=True)

# -------------------------------------------------------------------------
# CORRELATION ANALYSIS
# -------------------------------------------------------------------------

st.subheader("Correlation Analysis")

corr = filtered[indicators + ["score"]].corr()

fig_corr = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1,
    title="Pearson Correlation Matrix"
)

st.plotly_chart(fig_corr, use_container_width=True)

indicator = st.selectbox(
    "Select an indicator to examine",
    indicators
)

fig_scatter = px.scatter(
    filtered,
    x=indicator,
    y="score",
    hover_name="country",
    title=f"{indicator.replace('_', ' ').title()} vs Happiness Score",
    labels={"score": "Happiness Score"}
)

st.plotly_chart(fig_scatter, use_container_width=True)

# -------------------------------------------------------------------------
# COUNTRY COMPARISON
# -------------------------------------------------------------------------

st.subheader("Country Comparison")

comparison = st.multiselect(
    "Select countries to compare",
    sorted(df["country"].unique()),
    default=[
        country for country in
        ["Finland", "Denmark", "India", "United Kingdom"]
        if country in df["country"].values
    ]
)

comparison_data = df[df["country"].isin(comparison)]

if not comparison_data.empty:
    fig_compare = px.bar(
        comparison_data,
        x="country",
        y="score",
        color="country",
        title="Happiness Score by Country"
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    st.dataframe(
        comparison_data[
            ["country", "analysis_rank", "score"] + indicators
        ],
        use_container_width=True,
        hide_index=True
    )

# -------------------------------------------------------------------------
# DATA EXPLORER AND DOWNLOAD
# -------------------------------------------------------------------------

st.subheader("Explore the Dataset")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    label="Download Filtered Dataset",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_happiness_2026.csv",
    mime="text/csv"
)

# -------------------------------------------------------------------------
# METHODOLOGY
# -------------------------------------------------------------------------

with st.expander("Methodology and Limitations"):
    st.markdown("""
    **Dataset:** World Happiness Update Report 2026 (Kaggle).

    **Method:** Cross-sectional descriptive and
    exploratory correlation analysis.

    **Data quality:** The original dataset contained
    147 records representing 130 unique country names.
    Seventeen countries had conflicting observations.
    Both observations for each affected country were
    excluded, leaving 113 countries.

    **Rankings:** Analysis ranks were recalculated
    for the retained sample. They are not official
    global rankings.

    **Interpretation:** Correlation does not establish
    causation. Indicators should not be interpreted
    as literal economic or health measurements without
    verifying their source definitions.

    **Coverage:** The dashboard represents only
    the validated, non-conflicting subset.
    """)

st.caption(
    "Global Happiness & Quality of Life Dashboard | "
    "Data Analytics Portfolio Project"
)
