# Generated by Django 2.2.3 on 2020-03-12 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csapp', '0011_auto_20200312_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uofgstudent',
            name='contact',
            field=models.BooleanField(),
        ),
    ]
