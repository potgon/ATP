from dash.dependencies import Input, Output
import dash
from dash import dcc, html
import plotly.graph_objs as go
import threading
import time
from queue import Queue

import app.positions as pt
from aws.cdwatch import send_custom_metric
from data_processing.fetcher import Fetcher
from evaluator.evaluator_factory import get_evaluator
from evaluator.evaluators.tyr import get_snr_prices
from utils.algo_tracker import insert_transaction, alter_transaction
from utils.logger import make_log, log_full_dataframe

app = dash.Dash(__name__)
fetcher: Fetcher = Fetcher(ticker="AUDUSD=X")
buy_signals_queue = Queue()


app.layout = html.Div(
    [
        dcc.Graph(id="live-graph"),
        dcc.Interval(id="interval-component", interval=3_600_000, n_intervals=0),
    ]
)


@app.callback(
    Output("live-graph", "figure"), [Input("interval-component", "n_intervals")]
)
def update_graph(_):
    try:
        with fetcher.data_lock:
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

    fig = go.Figure()

    make_log("GRAPH", 20, "graph.log", "Adding candlesticks...")
    plot_cdl(data, fig)
    plot_reversal_zones(fig)
    # plot_patterns(data, fig)

    while not buy_signals_queue.empty():
        buy_signals_queue.get()
        plot_buy_signal(fig, data)

    layout = go.Layout(
        title=f"{fetcher.ticker} Live Candlestick Chart",
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
            target=lambda: app.run_server(debug=False, host="0.0.0.0", port=8050),
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
    evaluator = get_evaluator(fetcher)
    while True:
        make_log("DASH", 20, "workflow.log", "Period start...")
        evaluator.fetch_error = False
        fetcher.fetch()
        make_log("DASH", 20, "workflow.log", f"Position open?: {type(current_pos)}")
        with fetcher.data_lock:
            try:
                data = fetcher.current_data.copy()
            except Exception:
                evaluator.fetch_error = True
                data = None
        send_custom_metric("Dataframe Fetch Alert", custom_handler=evaluator.custom_metric_handler)
        if data is None:
            make_log("DASH", 20, "workflow.log", "Data is empty, skipping interval...")
        else:
            if current_pos:
                make_log(
                    "DASH",
                    20,
                    "workflow.log",
                    f"Current position attributes: {current_pos.sl}, {current_pos.tp}",
                )
                if pt.close_position(data, current_pos.sl, current_pos.tp):
                    alter_transaction(data.iloc[-1])
                    current_pos.close()
                    current_pos = None
                    make_log(
                        "DASH",
                        20,
                        "workflow.log",
                        f"Closing position...: {type(current_pos)}",
                    )
            else:
                if evaluator.evaluate():
                    buy_signals_queue.put(1)
                    insert_transaction(data.iloc[-1], evaluator.alpha)
                    make_log(
                        "DASH",
                        20,
                        "workflow.log",
                        f"EVALUATION POSITIVE, current queue: {buy_signals_queue.qsize()}",
                    )
                    current_pos = pt.Position(data["Close"], data["ATR"])
                    make_log(
                        "DASH",
                        20,
                        "workflow.log",
                        f"Opening position...: {type(current_pos)}",
                    )

        make_log("DASH", 20, "workflow.log", "Period sleep..." + "\n" + ("-" * 20))
        time.sleep(60 * 60)


def plot_reversal_zones(fig):
    reversal_dict = get_snr_prices(fetcher.ticker)
    for max, min in reversal_dict.items():
        fig.add_hrect(
            y0=min,
            y1=max,
            line_width=0,
            fillcolor="green",
            opacity=0.35,
        )


def plot_cdl(data, fig):
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


def plot_buy_signal(fig, data):
    fig.add_trace(
        go.Scatter(
            x=[data.index[-1]],
            y=[data["Close"].iloc[-1]],
            mode="markers",
            name="Buy Signal",
            marker=dict(color="purple", size=20, symbol="circle-open"),
        )
    )


def retrieve_fetcher() -> Fetcher:
    return fetcher
