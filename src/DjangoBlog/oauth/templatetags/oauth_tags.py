"""PHJ：向模板提供已启用的第三方登录应用列表。"""
from django import template
from django.urls import reverse

from oauth.oauthmanager import get_oauth_apps

register = template.Library()


@register.inclusion_tag('oauth/oauth_applications.html')
def load_oauth_applications(request):
    """PHJ：读取启用的平台配置并返回模板上下文。"""
    applications = get_oauth_apps()
    if applications:
        baseurl = reverse('oauth:oauthlogin')
        path = request.get_full_path()

        apps = list(map(lambda x: (x.ICON_NAME, '{baseurl}?type={type}&next_url={next}'.format(
            baseurl=baseurl, type=x.ICON_NAME, next=path)), applications))
    else:
        apps = []
    return {
        'apps': apps
    }
