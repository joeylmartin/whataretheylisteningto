# Generated by Django 3.1.5 on 2022-03-19 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album_api', '0034_auto_20220318_2028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ['creator', 'title']},
        ),
    ]
