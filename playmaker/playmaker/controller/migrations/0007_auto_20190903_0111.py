# Generated by Django 2.2 on 2019-09-03 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0006_auto_20190903_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue',
            name='controller',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='queue', to='controller.Controller'),
        ),
    ]
