# Generated by Django 5.0.7 on 2024-07-25 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_folder_is_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='music',
            field=models.ManyToManyField(blank=True, related_name='favorite_music', to='library.music'),
        ),
    ]
