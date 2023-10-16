from celery import shared_task
from time import sleep


@shared_task(ignore_result=False)
def health_check():
    sleep(5)
    return "everything is fine with celery"


@shared_task(ignore_result=False)
def health_cron_check():
    sleep(5)
    return "everything is fine with celery cron"
