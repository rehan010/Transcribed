# Create your views here.
from django.shortcuts import render
from django.conf import settings
from .forms import DocumentForm,DocumentTextForm
from django.views.generic import View, TemplateView,DeleteView
import speech_recognition as sr
from pathlib import Path
from .models import *
from gtts import gTTS
import os
from django.utils import timezone
from django.urls import reverse_lazy


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
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from the Google Speech Recognition service: {e}")


class HomeView(TemplateView):
    template_name = 'core/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = Document.objects.all()
        context['documents'] = documents
        return context


class ModelFormUploadView(TemplateView):
    template_name = 'core/simple_upload.html'

    def get(self, request, *args, **kwargs):
        form = DocumentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            data=form.save()
            media_root = settings.MEDIA_ROOT
            file_path = Path(media_root) / 'audio' / form.cleaned_data['audio_file'].name
            text=transcribe_audio(file_path)

            if text:
                document=Document.objects.get(pk=data.pk)
                document.audio_text=text
                document.save()
                return render(request, 'core/index.html', {'text': text})

        return render(request, self.template_name, {'form': form})


class ModelFormTextView(TemplateView):
    template_name = 'core/simple_text.html'

    def get(self, request, *args, **kwargs):
        form = DocumentTextForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = DocumentTextForm(request.POST)
        if form.is_valid():
            data=form.save()
            media_root = settings.MEDIA_ROOT
            text=data.audio_text
            tts = gTTS(text=text, lang='en')
            # Set the save path for the audio file
            save_path = Path(media_root) / 'audio'
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            filename = f'{timestamp}.mp3'
            file_path = os.path.join(save_path, filename)
            tts.save(file_path)
            document=Document.objects.get(pk=data.pk)
            document.audio_file='audio/'+filename
            document.save()
            return render(request, 'core/index.html', {'audio': 'audio/'+filename})

        return render(request, self.template_name, {'form': form})


class DocumentDeleteView(DeleteView):
    model = Document
    success_url = reverse_lazy('home')
    template_name = 'core/document_confirm_delete.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
