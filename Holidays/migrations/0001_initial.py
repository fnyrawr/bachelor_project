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
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField()),
                ('status', models.IntegerField(choices=[(0, 'sent'), (1, 'not decided'), (2, 'declined'), (3, 'approved')], default=0)),
                ('note', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Holidays',
                'verbose_name_plural': 'Holidays',
                'ordering': ['employee', 'start_date', 'end_date'],
            },
        ),
    ]