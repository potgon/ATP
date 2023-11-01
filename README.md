# Algorithmic Trading Platform (ATP) 
[Development Log](https://potgon.notion.site/Development-Log-0a4f8373e7e8472f8203e4b1972906ca?pvs=4)
## Overview

ATP is a versatile platform designed to host and run multiple trading algorithms concurrently. With a focus on different market assets, ATP provides a comprehensive environment for backtesting and deploying strategies in real-time, supported by modern technologies such as AWS, Python, and Dash.

## Features

- **Diverse Asset Support**: Host algorithms tailored for different market assets including stocks, forex, commodities, and cryptocurrencies.
- **Concurrent Execution**: Leverage threading and multiprocessing to run multiple algorithms simultaneously.
- **Live Data**: Fetch and analyze real-time market data.
- **Interactive Dashboard**: Utilize a Dash-based web application for monitoring live trading signals, price movements, and more.
- **Cloud Integration**: Hosted on AWS to ensure scalability, reliability, and ease of deployment.

## Installation

To set up the ATP platform, follow these steps:

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/potgon/AST
2. **Navigate to root folder**:
   ```sh
   cd AST
3. **Install and run with poetry**:
   ```sh
   poetry install
   poetry run python main.py

## Usage
- **Adding Algorithms**: To add new trading algorithms, follow the guidelines in the algorithms/ directory.
- **Monitoring**: Access the Dash-based web application to monitor the performance and signals generated by the algorithms.
- **Logs**: Check the logs/ directory for detailed logs on price data, algorithm signals, and system operations.

## License
ATP is licensed under the MIT License. See the LICENSE file for more details.
