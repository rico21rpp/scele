# Generated by Django 3.0.4 on 2020-03-11 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.TextField()),
                ('criteria', models.TextField()),
                ('badge_type', models.CharField(choices=[('p', 'participation'), ('s', 'skill')], default='p', max_length=1)),
                ('img', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('is_active', models.BooleanField()),
            ],
            options={
                'ordering': ['is_active'],
            },
        ),
        migrations.CreateModel(
            name='UserApp',
            fields=[
                ('username', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=100)),
                ('age', models.CharField(choices=[('U15', '< 15 tahun'), ('15-19', '15 - 19 tahun'), ('20-24', '20 - 24 tahun'), ('25-29', '25 - 29 tahun'), ('30-34', '30 - 34 tahun'), ('35-39', '35 - 39 tahun'), ('40-44', '40 - 44 tahun'), ('O44', '>= 45 tahun')], max_length=5)),
                ('gender', models.CharField(choices=[('L', 'laki-laki'), ('P', 'perempuan')], max_length=1)),
                ('domisili', models.CharField(choices=[('jab', 'jabodetabek'), ('njj', 'non-jabodetabek jawa'), ('lpj', 'luar pulau jawa')], max_length=3)),
                ('univ', models.CharField(max_length=200)),
                ('degree', models.CharField(choices=[('D1', 'Ahli Pratama'), ('D2', 'Ahli Muda'), ('D3', 'Ahli Madya'), ('D4', 'Sarjana Sains Terapan'), ('S1', 'Sarjana'), ('S2', 'Magister'), ('S3', 'Doktor')], max_length=2)),
                ('angkatan', models.IntegerField()),
                ('faculty', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['first_name'],
            },
        ),
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('msg', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('grade', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.Course')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.UserApp')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('msg', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('grade', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.Course')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.UserApp')),
                ('host_reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sceleapp.UserReply')),
                ('user_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.UserPost')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserBadge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.Badge')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.UserApp')),
            ],
        ),
        migrations.CreateModel(
            name='ReplyLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('user_reply', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.UserReply')),
            ],
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('user_post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.UserPost')),
            ],
        ),
        migrations.CreateModel(
            name='Notif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('notif_type', models.CharField(choices=[('b', 'badge'), ('g', 'grade'), ('l', 'like'), ('r', 'reply')], default='b', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_new', models.BooleanField()),
                ('img', models.CharField(max_length=200)),
                ('link', models.URLField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.Course')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.UserApp')),
            ],
        ),
        migrations.CreateModel(
            name='GivenReplyLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.UserApp')),
                ('reply_like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.ReplyLike')),
            ],
        ),
        migrations.CreateModel(
            name='GivenPostLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.UserApp')),
                ('post_like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sceleapp.PostLike')),
            ],
        ),
    ]
