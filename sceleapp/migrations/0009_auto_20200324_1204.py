# Generated by Django 3.0.4 on 2020-03-24 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sceleapp', '0008_auto_20200324_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='activity_type',
            field=models.CharField(choices=[('p', 'Create a post'), ('r', 'Create a reply'), ('l', 'Give a like'), ('n', 'Receive 3 likes')], default='p', max_length=1),
        ),
    ]
