# Generated by Django 2.2 on 2019-08-23 02:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controller',
            name='me',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='controller', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listener',
            name='me',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='listener', to=settings.AUTH_USER_MODEL),
        ),
    ]