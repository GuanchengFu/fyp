# Generated by Django 2.1.5 on 2020-03-23 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200318_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofessor',
            name='collaborated_professors',
            field=models.ManyToManyField(related_name='_userprofessor_collaborated_professors_+', to='core.UserProfessor'),
        ),
    ]
