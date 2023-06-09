# Generated by Django 4.2 on 2023-04-28 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Departments', '0002_departmentqualifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], default=1)),
                ('date', models.DateField(blank=True, null=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('staff_count', models.IntegerField()),
                ('note', models.TextField(blank=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Departments.department')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
                'ordering': ['department', 'weekday', 'start_time', 'end_time'],
            },
        ),
    ]
