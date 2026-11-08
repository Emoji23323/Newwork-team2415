"""YCY：管理命令：构建搜索词库。"""
from django.core.management.base import BaseCommand

from blog.models import Tag, Category


# YCY：TODO 参数化
class Command(BaseCommand):
    """YCY：封装搜索词库构建命令。"""
    help = 'build search words'

    def handle(self, *args, **options):
        datas = set([t.name for t in Tag.objects.all()] +
                    [t.name for t in Category.objects.all()])
        print('\n'.join(datas))
