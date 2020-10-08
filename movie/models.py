import srt
from django.db import models


class MovieModel(models.Model):
    title = models.TextField('Название фильма')
    description = models.TextField('Описание фильма')
    file_path = models.TextField('Ссылка на видео файл фильма')
    srt_path = models.TextField('Ссылка на файл с субтитрами')

    def get_subtitles(self):
        # Читаем файл с субтитрами
        with open(self.srt_path, 'r') as f:
            subtitles_generator = srt.parse(f.read())

        # Объединяем все реплики субтитров.
        # Убираем ненужные данные из субтитров.
        return '\n'.join([sub.content for sub in subtitles_generator])


def create_fake_data(count_ru: int = int(2.5 * 1000000),
                     count_en: int = int(2.5 * 1000000),
                     batch_size: int = 100000):
    from faker import Faker
    faker_en = Faker()
    faker_ru = Faker('ru_RU')
    print(f'Run fake data: {count_ru + count_en}, batch_size: {batch_size}')
    MovieModel.objects.all().delete()
    movies = []
    for i in range(count_ru):
        movie = MovieModel(
            title=faker_ru.sentence(),
            description=faker_ru.text(),
            file_path=faker_en.file_path(),
            str_path=faker_en.file_path()
        )
        movies.append(movie)
        if len(movies) >= batch_size:
            print(f'RUS: {i} success')
            MovieModel.objects.bulk_create(movies)
            movies = []

    for i in range(count_en):
        movie = MovieModel(
            title=faker_en.sentence(),
            description=faker_en.text(),
            file_path=faker_en.file_path(),
            str_path=faker_en.file_path()
        )
        movies.append(movie)
        if len(movies) >= batch_size:
            print(f'ENG: {i} success')
            MovieModel.objects.bulk_create(movies)
            movies = []
