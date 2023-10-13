import json

from botapp.models import Question, Test
from django.core.management.base import BaseCommand, CommandError


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
                for row in reader['questions']:
                    Question.objects.get_or_create(
                        questionId=row.get('questionId'),
                        question=row.get('question'),
                        score=row.get('score'),
                        type=row.get('type')
                    )
        except FileNotFoundError:
            raise CommandError('Добавьте файл questions.json в директорию data')
