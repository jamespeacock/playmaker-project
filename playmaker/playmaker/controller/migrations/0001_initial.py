# Generated by Django 2.1.4 on 2019-04-27 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sp_id', models.CharField(max_length=64)),
                ('is_active', models.BooleanField()),
                ('is_private_session', models.BooleanField()),
                ('is_restricted', models.BooleanField()),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=64)),
                ('volume_percent', models.IntegerField()),
            ],
        ),
    ]
