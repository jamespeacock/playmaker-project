# Generated by Django 2.2.7 on 2019-11-14 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0011_auto_20191114_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='uri',
        ),
    ]
