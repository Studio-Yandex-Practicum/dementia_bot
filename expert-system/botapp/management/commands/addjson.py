import json

from django.core.management.base import BaseCommand, CommandError
from botapp.models import Question


class Command(BaseCommand):
    help = 'loads data from questions.json file into a database'

    def handle(self, *args, **options):
        try:
            with open(
                'data/questions.json',
                'r',
                encoding='UTF-8'
            ) as jsonfile:
                reader = json.load(jsonfile)
                for row in reader:
                    text, question_type = row
                    Question.objects.get_or_create(
                        text=text,
                        question_type=question_type
                    )
        except FileNotFoundError:
            raise CommandError('Добавьте файл questions.json в директорию data')
