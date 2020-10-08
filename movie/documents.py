from elasticsearch_dsl import analyzer, analysis
from django_elasticsearch_dsl import Document, fields, Index

from movie.models import MovieModel


movie_index = Index('movies')

# Создаем TokenFilters из документации
russian_stop_filter = analysis.token_filter('russian_stop', type='stop', stopwords='_russian_')
russian_stemmer_filter = analysis.token_filter('russian_stemmer', type='stemmer', language='russian')
english_stop_filter = analysis.token_filter('english_stop', type='stop', stopwords='_english_')
english_stemmer_filter = analysis.token_filter('english_stemmer', type='stemmer', language='english')
english_possessive_stemmer_filter = analysis.token_filter('english_stemmer', type='stemmer',
                                                          language='possessive_english')

# Создаем анализаторы
ru_analyzer = analyzer(
    'ru_analyzer',
    type='custom',
    tokenizer='standard',
    filter=['lowercase', russian_stop_filter, russian_stemmer_filter],
)
en_analyzer = analyzer(
    'en_analyzer',
    type='custom',
    tokenizer='standard',
    filter=[english_possessive_stemmer_filter, 'lowercase', english_stop_filter, english_stemmer_filter]
)
# Добавляем анализаторы в Индекс
movie_index.analyzer(ru_analyzer)
movie_index.analyzer(en_analyzer)


@movie_index.doc_type
class MovieDocument(Document):
    title = fields.TextField(
        analyzer=ru_analyzer,  # Анализатор для индексации
        search_analyzer=ru_analyzer  # Анализатор для поискового запроса
    )
    description = fields.TextField(
        analyzer=ru_analyzer,  # Анализатор для индексации
        search_analyzer=ru_analyzer  # Анализатор для поискового запроса
    )
    subtitles = fields.TextField(
        attr='get_subtitles',
        analyzer=ru_analyzer,  # Анализатор для индексации
        search_analyzer=ru_analyzer,  # Анализатор для поискового запроса
        fields={
            'english': fields.TextField(
                analyzer=en_analyzer,  # Анализатор для индексации
                search_analyzer=en_analyzer  # Анализатор для поискового запроса
            )
        }
    )

    class Django:
        model = MovieModel
        fields = ('id',)
