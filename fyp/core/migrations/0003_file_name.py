# Generated by Django 2.1.5 on 2020-02-21 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200221_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(default='test', max_length=70),
            preserve_default=False,
        ),
    ]
