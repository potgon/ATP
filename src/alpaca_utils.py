from aws import get_secret



# def acc_info():

#     (api_key,) = get_secret("PAPER").keys()
#     (api_value,) = get_secret("PAPER").values()
#     trading_client = TradingClient(api_key, api_value)

#     account = trading_client.get_account()

#     print('${} is available as buying power.'.format(account.buying_power))