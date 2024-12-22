from django import forms

from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widget = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-6 py-4 border rounded-xl '
            })
        }