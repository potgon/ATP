from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import threading

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
            logger.info(f"Copied data length: {len(data)}")
        logger.info(f"Logged data: \n {data[-1:]}")
        #temp_data only serves debugging purposes. Will be removed at production
        temp_data = data.drop(columns=["Adj Close"])
        lg.log_full_dataframe(temp_data, logger)
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
            marker=dict(color="red", size=15, symbol="circle-open"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Stop Loss"],
            mode="lines",
            name="Stop Loss",
            line=dict(color="orange"),
        )
    )

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

        logger.info("Running periodic tasks...")
        fetcher.periodic_fetch()
    finally:
        logger.info("Dash web app shutdown successful")
