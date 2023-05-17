# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import DocumentForm,DocumentTextForm
from django.views.generic import FormView, TemplateView,DeleteView
import speech_recognition as sr
from pathlib import Path
from .models import *
from gtts import gTTS
import os
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django import forms


def transcribe_audio(audio_file):
    # Create a recognizer instance
    recognizer = sr.Recognizer()
    try:
        with audio_file.open('rb') as file_obj:
            with sr.AudioFile(file_obj) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                return text

    except sr.UnknownValueError:
        raise forms.ValidationError("Speech recognition could not understand audio")
    except sr.RequestError as e:
        raise forms.ValidationError(f"Could not request results from the Google Speech Recognition service: {e}")


def text_to_audio(data):
    media_root = settings.MEDIA_ROOT
    text = data.audio_text
    tts = gTTS(text=text, lang='en')
    # Set the save path for the audio file
    save_path = Path(media_root) / 'audio'
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    filename = f'{timestamp}.mp3'
    file_path = os.path.join(save_path, filename)
    tts.save(file_path)
    document = Document.objects.get(pk=data.pk)
    document.audio_file = 'audio/' + filename
    document.save()
    return filename


class HomeView(TemplateView):
    template_name = 'core/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = Document.objects.order_by('-uploaded_at')
        context['documents'] = documents
        return context


class ModelFormUploadView(FormView):
    template_name = 'core/simple_upload.html'
    form_class = DocumentForm
    success_url = '/home'

    def form_valid(self, form):
        audio_file = form.cleaned_data['audio_file']
        description = form.cleaned_data['description']

        try:
            data = form.save()
            text = transcribe_audio(audio_file)

            if text:
                document = get_object_or_404(Document, pk=data.pk)
                document.audio_text = text
                document.save()
                return redirect(self.success_url)

        except (ValueError, sr.UnknownValueError, sr.RequestError) as e:
            form.add_error('audio_file', str(e))

        return super().form_invalid(form)


class ModelFormTextView(FormView):
    template_name = 'core/simple_text.html'
    form_class = DocumentTextForm
    success_url = '/home'

    def form_valid(self, form):
        data = form.save()
        filename = text_to_audio(data)
        return redirect(self.success_url)


class DocumentDeleteView(DeleteView):
    model = Document
    success_url = reverse_lazy('home')
    template_name = 'core/document_confirm_delete.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
