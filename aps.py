import os
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import sys
from dcard18 import use_process,dcard_sex

def hello():
    print('hello world')

if __name__ == '__main__':
    crawl = dcard_sex(3,50)
    
    scheduler = BlockingScheduler()
    scheduler.add_job(use_process,'cron', minute='*/1', hour='*',args=(crawl,10))
    print('準備執行中')

    try:
        scheduler.start()

    except(KeyboardInterrupt, SystemExit):
        scheduler.shutdown()        
