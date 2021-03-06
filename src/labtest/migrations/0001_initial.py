# Generated by Django 3.1.6 on 2022-02-15 03:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('address', models.CharField(max_length=200)),
                ('contact_no', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
