from shiny import App, ui, reactive
from shinywidgets import (
    render_plotly,
    output_widget
)




# ============================================================================
# PART 1: GLOBAL STATE (not dep. on user input)
#   Import helper functions, read data, compute axis ranges (of individual attributes)
# ============================================================================

import pandas as pd

# 1.1. Global state: Import helper functions
from dashboard_helpers import (
    education_vars,
    health_vars,
    filter_data,
    compute_axis_ranges,
    create_scatterplot
)

# 1.2. Global state: read data
df = pd.read_csv(
    "data/panel_1980_2010.csv"
)

# 1.3. Global state:  Compute ranges for each variable (keep plotting consistent)
axis_ranges = compute_axis_ranges(
    df=df,
    x_vars=education_vars,
    y_vars=health_vars
)




# ============================================================================
# PART 2: Dashboard Structure (tabbed between About, Q1, Q2, Q3, Q4)
# ============================================================================
app_ui = ui.page_navbar(

    # ============================================================
    # ABOUT TAB
    # ============================================================

    ui.nav_panel(
        "About",

        ui.h2(
            "Education and Health in East & Southeast Asia"
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

        "Q2",

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
                    output_widget("scatterplot"),
                    style="max-width:1200px; margin:auto;"
                )
            )
        )
    ),

    # ============================================================
    # Q3's Tab
    # ============================================================

    ui.nav_panel(
        "Q3",

        ui.h3("Question 3"),

        ui.p("Notebook integration pending.")
    ),

    # ============================================================
    # Q4's Tab
    # ============================================================

    ui.nav_panel(
        "Q4",

        ui.h3("Question 4"),

        ui.p("Notebook integration pending.")
    ),

    title="Education & Health Dashboard (E/SE Asia; 1980-2019)"
)





def server(input, output, session):

    # 1. FILTER DATA: when UI-input-values are changed, re-filter the displayed-data accordingly. 
    @reactive.calc  
    def filtered():
        # invoke dashboard_helpers.filter_data(...) 
        #   a helper function in dashboard_helpers.py

        return filter_data(
            df,
            year=input.year(),
            include_east="East Asia" in input.regions(),
            include_southeast="Southeast Asia" in input.regions(),
        )

    # 2. DISPLAY SCATTER: Render the scatterplot (perhaps again, when the UI values changed)
    @render_plotly
    def scatterplot():

        fig = create_scatterplot(
            filtered(),
            input.x_var(),
            input.y_var(),
            input.color_var(),
            input.year(),
            axis_ranges,
        )

        return fig





app = App(app_ui, server)
