from django import forms
from .models import Post, PostImage


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = ('title', 'contents')
        fields = ('title', 'contents')  # 입력 받고 싶은 것
        exclude = ('writer',)  # 입력 받고 싶지 않은 것