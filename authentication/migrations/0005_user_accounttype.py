# Generated by Django 3.1.2 on 2020-10-11 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_remove_user_accounttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='accountType',
            field=models.CharField(choices=[('A', 'Artist'), ('C', 'Consumer')], default='A', max_length=1),
            preserve_default=False,
        ),
    ]
