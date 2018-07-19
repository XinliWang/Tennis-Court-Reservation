import cancellation
import tennis
from apscheduler.schedulers.background import BackgroundScheduler
import time

scheduler = BackgroundScheduler()
# method is trigger everyday at 12:01 am
scheduler.add_job(tennis.runReserve,
				  'cron',
				  day_of_week='mon-sun',
				  hour=0, minute=0,
				  end_date='2018-10-30'
				  )

scheduler.add_job(cancellation.cancel,
				  'cron',
				  day_of_week='mon-sun',
				  hour=22, minute=0,
				  end_date='2018-10-30'
				  )
scheduler.start()

while True:
    time.sleep(5)
