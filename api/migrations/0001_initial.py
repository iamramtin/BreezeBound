# Generated by Django 5.1.1 on 2024-09-19 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
                'unique_together': {('city', 'country')},
            },
        ),
        migrations.CreateModel(
            name='ScheduleDestination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_date', models.DateField()),
                ('departure_date', models.DateField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.destination')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.schedule')),
            ],
            options={
                'ordering': ['arrival_date'],
            },
        ),
        migrations.AddField(
            model_name='schedule',
            name='destinations',
            field=models.ManyToManyField(through='api.ScheduleDestination', to='api.destination'),
        ),
    ]
