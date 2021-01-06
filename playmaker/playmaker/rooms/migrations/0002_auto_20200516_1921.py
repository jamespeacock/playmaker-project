# Generated by Django 2.2.7 on 2020-05-16 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0018_auto_20200516_1921'),
        ('songs', '0009_auto_20200327_0033'),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_song', models.CharField(max_length=256, null=True)),
                ('next_pos', models.IntegerField(default=0)),
                ('controller', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='queue', to='controller.Controller')),
            ],
        ),
        migrations.CreateModel(
            name='SongInQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Queue')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_q', to='songs.Song')),
            ],
        ),
        migrations.AddField(
            model_name='queue',
            name='songs',
            field=models.ManyToManyField(through='rooms.SongInQueue', to='songs.Song'),
        ),
        migrations.AddField(
            model_name='room',
            name='queue',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='room', to='rooms.Queue'),
            preserve_default=False,
        ),
    ]