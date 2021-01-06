# Generated by Django 2.2 on 2019-08-17 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='artists',
            field=models.ManyToManyField(blank=True, to='songs.Artist'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='genres',
            field=models.ManyToManyField(blank=True, related_name='artists', to='songs.Genre'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='artist_images', to='songs.Image'),
        ),
        migrations.AlterField(
            model_name='song',
            name='artists',
            field=models.ManyToManyField(blank=True, related_name='songs', to='songs.Artist'),
        ),
    ]