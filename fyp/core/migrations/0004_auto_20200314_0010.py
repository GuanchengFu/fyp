# Generated by Django 2.1.5 on 2020-03-14 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200312_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercandidate',
            name='professor',
            field=models.ManyToManyField(related_name='students', to='core.UserProfessor'),
        ),
    ]