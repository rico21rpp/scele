# Generated by Django 3.0.4 on 2020-04-09 04:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sceleapp', '0020_auto_20200409_0445'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_posted', models.BooleanField(default=False)),
                ('has_replied', models.BooleanField(default=False)),
                ('has_liked', models.BooleanField(default=False)),
                ('has_been_liked_3_times', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
    ]
