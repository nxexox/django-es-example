from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from movie.documents import MovieDocument


class MovieDocumentSerializer(DocumentSerializer):
    class Meta:
        document = MovieDocument
        fields = (
            'id', 'title', 'description', 'subtitles', 'subtitles.english'
        )
