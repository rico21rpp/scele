# Generated by Django 3.0.4 on 2020-04-21 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sceleapp', '0031_auto_20200422_0530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notif',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
