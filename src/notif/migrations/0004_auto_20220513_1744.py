# Generated by Django 3.1.6 on 2022-05-13 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notif', '0003_auto_20220513_1656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notif',
            name='read',
        ),
        migrations.AddField(
            model_name='notif',
            name='date_created',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='notif',
            name='date_read',
            field=models.DateField(blank=True, null=True),
        ),
    ]