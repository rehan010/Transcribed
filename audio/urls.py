from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name="main"),
    path('home/', HomeView.as_view(), name="home"),
    path('simple_audio/', ModelFormUploadView.as_view(), name="audio"),
    path('simple_text/', ModelFormTextView.as_view(), name="text"),
    path('documents/<int:pk>/delete/', DocumentDeleteView.as_view(), name='document_delete'),
]
