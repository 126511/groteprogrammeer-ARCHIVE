# Generated by Django 3.1.5 on 2021-04-06 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0008_latestpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=64)),
                ('definition', models.CharField(max_length=1024)),
            ],
        ),
    ]
