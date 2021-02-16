# Generated by Django 2.2.7 on 2020-08-16 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('playmaker', '0002_auto_20200816_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('spmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='playmaker.SPModel')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('uri', models.CharField(max_length=255, null=True)),
            ],
            bases=('playmaker.spmodel',),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('spmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='playmaker.SPModel')),
                ('name', models.CharField(max_length=255)),
                ('popularity', models.IntegerField(null=True)),
                ('uri', models.CharField(max_length=255, null=True)),
                ('num_followers', models.IntegerField(null=True)),
            ],
            bases=('playmaker.spmodel',),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('spmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='playmaker.SPModel')),
                ('name', models.CharField(max_length=255)),
                ('uri', models.CharField(max_length=255)),
                ('duration_ms', models.IntegerField(null=True)),
                ('popularity', models.IntegerField(null=True)),
                ('preview_url', models.CharField(max_length=255, null=True)),
                ('explicit', models.BooleanField(blank=True, default=False)),
                ('track_number', models.IntegerField(blank=True, null=True)),
                ('position_ms', models.IntegerField(null=True)),
                ('albums', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='songs_rel', to='songs.Album')),
                ('artists', models.ManyToManyField(blank=True, related_name='songs_rel', to='songs.Artist')),
            ],
            bases=('playmaker.spmodel',),
        ),
        migrations.AddField(
            model_name='artist',
            name='genres',
            field=models.ManyToManyField(blank=True, related_name='artists', to='songs.Genre'),
        ),
        migrations.AddField(
            model_name='artist',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='artist', to='songs.Image'),
        ),
        migrations.AddField(
            model_name='album',
            name='artists',
            field=models.ManyToManyField(blank=True, to='songs.Artist'),
        ),
        migrations.AddField(
            model_name='album',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='album', to='songs.Image'),
        ),
    ]
