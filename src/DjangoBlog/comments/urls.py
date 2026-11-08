"""PZQ：注册评论提交与表情反应两条路由。"""
from django.urls import path

from . import views

app_name = "comments"
urlpatterns = [
    path(
        'article/<int:article_id>/postcomment',
        # PZQ：评论提交走登录 + CSRF 双重保护。
        views.CommentPostView.as_view(),
        name='postcomment'),
    path(
        'comment/<int:comment_id>/react',
        # PZQ：反应接口同时提供公开 GET 与需登录的 POST。
        views.CommentReactionView.as_view(),
        name='comment_react'),
]
