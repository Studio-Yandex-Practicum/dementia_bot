# Generated by Django 4.2.5 on 2024-02-01 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_self', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='image_answer',
            field=models.ImageField(blank=True, null=True, upload_to='image_answer/', verbose_name='Графический ответ на вопрос'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='ranking',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Оценка ответа в баллах'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text_answer',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Текстовый ответ на вопрос'),
        ),
        migrations.AddConstraint(
            model_name='answer',
            constraint=models.UniqueConstraint(fields=('session_id', 'question_id'), name='unique_pair_session_question'),
        ),
    ]
