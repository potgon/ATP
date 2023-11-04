from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import threading
import time

import app.positions as pt
import utils.logger as lg
from app.fetcher import Fetcher
from evaluator.evaluator_factory import get_evaluator

logger = lg.setup_custom_logger("dash_app")
app = dash.Dash(__name__)
fetcher: Fetcher = Fetcher(ticker="GC=F")


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
            logger.info(f"Original data length: {len(fetcher.current_data)}")
            data = fetcher.current_data.copy()
        logger.info(f"Update graph received data: \n {data[-1:]}")
        lg.log_full_dataframe(data, logger)
        if data.empty:
            logger.info("No data available updating the graph")
            return go.Figure()
    except Exception as e:
        logger.error(f"Error updating the graph: {e}")
        return go.Figure()

    buy_data = data[get_evaluator()(data)]

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
    #    fig.add_trace(
    #        go.Scatter(
    #            x=data.index, y=data["Slope"], mode="lines", name="Slope", yaxis="y2"
    #        )
    #    )
    # logger.info(f"Slope value: {data['Slope']}")
    fig.add_trace(
        go.Scatter(
            x=buy_data.index,
            y=buy_data["Close"],
            mode="markers",
            name="Buy Signal",
            marker=dict(color="purple", size=20, symbol="circle-open"),
        )
    )

    #    fig.add_trace(
    #        go.Scatter(
    #            x=data.index,
    #            y=data["Stop Loss"],
    #            mode="lines+markers",
    #            name="Stop Loss",
    #            line=dict(color="red", width=2),
    #            marker=dict(size=6, color="red"),
    #        )
    #    )

    #    fig.add_trace(
    #        go.Scatter(
    #            x=data.index,
    #            y=data["Take Profit"],
    #            mode="lines+markers",
    #            name="Take Profit",
    #            line=dict(color="green", width=2),
    #            marker=dict(size=6, color="green"),
    #        )
    #    )

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
    return fig


def run():
    try:
        logger.info(
            "\n"
            + ("-" * 20)
            + "\n"
            + "Dash web app startup successful"
            + "\n"
            + ("-" * 20)
        )

        web_app_thread = threading.Thread(
            target=app.run,
        )
        web_app_thread.setDaemon(True)
        web_app_thread.start()

        logger.info("Running service loop...")
        service_loop()
    finally:
        logger.info("Dash web app shutdown successful")


def service_loop():
    current_pos = None
    evaluation_function = get_evaluator()
    while True:
        data = fetcher.fetch()
        if current_pos:
            if pt.close_position(data, current_pos.sl, current_pos.tp):
                current_pos.close()
                current_pos = None
        else:
            if evaluation_function(data.iloc[-1]):
                current_pos = pt.Position(data["Close"], data["ATR"], logger)
        time.sleep(60)
