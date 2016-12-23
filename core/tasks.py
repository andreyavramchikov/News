from django.core.management import call_command


from celery.task.base import periodic_task
from celery.schedules import crontab


@periodic_task(run_every=(crontab(minute='*/10')), name="parse", ignore_result=True)
def parse_all():
    """
    To run locally:
       1. celery -A news worker -l info
       2. celery -A news beat -l info
    """
    call_command('parse_all')
    print 'FINISHED'


