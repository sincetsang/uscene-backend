import asyncio
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
import logging
from .event import EventTask

logger = logging.getLogger(__name__)

# 全局变量来管理事件监听器
event_listener_thread = None
event_listener_instance = None

def start_scheduler():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    # 添加事件扫描任务
    scheduler.add_job(
        EventTask.scan_low_events,
        trigger=IntervalTrigger(seconds=10),  # 每10秒执行一次
        id="scan_events",
        max_instances=1,
        replace_existing=True,
        misfire_grace_time=60
    )

    try:
        logger.info("启动调度器...")
        scheduler.start()
    except Exception as e:
        logger.error(f"调度器启动失败: {e}")
