# Generated by Django 2.2 on 2019-07-29 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playmaker', '0003_auto_20190716_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='access_token',
            field=models.CharField(blank=True, max_length=511, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=511, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='scope',
            field=models.CharField(blank=True, max_length=511, null=True),
        ),
    ]