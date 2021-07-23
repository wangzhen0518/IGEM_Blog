from django import forms
from .models import blogpost


class blogform(forms.ModelForm):
    class Meta:
        model = blogpost
        fields = ['title', 'text']
        labels = {'title': 'title', 'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 100, 'rows': 25})}
