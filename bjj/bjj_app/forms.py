from django import forms
from .models import Comment, NewsReaction


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = Comment
        fields = ('content',)


class NewsReactionForm(forms.ModelForm):
    class Meta:
        model = NewsReaction
        fields = ['reaction_type']
        widgets = {
            'reaction_type': forms.Select(choices=NewsReaction.REACTION_CHOICES)
        }
