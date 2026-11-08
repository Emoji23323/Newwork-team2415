"""PHJ：定义第三方登录补充邮箱表单。"""
from django.contrib.auth.forms import forms
from django.forms import widgets


class RequireEmailForm(forms.Form):
    """PHJ：要求用户补充邮箱以完成第三方账号绑定。"""
    email = forms.EmailField(label='电子邮箱', required=True)
    oauthid = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super(RequireEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = widgets.EmailInput(
            attrs={'placeholder': "email", "class": "form-control"})
