# Generated by Django 3.1.3 on 2022-06-13 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecourse', '0006_remove_question_happy'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='false_but_selected',
            field=models.ManyToManyField(related_name='false_but_selected', to='onlinecourse.Choice'),
        ),
        migrations.AddField(
            model_name='submission',
            name='true_not_selected',
            field=models.ManyToManyField(related_name='true_not_elected', to='onlinecourse.Choice'),
        ),
    ]
