# Generated by Django 4.2 on 2023-04-29 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShiftTemplates', '0002_alter_shifttemplate_break_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shifttemplate',
            name='break_duration',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='shifttemplate',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='shifttemplate',
            name='start_time',
            field=models.TimeField(),
        ),
    ]