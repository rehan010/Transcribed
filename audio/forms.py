from .models import Document
from django import forms
from django.core.exceptions import ValidationError

class DocumentForm(forms.ModelForm):
    audio_file = forms.FileField(label='Select an audio file', widget=forms.FileInput(attrs={'class': 'custom-file-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['audio_file'].widget.attrs.update({'class': 'custom-file-input'})


    def clean_audio_file(self):
        audio_file = self.cleaned_data.get('audio_file')
        if audio_file:
            content_type = audio_file.content_type
            allowed_content_types = [
                # 'audio/mpeg',
                'audio/wav',
                # Add more accepted audio file types as needed
            ]
            if content_type not in allowed_content_types:
                raise ValidationError('Please upload an audio file ( WAV).')
        return audio_file

    class Meta:
        model = Document
        fields = ('description', 'audio_file',)

class DocumentTextForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('description', 'audio_text',)
