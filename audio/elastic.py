from django_elasticsearch_dsl import Document,Index
from django_elasticsearch_dsl.registries import registry
from .models import Document as DC

@registry.register_document
class CategoryDocument(Document):
    class Index:
        name = 'document'
    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }
    class Django:
         model = DC
         fields = [
             'description',
             'audio_file',
             'audio_text',
             'uploaded_at'
         ]
