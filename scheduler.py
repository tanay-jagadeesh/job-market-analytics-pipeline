import schedule
import time
from datetime import datetime
from analytics import run_all_queries


def job():
    run_all_queries()

#ensures that it runs at 6 am everyday
schedule.every().day.at("6:00").do(job)
