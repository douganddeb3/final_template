# Generated by Django 3.1.3 on 2022-06-15 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecourse', '0007_auto_20220613_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='true_not_selected',
            field=models.ManyToManyField(related_name='true_not_selected', to='onlinecourse.Choice'),
        ),
    ]
