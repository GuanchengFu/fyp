# Generated by Django 2.2 on 2020-04-05 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_notification_button_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='button_class',
            field=models.CharField(default='none', max_length=20),
        ),
    ]
