## 1. Git Repo for Project 2:
DS-2003-Group-Project-Dashboard-Repo

## 2. Project 2: Data Contract

- Data contract: data/clean/panel_1980_2010.parquet has one row per (Country Name, Country Code, Year) for 15 countries × 1980–2020 (expanded since certain data is only covered after 2000). 

- Columns include life_expectancy, infant_mortality, under5_mortality, secondary_enrollment, primary_enrollment, literacy_rate, adolescent_fertility, sanitation_basic_pct, water_basic_pct, water_safe_pct, gdp_per_capita_const2010usd. 

- Missing values are NaN — filter with dropna(subset=[...]) at render time.