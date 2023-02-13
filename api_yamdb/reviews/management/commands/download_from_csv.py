import csv
import os
import pathlib

from chardet import detect
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleAndGenre)
from users.models import User

# Ссылки по теме:
# https://habr.com/ru/post/415049/
# https://docs-python.ru/tutorial/vstroennye-funktsii-interpretatora-python/funktsija-open/
# https://docs-python.ru/packages/modul-chardet-python-opredelenie-kodirovki/
# https://docs-python.ru/standart-library/modul-csv-python/klass-dictreader-modulja-csv/


class Command(BaseCommand):
    FILES_NAME = {
        'users.csv': {'model_proj': User},
        'category.csv': {'model_proj': Category},
        'genre.csv': {'model_proj': Genre},
        'titles.csv': {'model_proj': Title},
        'genre_title.csv': {'model_proj': TitleAndGenre},
        'review.csv': {'model_proj': Review},
        'comments.csv': {'model_proj': Comment}
    }

    RENAME_KEY_FIELDS = ('category', 'author')

    help = 'This script update DB in project from files in ~/static/data'

    def add_arguments(self, parser):
        """Можем добавить к команде аргумент пути, если путь будет не типовой
        python manage.py download_from_csv С:/Div/folder_with_csv/
        """
        parser.add_argument(
            'path_to_dir',
            type=str,
            help='Way to dir with files',
            nargs="?")

    def handle(self, *args, **options):
        path = options['path_to_dir']
        # ********
        # Переходим в папку с файлами
        if path is None:
            # Если папка в аргументах не задана
            os.chdir(settings.BASE_DIR)
            os.chdir("...")
            os.chdir(pathlib.Path.cwd() / 'static' / 'data')
        elif os.path.exists(path):
            #  Если папка пришла из аргументов
            os.chdir(path)
        else:
            #  Иначе ошибка
            raise CommandError(f"Path {path} is not exist")

        # ********
        #  Побежали разбирать файлики и создавать
        #  объекты по соответствующим моделям
        try:
            for file_name, data in Command.FILES_NAME.items():
                # Определяем кодировку файла
                with open(file_name, "rb") as f:
                    encoding_info = detect(f.read())

                # Открываем файл на чтение
                with open(
                    file_name,
                    "r",
                    encoding=encoding_info["encoding"]
                ) as f:
                    reader = list(csv.DictReader(f))
                    if len(reader) == 0:
                        raise CommandError("File is empty")

                model_obj = data['model_proj']
                # Для каждой строки в открытом файле создаем
                # объект соответствующей модели
                for row in reader:
                    for field in Command.RENAME_KEY_FIELDS:
                        if field in row:
                            row[f'{field}_id'] = row[field]
                            del row[field]
                    model_obj.objects.get_or_create(**row)
        except Exception as error:
            raise CommandError("Objects can't to be create", error)
        self.stdout.write(self.style.SUCCESS('Date Base Update.'))
