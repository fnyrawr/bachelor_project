# Generated by Django 4.2 on 2023-05-05 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DataManagement', '0003_file_delete_import'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='filename',
        ),
        migrations.RemoveField(
            model_name='file',
            name='upload_date',
        ),
        migrations.RemoveField(
            model_name='file',
            name='user',
        ),
    ]
