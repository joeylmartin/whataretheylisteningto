# Generated by Django 3.2 on 2021-08-12 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album_api', '0006_alter_album_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ['start_date']},
        ),
        migrations.AlterField(
            model_name='collection',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
