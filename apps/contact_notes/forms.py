from django import forms
from .models import ContactNote
from django.core.exceptions import ValidationError


class ContactNoteForm(forms.ModelForm):
    class Meta:
        model = ContactNote
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, })
        }

    def clean_message(self):
        message = self.cleaned_data['message']
        if message and len(message.strip()) < 10:
            raise ValidationError('Message must contain at least 10 characters.')

        return message
