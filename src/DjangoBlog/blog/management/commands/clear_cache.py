"""YCY：管理命令：清空站点缓存。"""
from django.core.management.base import BaseCommand

from djangoblog.utils import cache


class Command(BaseCommand):
    """YCY：提供缓存清理的运维入口。"""
    help = 'clear the whole cache'

    def handle(self, *args, **options):
        cache.clear()
        self.stdout.write(self.style.SUCCESS('Cleared cache\n'))
