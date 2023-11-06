from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import threading
import time

import app.positions as pt
import utils.logger as lg
from utils.config import SNR_CHECK_INTERVAL
from app.fetcher import Fetcher
from evaluator.evaluator_factory import get_evaluator

logger = lg.setup_custom_logger("dash_app")
app = dash.Dash(__name__)
fetcher: Fetcher = Fetcher(ticker="CL=F")


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
            clusters = fetcher.current_snr.copy()
        logger.info(f"Updating graph with received data: \n {data[-1:]}")
        logger.info(f"Updating the graph with received cluster: \n {clusters[-1:]}")
        lg.log_full_dataframe(data, logger)
        if data.empty:
            logger.info("No data available updating the graph")
            return go.Figure()
    except Exception as e:
        logger.error(f"Error updating the graph: {e}")
        return go.Figure()

    # buy_data = data[get_evaluator()(data)]

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

    # for _, row in support_resistance.iterrows():
    #     fig.add_trace(go.Scatter(x=data.index, y=[row['min'], row['min']], mode='lines', line=dict(color='green'), name='Support'))
    #     fig.add_trace(go.Scatter(x=data.index, y=[row['max'], row['max']], mode='lines', line=dict(color='red'), name='Resistance'))

    # fig.add_trace(
    #     go.Scatter(
    #         x=buy_data.index,
    #         y=buy_data["Close"],
    #         mode="markers",
    #         name="Buy Signal",
    #         marker=dict(color="purple", size=20, symbol="circle-open"),
    #     )
    # )

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
    logger.info("Service loop start...")
    current_pos = None
    logger.info(f"Position open?: {type(current_pos)}")
    last_snr_check = time.time()
    next_snr_check = last_snr_check + SNR_CHECK_INTERVAL
    evaluation_function = get_evaluator()
    while True:
        data = fetcher.fetch()
        current_time = time.time()
        if current_pos:
            logger.info(
                f"Current position attributes: {current_pos.sl}, {current_pos.tp}"
            )
            if pt.close_position(data, current_pos.sl, current_pos.tp):
                current_pos.close()
                current_pos = None
                logger.info(f"Position closed?: {type(current_pos)}")
        else:
            if evaluation_function(data.iloc[-1]):
                current_pos = pt.Position(data["Close"], data["ATR"], logger)
                logger.info(f"Position opened?: {type(current_pos)}")

        if current_time >= next_snr_check:
            cluster = fetcher.update_snr()
            last_snr_check = time.time()
            next_snr_check = last_snr_check + SNR_CHECK_INTERVAL
            logger.info("Cluster checked for support and resistance zones")

        logger.info("Service loop sleep...")
        time.sleep(60)
