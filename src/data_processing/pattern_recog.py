from app.dash_app import retrieve_fetcher

fetcher = retrieve_fetcher()


def find_engulfing():
    data = fetcher.current_data.copy()
    
