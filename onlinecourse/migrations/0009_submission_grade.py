# Generated by Django 3.1.3 on 2022-06-16 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecourse', '0008_auto_20220615_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='grade',
            field=models.IntegerField(default=0),
        ),
    ]
