# Generated by Django 2.2.7 on 2020-03-22 03:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('playmaker', '0008_auto_20191026_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('spmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='playmaker.SPModel')),
                ('is_selected', models.BooleanField(null=True)),
                ('is_active', models.BooleanField(null=True)),
                ('is_private_session', models.BooleanField(null=True)),
                ('is_restricted', models.BooleanField(null=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=64)),
                ('volume_percent', models.IntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('playmaker.spmodel',),
        ),
    ]
