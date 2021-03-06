# Generated by Django 2.2 on 2019-08-17 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('songs', '0001_initial'),
        ('playmaker', '0006_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Controller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('me', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('controller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='controller.Controller')),
            ],
        ),
        migrations.CreateModel(
            name='Listener',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listeners', to='controller.Group')),
                ('me', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='as_listener', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SongInQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('songs', models.ManyToManyField(through='controller.SongInQueue', to='songs.Song')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scope', models.CharField(max_length=256)),
                ('actor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='controller.Controller')),
                ('listener', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='controller.Listener')),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('spmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='playmaker.SPModel')),
                ('is_active', models.BooleanField()),
                ('is_private_session', models.BooleanField()),
                ('is_restricted', models.BooleanField()),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=64)),
                ('volume_percent', models.IntegerField(null=True)),
                ('listener', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='controller.Listener')),
            ],
            bases=('playmaker.spmodel',),
        ),
        migrations.AddField(
            model_name='controller',
            name='queue',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='controller.Queue'),
        ),
        migrations.AddField(
            model_name='songinqueue',
            name='queue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controller.Queue'),
        ),
        migrations.AddField(
            model_name='songinqueue',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='songs.Song'),
        ),
    ]
