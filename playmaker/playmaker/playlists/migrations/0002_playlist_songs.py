# Generated by Django 2.2.7 on 2020-08-16 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('songs', '0001_initial'),
        ('playlists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(related_name='playlists', to='songs.Song'),
        ),
    ]
