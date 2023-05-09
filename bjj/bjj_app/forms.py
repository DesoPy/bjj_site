from django import forms
from .models import Comment, NewsReaction


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = Comment
        fields = ('content',)


class ReactionForm(forms.ModelForm):
    class Meta:
        model = NewsReaction
        fields = ['reaction_type']
        widgets = {
            'reaction_type': forms.Select(attrs={'class': 'select'}),
        }
        labels = {
            'reaction_type': 'Choose a reaction:',
        }

    def save(self, commit=True):
        reaction = super().save(commit=False)
        reaction.reaction_type = self.cleaned_data['reaction_type']
        if commit:
            reaction.save()
        return reaction

    reaction_type = forms.ChoiceField(choices=NewsReaction.REACTION_CHOICES, widget=forms.Select(attrs={'class': 'select'}), required=True)


