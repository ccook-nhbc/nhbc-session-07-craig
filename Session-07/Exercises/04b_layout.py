from shiny import App, ui, render, run_app
from shinywidgets import output_widget, render_widget
import plotly.express as px
import numpy as np

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h3("Controls"),
        ui.input_slider("n", "Sample Size", 10, 1000, 500),
        ui.input_select("color", "Color", choices=["blue", "red", "green"]),
        # Task 1: Add Checkbox
        ui.input_checkbox("show_grid", "Show Grid", True),
    ),
    # Task 3: Use layout_columns
    ui.layout_columns(
        ui.card(
            ui.card_header("Distribution Plot"),
            output_widget("dist_plot"),
        ),
        ui.card(
            ui.card_header("Summary Statistics"),
            ui.output_text_verbatim("stats"),
        ),
        col_widths=(8, 4) # 8/12 for plot, 4/12 for stats
    )
)

def server(input, output, session):
    
    @render_widget
    def dist_plot():
        rng = np.random.default_rng(123)
        data = rng.standard_normal(input.n())
        fig = px.histogram(x=data, nbins=30, title=f"Histogram of {input.n()} points")
        fig.update_traces(marker_color=input.color())
        
        # Task 2: Update grid
        fig.update_layout(
            xaxis=dict(showgrid=input.show_grid()),
            yaxis=dict(showgrid=input.show_grid())
        )
        return fig

    @render.text
    def stats():
        return f"Selected N: {input.n()}"

app = App(app_ui, server)

if __name__ == "__main__":
    run_app(app, launch_browser=True)