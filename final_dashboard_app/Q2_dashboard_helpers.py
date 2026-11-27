"""
dashboard_helpers.py (dashboard/dashboard_helpers.py)

This file contains:
1. the data logic (filter_data, trendlines, correlation, coverage) 
2. plot creation (create_scatterplot)

** for Q2 (Education and Health Outcomes) of the Project **
"""


""" SECTION 0. IMPORT statements """
# %pip install statsmodels
# %pip install ipywidgets


import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm # for trendline
# import ipywidgets as widgets      # DELETED - was used in mockups





""" SECTION 1. variable groups """
# 1.1. education vars (x-axis)
education_vars = [
    "literacy_rate",
    "primary_enrollment",
    "prog_to_secondary",
    "secondary_enrollment"
]

# 1.2. health vars (y-axis)
health_vars = [
    "life_expectancy",
    "infant_mortality",
    "under5_mortality"
]

# 1.3. Compute global range (xmin, xmax, ymin, ymax) per variable
#   PURPOSE: so that the axes remain stable whilst the points move across time
def compute_axis_ranges(
    df, 
    x_vars, 
    y_vars, 
):
    axis_ranges = {}

    for col in x_vars + y_vars:
        series = df[col].dropna()
        axis_ranges[col] = (
            series.min(),
            series.max()
        )

    return axis_ranges      # NOTE: compute_axis_ranges(...) will be called in the make_plot() function






""" SECTION 2. DATA-LOGIC Functions (filter_data, trendlines, correlation, coverage) """

# 2.1. filter_data()
#   display only data for the selected year and region
def filter_data(df, year, include_east, include_southeast):
    # 1.1. Include only selected regions (E/SE Asia)
    selected_regions = []
    if include_east:
        selected_regions.append("East Asia")
    if include_southeast:
        selected_regions.append("Southeast Asia")

    # 1.2. Filter data by year and selected region
    filtered_df = df[
        (df["Year"] == year)
        &
        (df["region"].isin(selected_regions))
    ].copy()

    return filtered_df



# 2.2. classify_correlation()
def classify_correlation(r):
    magnitude = abs(r)

    if magnitude < 0.2:
        return "Very Weak"

    elif magnitude < 0.4:
        return "Weak"

    elif magnitude < 0.6:
        return "Moderate"

    elif magnitude < 0.8:
        return "Strong"

    return "Very Strong"



# 2.3. coverage_details()
#   "What % of total countries have non-null data for this selection (year, x-metric, y-metric)?"
#   Returns: a 3-item tuple (% coverage, "_[desc]__ Coverage", "color_of_banner")
def coverage_details(data, variable):

    # 1. Total data 
    total = len(data)
    if total == 0:
        return (0, "No data", "danger")

    # 2. Non-null data
    available = data[variable].notna().sum()
    pct = available / total

    # 3. Return appropriate label
    if pct >= 0.80:
        return (pct, "Good Coverage", "success")
    elif pct >= 0.40:
        return (pct, "Limited Coverage", "warning")
    else:
        return (pct, "Sparse Coverage", "danger")



# 2.4. can_fit_trendline() - 
#   GUARD against empty-exceptions when no countries data for certain year/metric combinations
def can_fit_trendline(
    plot_df,
    x_var,
    y_var
):
    """
    Determine whether there is enough valid data
    to fit an OLS regression line.
    """

    trend_df = plot_df[
        [x_var, y_var]
    ].dropna()

    # Need at least 3 observations
    if len(trend_df) < 3:
        return False

    # Need at least 2 distinct x values
    if trend_df[x_var].nunique() < 2:
        return False

    return True



# 2.5. can_compute_correlation
#   GUARD against empty-exceptions when no countries data for certain year/metric combinations
#   how: by checking if there are enough non-null x and y for this year/metric combination
def can_compute_correlation(
    plot_df,
    x_var,
    y_var
):

    corr_df = plot_df[
        [x_var, y_var]
    ].dropna()

    if len(corr_df) < 3:
        return False

    if corr_df[x_var].nunique() < 2:
        return False

    if corr_df[y_var].nunique() < 2:
        return False

    return True



# 2.6. fit_regression_line_to_fig()
def fit_regression_line_to_fig(
    fig, plot_df, x_var, y_var, x_min, x_max
):
    # 5.1. Check if there are enough valid data points for selected year + metrics
    if not can_fit_trendline(
        plot_df, x_var, y_var
    ):
        fig.add_annotation(
            text="Not enough data to fit trendline",
            xref="paper",
            yref="paper",
            x=0.5,
            y=1.05,
            showarrow=False,
            font=dict(
                color="red",
                size=12
            )
        )

        return fig

    # 5.3. Fit one regression line across all displayed countries
    trend_df = plot_df[[x_var, y_var]].dropna()
    x = trend_df[x_var]
    y = trend_df[y_var]

    # 5.4. create OLS regression
    X_model = sm.add_constant(x)
    model = sm.OLS(y, X_model).fit()
    # print(model.summary())  # summarise model

    # 5.5. Plot line: Generate x-range
    x_line = np.linspace(
        x_min,
        x_max,
        100 # multiply decimals by 100 to get percents
    )

    # 5.6. Generate y-predictions
    X_line = sm.add_constant(x_line)    # add bias (y-intercept)
    y_pred = model.predict(X_line)

    # 5.7. Add the all-country trendline (includes all income levels) to the scatterplot
    fig.add_scatter(
        x=x_line,
        y=y_pred,
        mode="lines",
        name="Overall Trend",
        line=dict(
            color="gray",
            dash="dash",
            width=2,
        )
    )

    return fig



# 2.7. create_scatterplot()
#   DESC: Helper function to plot the scatterplot and best-fit line
def create_scatterplot(filtered_df, x_var, y_var, color_var, year, axis_ranges):
    # 17.3. PLOT the actual scatterplot
    fig = px.scatter(
        filtered_df,
        x = x_var,
        y = y_var,
        color = color_var,
        hover_name="Country Name",
        hover_data=[
            "region",
            "income",
            x_var,
            y_var,
        ],
        title=f"{x_var} vs {y_var} ({year})",
        # trendline="ols"
    )

    # 17.3. Fix the axes to a reasonable range, so that points move (instead of axes)
    xmin, xmax = axis_ranges[x_var]
    ymin, ymax = axis_ranges[y_var]
    padding_x = (xmax - xmin) * 0.05  # add 5% padding
    fig.update_xaxes(
        range=[xmin - padding_x, xmax + padding_x],
    )

    padding_y = (ymax - ymin) * 0.05
    fig.update_yaxes(
        range=[ymin - padding_y, ymax + padding_y]
    )

    # 17.4. Add improved (nice) labels to the axes
    label_map = {
        "literacy_rate": "Literacy Rate (%)",
        "primary_enrollment": "Primary Enrollment (%)",
        "prog_to_secondary": "Progression to Secondary (%)",
        "secondary_enrollment": "Secondary Enrollment (%)",
        "life_expectancy": "Life Expectancy (Years)",
        "infant_mortality": "Infant Mortality (per 1000)",
        "under5_mortality": "Under-5 Mortality (per 1000)",
    }
    fig.update_layout(  # map raw (csv) col-labels to readable ones
        xaxis_title=label_map[x_var],
        yaxis_title=label_map[y_var],
        title=f"{label_map[x_var]} vs {label_map[y_var]} ({year})",

        # reasonable height and width constraints
        # height=700,
        # width=1000,
    )

    # 17.5. Fit a regression line (helper function above)
    fig = fit_regression_line_to_fig(fig, filtered_df, x_var, y_var, xmin, xmax)

    return fig  # for further modification (common pattern in Python data viz)


