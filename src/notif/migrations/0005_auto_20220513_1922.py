# Generated by Django 3.1.6 on 2022-05-13 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notif', '0004_auto_20220513_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notif',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='notif',
            name='date_read',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
