"""YCY：定义前台页面、归档、链接、文件上传与缓存清理路由。"""
from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = "blog"
urlpatterns = [
    path(
        r'',
        views.IndexView.as_view(),
        name='index'),
    path(
        r'page/<int:page>/',
        views.IndexView.as_view(),
        name='index_page'),
    path(
        r'article/<int:year>/<int:month>/<int:day>/<int:article_id>.html',
        views.ArticleDetailView.as_view(),
        name='detailbyid'),
    path(
        r'category/<slug:category_name>.html',
        views.CategoryDetailView.as_view(),
        name='category_detail'),
    path(
        r'category/<slug:category_name>/<int:page>.html',
        views.CategoryDetailView.as_view(),
        name='category_detail_page'),
    path(
        r'author/<author_name>.html',
        views.AuthorDetailView.as_view(),
        name='author_detail'),
    path(
        r'author/<author_name>/<int:page>.html',
        views.AuthorDetailView.as_view(),
        name='author_detail_page'),
    path(
        r'tag/<slug:tag_name>.html',
        views.TagDetailView.as_view(),
        name='tag_detail'),
    path(
        r'tag/<slug:tag_name>/<int:page>.html',
        views.TagDetailView.as_view(),
        name='tag_detail_page'),
    path(
        'archives.html',
        cache_page(
            60 * 60)(
            views.ArchivesView.as_view()),
        name='archives'),
    path(
        'links.html',
        views.LinkListView.as_view(),
        name='links'),
    path(
        r'upload',
        # YCY：上传入口使用自定义签名鉴权，而不是登录态。
        views.fileupload,
        name='upload'),
    path(
        r'clean',
        # YCY：清缓存入口未做权限校验，生产环境应限制访问来源。
        views.clean_cache_view,
        name='clean'),
]
