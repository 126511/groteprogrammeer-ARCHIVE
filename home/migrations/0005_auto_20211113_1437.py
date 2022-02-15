# Generated by Django 3.2.5 on 2021-11-13 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0004_alter_filepage_options'),
        ('home', '0004_teachers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='filepage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='files.filepage'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
