# Generated by Django 4.2 on 2023-05-03 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Absences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absence',
            name='reason',
            field=models.IntegerField(choices=[(0, 'sickness (without medical proof)'), (1, 'sickness (with medical proof)'), (2, 'private related'), (3, 'business related'), (4, 'other reason')], default=4),
        ),
    ]
