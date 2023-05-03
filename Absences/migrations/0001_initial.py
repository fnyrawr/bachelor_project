# Generated by Django 4.2 on 2023-05-03 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField()),
                ('reason', models.IntegerField(choices=[(0, 'sickness (without medical proof'), (1, 'sickness (with medical proof)'), (2, 'private related'), (3, 'business related'), (4, 'other reason')], default=4)),
                ('status', models.IntegerField(choices=[(0, 'sent'), (1, 'not decided'), (2, 'declined'), (3, 'approved')], default=0)),
                ('note', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Absence',
                'verbose_name_plural': 'Absences',
                'ordering': ['employee', 'start_date', 'end_date'],
            },
        ),
    ]