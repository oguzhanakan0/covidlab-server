# Generated by Django 3.1.6 on 2022-03-21 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labtest', '0004_auto_20220321_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='slug',
            field=models.SlugField(default='location', max_length=40),
            preserve_default=False,
        ),
    ]
