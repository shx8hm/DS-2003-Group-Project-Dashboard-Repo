# TODO: Add any imports needed here

from shiny import App, ui, reactive
from shinywidgets import (
    render_plotly,
    output_widget
)




# ============================================================================
# PART 1: GLOBAL STATE (data and helper-functions: for each section/question)
#   1. Read data
#   2. For each question - Import helper functions,  compute axis ranges (of individual attributes)
# ============================================================================


import pandas as pd
# A. Global state: read data (shared across all sections) ONCE, at the beginning.  
df = pd.read_csv(
    "data/panel_1980_2010.csv"
)



# B. Setup each question's state, as necessary
#   (e.g., helper functions, column ranges, etc.)

"""
Q1 State SETUP
"""



"""
Q2 State SETUP
"""
# Q2 state: Import helper functions
from Q2_dashboard_helpers import (
    education_vars,
    health_vars,
    filter_data,
    compute_axis_ranges,
    create_scatterplot
)

# Q2 state:  Compute ranges for each variable (keep plotting consistent)
axis_ranges = compute_axis_ranges(
    df=df,
    x_vars=education_vars,
    y_vars=health_vars
)



"""
Q3 State SETUP
"""



"""
Q4 State SETUP
"""




# ============================================================================
# PART 2: Dashboard Structure (tabbed between: About, Q1, Q2, Q3, Q4)
# ============================================================================
app_ui = ui.page_navbar(

    # ============================================================
    # ABOUT TAB
    # ============================================================

    ui.nav_panel(
        "About",

        ui.h2(
            "Development in East and Southeast Asia, 1980-2019"
        ),

        ui.p(
            """
            Dashboard under development.
            This section will contain dataset information,
            research questions, and key findings.
            """
        )
    ),

    # ============================================================
    # Q1's Tab
    # ============================================================

    ui.nav_panel(
        "Q1",

        ui.h3("Question 1"),

        ui.p("Notebook integration pending")
    ),

    # ============================================================
    # Q2's Tab (Education vs. Health Outcome)
    # ============================================================

    ui.nav_panel(

        "Q2 - Education and Health",

        ui.layout_sidebar(

            ui.sidebar(

                ui.input_slider(
                    "year",
                    "Year",
                    min=1980,
                    max=2019,
                    value=2000
                ),

                ui.input_select(
                    "x_var",
                    "Education Metric (x)",
                    choices=education_vars,
                    selected="secondary_enrollment"
                ),

                ui.input_select(
                    "y_var",
                    "Health Outcome (y)",
                    choices=health_vars,
                    selected="under5_mortality"
                ),

                ui.input_checkbox_group(
                    "regions",
                    "Region",
                    choices=[
                        "East Asia",
                        "Southeast Asia"
                    ],
                    selected=[
                        "East Asia",
                        "Southeast Asia"
                    ]
                ),

                ui.input_radio_buttons(
                    "color_var",
                    "Color Encoding",
                    choices=[
                        "region",
                        "income"
                    ],
                    selected="region"
                )
            ),

            # provide a clean title for Q2's scatterplot
            ui.card(
                ui.card_header(
                    "Interactive Scatter: Education vs Health Outcomes (E / SE Asia)"
                ),

                ui.div(
                    output_widget("Q2_scatterplot"),
                    style="max-width:1200px; margin:auto;"
                )
            )
        )
    ),

    # ============================================================
    # Q3's Tab
    # ============================================================

    ui.nav_panel(
        "Q3 - Sanitation and Health",

        ui.h3("Question 3"),

        ui.p("Notebook integration pending.")
    ),

    # ============================================================
    # Q4's Tab
    # ============================================================

    ui.nav_panel(
        "Q4 - Econ. and Health",

        ui.h3("Question 4"),

        ui.p("Notebook integration pending.")
    ),

    title="Dashboard (E/SE Asia Development; 1980-2019)"
)




# ============================================================================
# PART 3: Dynamic RENDER LOGIC (for Q1, Q2, Q3, and Q4) -
#   Only for pages with interactive visualizations
# ============================================================================
def server(input, output, session):
    """
    QUESTION 1 (dynamic) RENDER LOGIC
    """
    # TODO

    

    """
    QUESTION 2 (dynamic) RENDER LOGIC
    """
    # Q2.1. FILTER DATA: when UI-input-values are changed, re-filter the displayed-data accordingly. 
    @reactive.calc  
    def filtered_data_by_year_region():     # NOTE: This filter() function may be used across Q2-Q4. 
        # invoke dashboard_helpers.filter_data(...) 
        #   a helper function in Q2_dashboard_helpers.py
        return filter_data(
            df,
            year=input.year(),
            include_east="East Asia" in input.regions(),
            include_southeast="Southeast Asia" in input.regions(),
        )
    
    # Q2.2. DISPLAY SCATTER: Render the scatterplot (perhaps again, when the UI values changed)
    @render_plotly
    def Q2_scatterplot():
        fig = create_scatterplot(
            filtered_data_by_year_region(),
            input.x_var(),
            input.y_var(),
            input.color_var(),
            input.year(),
            axis_ranges,
        )
        return fig




    """
    QUESTION 3 (dynamic) RENDER LOGIC
    """
    # TODO




    """
    # QUESTION 4 (dynamic) RENDER LOGIC
    """
    # TODO






# ============================================================================
# PART 4: Run the app (do NOT change this!)
# ============================================================================
app = App(app_ui, server)
