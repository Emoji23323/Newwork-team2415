"""PHJ：注册 OAuth 授权入口、回调、邮箱补全与绑定结果路由。"""
from django.urls import path

from . import views

app_name = "oauth"
urlpatterns = [
    path(
        r'oauth/authorize',
        # PHJ：回调地址接收 code，并换取令牌与用户信息。
        views.authorize),
    path(
        r'oauth/requireemail/<int:oauthid>.html',
        views.RequireEmailView.as_view(),
        name='require_email'),
    path(
        r'oauth/emailconfirm/<int:id>/<sign>.html',
        views.emailconfirm,
        name='email_confirm'),
    path(
        r'oauth/bindsuccess/<int:oauthid>.html',
        views.bindsuccess,
        name='bindsuccess'),
    path(
        r'oauth/oauthlogin',
        # PHJ：登录入口根据 type 选择平台并跳转授权页。
        views.oauthlogin,
        name='oauthlogin')]
