# Generated by Django 2.2.7 on 2020-03-22 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playmaker', '0012_user_pollingthread'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_action',
            field=models.FloatField(null=True),
        ),
    ]
