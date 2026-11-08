"""ZXL：提供用户名或邮箱二选一的认证后端。"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameModelBackend(ModelBackend):
    """ZXL：
    允许使用用户名或邮箱登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """ZXL：按输入形态选择查询字段，并校验密码哈希。"""
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
