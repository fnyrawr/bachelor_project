# Generated by Django 4.2 on 2023-04-26 04:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_alter_user_start_contract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='start_contract',
            field=models.DateField(default=datetime.date(2023, 4, 26)),
        ),
    ]
