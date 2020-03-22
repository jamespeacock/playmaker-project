# Generated by Django 2.2.7 on 2020-03-22 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0014_controller_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='controller',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='controller.Controller'),
        ),
    ]
