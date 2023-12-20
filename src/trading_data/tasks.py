from celery import shared_task

from .models import Position
from .services.fetcher import Fetcher
from aws_integration.services import send_custom_metric
from evaluation_core.factories import get_evaluator
from utils.logger import make_log, log_full_dataframe


@shared_task
def manage_algorithm(algo_name, ticker):
    fetcher = Fetcher(ticker) # Possible exception if ticker does not exist
    evaluator = get_evaluator(fetcher, algo_name)
    current_pos = None
    make_log("ALGO", 20, "workflow.log", f"Instantiation start: \n Evaluator: {algo_name} \n Fetcher pointing to: {ticker}")
    
    while True:
        make_log("ALGO", 20, "workflow.log", f"{algo_name} algorithm period start") # Make a different log file for each algorithm?
        evaluator.fetch_error = False
        
        with fetcher.data_lock:
            try:
                make_log("ALGO", 20, "workflow.log", f"{algo_name} is attempting data fetch for {ticker}")
                fetcher.fetch()
                data = fetcher.current_data.copy()
                make_log("ALGO", 20, "workflow.log", "Successful data fetch!")
            except Exception:
                evaluator.fetch_error = True
                
        send_custom_metric("Dataframe Fetch Alert", custom_handler=evaluator.custom_metric_handler)
        
        if evaluator.fetch_error == True:
            make_log("EVAL_LOOP", 30, "workflow.log", "Failure on fetching new data, skipping interval...")
        else:    
            log_full_dataframe("PRICE", 10, "price.log")
            make_log("ALGO", 20, "workflow.log", f"Position open? {'No' if current_pos == None else 'Yes'}")
            
            if current_pos:
                if current_pos.should_close(data["Low"], data["High"]):
                    current_pos.close_db(data["Close"])
                    make_log("EVAL_LOOP", 30, "workflow.log", "Closing position in database")
                    current_pos.close_broker()
                    make_log("EVAL_LOOP", 30, "workflow.log", "Closing position in broker")
                    current_pos = None
            else: 
                if evaluator.evalaute():
                    current_pos = Position(data["Close"], data["ATR"], evaluator.alpha)
                    make_log("EVAL_LOOP", 30, "workflow.log", f"Instantiating position...: {'Success!' if current_pos is not None else 'Failure'}")
                    current_pos.open_broker()
                    make_log("EVAL_LOOP", 30, "workflow.log", "Opening Position in broker...")
                
        time.sleep(60 * 60) # Make generic, should work for every algorithm   