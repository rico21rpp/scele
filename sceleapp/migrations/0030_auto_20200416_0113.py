# Generated by Django 3.0.4 on 2020-04-15 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sceleapp', '0029_auto_20200414_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notif',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
