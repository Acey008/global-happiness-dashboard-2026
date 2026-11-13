# Global Happiness & Quality of Life Dashboard 2026

## Project Overview

An interactive data analytics dashboard examining
cross-country happiness scores and associated
quality-of-life indicators.

## Objectives

- Examine global happiness score distributions
- Compare country-level happiness scores
- Explore relationships between happiness and
  selected quality-of-life indicators
- Present findings through interactive visualisations

## Tools and Technologies

Python, Pandas, Plotly, Streamlit, Google Colab

## Dashboard Features

- Interactive world map
- Country rankings
- Happiness score distribution
- Pearson correlation heatmap
- Indicator scatter plots
- Country comparisons
- Interactive country filters
- Downloadable filtered data

## Dataset

Source: World Happiness Update Report 2026

https://www.kaggle.com/datasets/jummanalnahian/world-happiness-update-report-2026

The original dataset contains 147 records.

## Data Quality

The source contains 17 country names appearing twice
with conflicting scores and indicator values.

Both records for each affected country were excluded
from the dashboard dataset.

The retained dataset contains 113 countries.

Analysis ranks were recalculated within this subset
and must not be interpreted as official global ranks.

Excluded records are preserved separately for review.

## Methodology

Exploratory data analysis, descriptive statistics,
country comparisons and Pearson correlation analysis.

The dataset represents a single reporting year.
Correlations are associations, not causal evidence.

## Run Locally

Install dependencies:

pip install -r requirements.txt

Launch the application:

streamlit run app.py

## Project Structure

app.py
requirements.txt
happiness_2026_clean.csv
excluded_country_records.csv
README.md

## Limitations

- Conflicting source records affect country coverage.
- Original data provenance requires further verification.
- Country indicators require source-specific interpretation.
- Results cannot establish causation or temporal trends.
