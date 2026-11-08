"""YCY：管理命令：重建 Haystack 文章索引。"""
from django.core.management.base import BaseCommand

from blog.documents import ElapsedTimeDocument, ArticleDocumentManager, ElaspedTimeDocumentManager, \
    ELASTICSEARCH_ENABLED


# YCY：TODO 参数化
class Command(BaseCommand):
    """YCY：封装索引重建命令的入口。"""
    help = 'build search index'

    def handle(self, *args, **options):
        """YCY：调用 Haystack 的 update_index 完成全量重建。"""
        if ELASTICSEARCH_ENABLED:
            ElaspedTimeDocumentManager.build_index()
            manager = ElapsedTimeDocument()
            manager.init()
            manager = ArticleDocumentManager()
            manager.delete_index()
            manager.rebuild()
