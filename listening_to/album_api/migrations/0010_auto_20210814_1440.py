# Generated by Django 3.1.5 on 2021-08-14 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('album_api', '0009_auto_20210812_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='collection',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='albums', to='album_api.collection'),
        ),
    ]
