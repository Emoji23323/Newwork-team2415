"""YCY：提供文章搜索表单，把用户输入转换为 Haystack 查询。"""
import logging

from django import forms
from haystack.forms import SearchForm

logger = logging.getLogger(__name__)


class BlogSearchForm(SearchForm):
    """YCY：文章搜索表单，对关键词做最小长度与空白校验。"""
    querydata = forms.CharField(required=True)

    def search(self):
        datas = super(BlogSearchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['querydata']:
            logger.info(self.cleaned_data['querydata'])
        return datas
