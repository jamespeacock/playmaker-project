# Generated by Django 2.2.7 on 2020-03-27 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('controller', '0017_auto_20200327_0033'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('controller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='room', to='controller.Controller')),
            ],
        ),
    ]
