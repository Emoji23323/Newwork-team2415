"""YCY：声明 Haystack 文章索引的字段与文档模板。"""
from haystack import indexes

from blog.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    """YCY：把文章标题、正文、标签和作者映射到全文索引。"""
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', stored=True)
    body = indexes.CharField(model_attr='body', stored=True)

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status='p')
