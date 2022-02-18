# Generated by Django 3.1.6 on 2022-02-15 03:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('labtest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabTest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('test_date', models.DateField()),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('result', models.BooleanField(blank=True, null=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='labtest.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.user')),
            ],
        ),
    ]