from dash.dependencies import Input, Output
from app.fetcher import Fetcher
import utils.logger as lg
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import threading

from evaluator.evaluator_factory import get_evaluator

logger = lg.setup_logger("dash_app")
app = dash.Dash(__name__)

fetcher: Fetcher = Fetcher()

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
            logger.info(
                f"Original data length and ID: {len(fetcher.current_data)}, {id(fetcher.current_data)}"
            )
            data = fetcher.current_data.copy()
            logger.info(f"Copied data length: {len(data)}")
        logger.info(f"Updating graph, current data: {data}")
        if data.empty:
            logger.info("No data available updating the graph")
            return go.Figure()
    except Exception as e:
        logger.error(f"Error updating the graph: {e}")
        return go.Figure()

    buy_signals = get_evaluator()(data)
    buy_data = data[buy_signals]

    fig = go.Figure()

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
    fig.add_trace(
        go.Scatter(x=data.index, y=data["Upper"], mode="lines", name="Upper Bollinger")
    )
    fig.add_trace(
        go.Scatter(
            x=data.index, y=data["Middle"], mode="lines", name="Middle Bollinger"
        )
    )
    fig.add_trace(
        go.Scatter(x=data.index, y=data["Lower"], mode="lines", name="Lower Bollinger")
    )
    fig.add_trace(go.Scatter(x=data.index, y=data["EMA9"], mode="lines", name="EMA9"))
    fig.add_trace(go.Scatter(x=data.index, y=data["EMA21"], mode="lines", name="EMA21"))
    fig.add_trace(
        go.Scatter(
            x=buy_data.index,
            y=buy_data["Close"],
            mode="markers",
            name="Buy Signal",
            marker=dict(color="red", size=15, symbol="circle-open"),
        )
    )

    layout = go.Layout(
        title="AAPL Live Candlestick Chart with Buy Signals",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        yaxis=dict(type="linear", range=[min(data["Low"]), max(data["High"])]),
    )

    fig.update_layout(layout)
    return fig


def run():
    try:
        logger.info("Dash web app startup successful")

        web_app_thread = threading.Thread(
            target=app.run,
        )
        web_app_thread.setDaemon(True)
        web_app_thread.start()

        logger.info("Running periodic tasks...")
        fetcher.periodic_fetch()
    finally:
        logger.info("Dash web app shutdown successful")
