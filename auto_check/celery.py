from celery import Celery
from celery.schedules import crontab

import os

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

CELERY_TIMEZONE = 'Asia/Shanghai'

DDQ = Celery("DDQ", broker="redis://127.0.0.1:6379", backend="redis://127.0.0.1:6379",
             include=["auto_check.TaskOne",])

# 我要要对beat任务生产做一个配置,这个配置的意思就是每10秒执行一次Celery_task.task_one任务参数是(10,10)
DDQ.conf.beat_schedule = {
    "each10s_task": {
        "task": "auto_check.TaskOne.check",
        "schedule": 10*60,  # 每10秒钟执行一次
        "args": (1,)
    },
}