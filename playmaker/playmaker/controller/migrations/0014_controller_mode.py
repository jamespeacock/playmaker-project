# Generated by Django 2.2.7 on 2020-03-20 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0013_auto_20191114_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='controller',
            name='mode',
            field=models.CharField(choices=[('broadcast', 'broadcast'), ('curate', 'curate')], default='broadcast', max_length=128),
            preserve_default=False,
        ),
    ]
