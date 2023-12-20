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
    
    while True:
        evaluator.fetch_error = False
        
        with fetcher.data_lock:
            try:
                fetcher.fetch()
                data = fetcher.current_data.copy()
            except Exception:
                evaluator.fetch_error = True
                
        send_custom_metric("Dataframe Fetch Alert", custom_handler=evaluator.custom_metric_handler)
        
        if evaluator.fetch_error == True:
            make_log("EVAL_LOOP", 30, "workflow.log", "Failure on fetching new data, skipping interval...")
        else:    
            log_full_dataframe("PRICE", 10, "price.log")
        
            if current_pos:
                if current_pos.should_close(current_pos):
                    current_pos.close()
                    current_pos = None
                    
            else: 
                if evaluator.evalaute():
                    current_pos = open_position(ticker)
                
        time.sleep(60 * 60) # Make generic, should work for every algorithm   