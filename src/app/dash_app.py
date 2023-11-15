from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import threading
import time

import app.positions as pt
from utils.logger import make_log, log_full_dataframe
from app.fetcher import Fetcher
from evaluator.evaluator_factory import get_evaluator

app = dash.Dash(__name__)
fetcher: Fetcher = Fetcher(ticker="EURUSD=X")

app.layout = html.Div(
    [
        dcc.Graph(id="live-graph"),
        dcc.Interval(id="interval-component", interval=60_000, n_intervals=0),
    ]
)


@app.callback(
    Output("live-graph", "figure"), [Input("interval-component", "n_intervals")]
)
def update_graph(_):
    try:
        with fetcher.data_lock:
            make_log(
                "GRAPH",
                20,
                "graph.log",
                f"Original data length: {len(fetcher.current_data)}",
            )
            data = fetcher.current_data.copy()
        make_log(
            "GRAPH",
            20,
            "graph.log",
            f"Updating graph with received data: \n {data[-1:]}",
        )
        log_full_dataframe("PRICE", 10, "price.log", data)
        if data.empty:
            make_log("GRAPH", 20, "graph.log", "No data available updating the graph")
            return go.Figure()
    except Exception as e:
        make_log("GRAPH", 20, "graph.log", f"Error updating the graph: {e}")
        return go.Figure()

    # buy_data = data[get_evaluator()(data)]

    fig = go.Figure()

    make_log("GRAPH", 20, "graph.log", "Adding candlesticks...")

    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Price",
        )
    )

    # fig.add_trace(
    #     go.Scatter(
    #         x=buy_data.index,
    #         y=buy_data["Close"],
    #         mode="markers",
    #         name="Buy Signal",
    #         marker=dict(color="purple", size=20, symbol="circle-open"),
    #     )
    # )

    plot_support_resistance(data, min_bounces=2, fig=fig)

    layout = go.Layout(
        title=f"{fetcher.ticker} Live Candlestick Chart with Buy Signals",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        yaxis=dict(type="linear", range=[min(data["Low"]), max(data["High"])]),
        yaxis2=dict(
            overlaying="y",
            side="right",
            range=[-1, 1],
        ),
    )

    fig.update_layout(layout)
    make_log("GRAPH", 20, "graph.log", "Updating graph layout...")
    return fig


def run():
    try:
        make_log(
            "DASH",
            20,
            "workflow.log",
            "\n"
            + ("-" * 20)
            + "\n"
            + "Dash web app startup successful"
            + "\n"
            + ("-" * 20),
        )

        web_app_thread = threading.Thread(
            target=app.run,
        )
        web_app_thread.setDaemon(True)
        web_app_thread.start()

        make_log("DASH", 20, "workflow.log", "Running service loop...")
        service_loop()
    finally:
        make_log("DASH", 20, "workflow.log", "Dash web app shutdown successful")


def service_loop():
    make_log("DASH", 20, "workflow.log", "Service loop start...")
    current_pos = None
    make_log("DASH", 20, "workflow.log", f"Position open?: {type(current_pos)}")
    evaluation_function = get_evaluator()
    while True:
        data = fetcher.fetch()
        if current_pos:
            make_log(
                "DASH",
                20,
                "workflow.log",
                f"Current position attributes: {current_pos.sl}, {current_pos.tp}",
            )
            if pt.close_position(data, current_pos.sl, current_pos.tp):
                current_pos.close()
                current_pos = None
                make_log(
                    "DASH", 20, "workflow.log", f"Position closed?: {type(current_pos)}"
                )
        else:
            if evaluation_function(data.iloc[-1]):
                current_pos = pt.Position(data["Close"], data["ATR"])
                make_log(
                    "DASH", 20, "workflow.log", f"Position opened?: {type(current_pos)}"
                )

        make_log("DASH", 20, "workflow.log", "Service loop sleep...")
        time.sleep(60)


import plotly.graph_objects as go


def plot_support_resistance(dfkeys, min_bounces, fig):
    high_counts = dfkeys[dfkeys["Pivot"] == 2]["High"].value_counts()
    low_counts = dfkeys[dfkeys["Pivot"] == 1]["Low"].value_counts()

    significant_highs = high_counts[high_counts >= min_bounces]
    significant_lows = low_counts[low_counts >= min_bounces]

    for level in significant_highs.index:
        fig.add_hline(
            y=level,
            line_dash="solid",
            line_color="red",
            annotation_text=f"Resistance ({high_counts[level]})",
            annotation_position="bottom right",
        )

    for level in significant_lows.index:
        fig.add_hline(
            y=level,
            line_dash="solid",
            line_color="green",
            annotation_text=f"Support ({low_counts[level]})",
            annotation_position="top right",
        )
