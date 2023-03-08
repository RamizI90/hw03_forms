from django import forms

from .views import Post

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        help_texts = {
            'text':'Текст нового поста',
            'group':'Группа, к которой будет относиться пост',
        }
        labels = {
            'text':'Введите  текст поста',
            'group':'Выберите группу'
        }