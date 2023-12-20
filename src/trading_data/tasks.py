from celery import shared_task

from .models import Position
from .services.fetcher import Fetcher
from evaluation_core.factories import get_evaluator
from utils.logger import make_log


@shared_task
def manage_algorithm(algo_name, ticker):
    fetcher = Fetcher(ticker)
    evaluator = get_evaluator(fetcher, algo_name)
    current_pos = None
    
    while True:
        evaluator.fetch_error = False
        
        with fetcher.data_lock:
            try:
                fetcher.fetch()
            except Exception:
                evaluator.fetch_error = True
                
        if evaluator.fetch_error == True:
            make_log("EVAL_LOOP", 30, "workflow.log", "Failure on fetching new data, skipping interval...")
        else:    
            should_open = evaluator.evalaute()
        
            if current_pos:
                if current_pos.should_close(current_pos):
                    current_pos.close()
                    current_pos = None
                    
            else: 
                if should_open:
                    current_pos = open_position(ticker)
                
        time.sleep(60 * 60) # Make generic, should work for every algorithm   