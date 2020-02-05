# Generated by Django 2.1.5 on 2020-02-01 18:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'verbose_name_plural': 'Files'},
        ),
        migrations.AlterModelOptions(
            name='folder',
            options={'verbose_name_plural': 'Folders'},
        ),
        migrations.AddField(
            model_name='file',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='file',
            name='modified',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
