# Generated by Django 4.2 on 2023-05-09 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Holidays', '0003_alter_holiday_end_date_alter_holiday_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='holiday',
            name='start_date',
            field=models.DateField(),
        ),
    ]