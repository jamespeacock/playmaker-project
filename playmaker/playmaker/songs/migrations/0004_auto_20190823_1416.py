# Generated by Django 2.2 on 2019-08-23 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0003_album_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='explicit',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='song',
            name='track_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]