# Generated by Django 4.2 on 2023-04-29 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('DayTemplates', '0001_initial'),
        ('ShiftTemplates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayshifttemplates',
            name='shift_template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShiftTemplates.shifttemplate'),
        ),
    ]