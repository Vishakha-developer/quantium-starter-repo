import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("formatted_sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Create Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div(
    style={
        "backgroundColor": "#f4f6f9",
        "padding": "30px",
        "fontFamily": "Arial"
    },
    children=[

        html.H1(
            "Soul Foods Pink Morsel Sales Dashboard",
            id="header",
            style={
                "textAlign": "center",
                "color": "#2c3e50",
                "marginBottom": "30px"
            }
        ),

        html.Div(
            children=[

                html.Label(
                    "Select Region:",
                    style={
                        "fontSize": "20px",
                        "fontWeight": "bold"
                    }
                ),

                dcc.RadioItems(
                    id="region-picker",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    style={
                        "marginTop": "10px",
                        "marginBottom": "20px"
                    }
                ),

                dcc.Graph(id="sales-chart")

            ]
        )

    ]
)


# Callback
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-picker", "value")
)
def update_chart(region):

    if region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["Region"].str.lower() == region]

    daily_sales = (
        filtered_df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title=f"Pink Morsel Sales - {region.title()}",
        markers=True
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="#f4f6f9",
        font=dict(size=15),
        xaxis_title="Date",
        yaxis_title="Sales",
        title_x=0.5
    )

    return fig


# Run app
if __name__ == "__main__":
    app.run(debug=True)