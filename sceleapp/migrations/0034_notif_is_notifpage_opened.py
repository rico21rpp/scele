# Generated by Django 3.0.4 on 2020-04-23 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sceleapp', '0033_auto_20200423_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='notif',
            name='is_notifpage_opened',
            field=models.BooleanField(default=False),
        ),
    ]
