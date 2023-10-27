from dash.dependencies import Input, Output
from utils import periodic_fetch, current_data, buy_signal
import logger as lg
import asyncio
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import talib as ta
import yfinance as yf

logger = lg.setup_logger("dash_app")
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*60*1000, 
        n_intervals=0
    )
])

def run_periodic_tasks():
    logger.info("Running periodic tasks...")
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_fetch())
    
@app.callback(
    Output('live-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    try:
        data = current_data
        logger.debug(f"Updating graph, current data: {data}")
        if current_data.empty:
            logger.info("No data available updating the graph")
            return go.Figure()
    except Exception as e:
        logger.error(f"Error updating the graph: {e}")
        return go.Figure()
    buy_signals = buy_signal(data)
    buy_data = data[buy_signals]

    fig = go.Figure()

    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name="Price"))
    fig.add_trace(go.Scatter(x=data.index, y=data['Upper'], mode='lines', name='Upper Bollinger'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Middle'], mode='lines', name='Middle Bollinger'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Lower'], mode='lines', name='Lower Bollinger'))
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA9'], mode='lines', name='EMA9'))
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA21'], mode='lines', name='EMA21'))
    fig.add_trace(go.Scatter(x=buy_data.index, y=buy_data['Close'], mode='markers', name='Buy Signal', marker=dict(color='red', size=15, symbol='circle-open')))

    layout = go.Layout(title="AAPL Live Candlestick Chart with Buy Signals",
                   xaxis_title="Date",
                   yaxis_title="Price",
                   xaxis_rangeslider_visible=False, 
                   yaxis=dict(type='linear', range=[min(data['Low']), max(data['High'])])
                   )

    fig.update_layout(layout)
    return fig

def run():
    run_periodic_tasks()
    logger.info("Dash web app startup completed")
    app.run_server(debug=True)
    logger.info("Dash web app finalized successfully")