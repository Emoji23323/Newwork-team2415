"""PZQ：定义评论正文与父评论 ID 表单。"""
from django import forms
from django.forms import ModelForm

from .models import Comment


class CommentForm(ModelForm):
    """PZQ：评论表单，正文来自 Comment 模型，父评论 ID 为隐藏字段。"""
    parent_comment_id = forms.IntegerField(
        widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['body']
