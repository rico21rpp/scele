# Generated by Django 3.0.4 on 2020-04-13 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sceleapp', '0026_auto_20200413_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notif',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
