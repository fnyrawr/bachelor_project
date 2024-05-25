# Generated by Django 5.0.6 on 2024-05-25 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], default=1)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('tendency', models.IntegerField(choices=[(0, 'No preference'), (1, 'Early shift'), (2, 'Midday shift'), (3, 'Late shift'), (4, 'Night shift')], default=0)),
                ('is_available', models.BooleanField(default=True)),
                ('note', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Availability',
                'verbose_name_plural': 'Availabilities',
                'ordering': ['-is_available', 'weekday', 'tendency', 'start_time', 'end_time', 'employee'],
            },
        ),
    ]
