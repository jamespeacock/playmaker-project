# Generated by Django 2.2 on 2019-08-20 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playmaker', '0006_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spmodel',
            name='sp_id',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
