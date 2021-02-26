# Generated by Django 3.1.5 on 2021-02-26 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0007_auto_20210226_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapterpath', models.CharField(default='h1', max_length=16)),
                ('path', models.CharField(default='1', max_length=16)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
