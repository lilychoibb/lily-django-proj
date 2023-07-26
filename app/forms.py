from django import forms
from app.models import Post


class Postform(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
