from django.core.management.base import BaseCommand
from scheduler.tasks import start_scheduler
import time
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = '启动定时任务调度器'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('启动定时任务调度器...')
        )
        
        try:
            # 启动调度器
            start_scheduler()
            
            # 保持进程运行
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING('收到停止信号，正在关闭调度器...')
            )
        except Exception as e:
            logger.error(f"调度器运行失败: {e}")
            self.stdout.write(
                self.style.ERROR(f'调度器运行失败: {e}')
            ) 