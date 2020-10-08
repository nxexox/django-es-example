from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from movie.documents import MovieDocument
from movie.serializers import MovieDocumentSerializer


class MovieViewSet(DocumentViewSet):
    document = MovieDocument
    serializer_class = MovieDocumentSerializer
    filter_backends = [SearchFilterBackend,]
    search_fields = ('title', 'description', 'subtitles', 'subtitles.english')
