# Generated by Django 3.1.3 on 2022-06-17 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecourse', '0009_submission_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='question',
            field=models.ManyToManyField(to='onlinecourse.Question'),
        ),
    ]
