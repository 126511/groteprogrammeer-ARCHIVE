# Generated by Django 3.1.5 on 2021-02-26 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0006_filepage_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filepage',
            name='chapterpath',
            field=models.CharField(default='h1', max_length=16),
        ),
    ]
