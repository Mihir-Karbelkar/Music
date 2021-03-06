# Generated by Django 3.1.2 on 2020-10-12 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_user_accounttype'),
        ('core', '0007_song_listencount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs_artist', to='authentication.artist'),
        ),
    ]
