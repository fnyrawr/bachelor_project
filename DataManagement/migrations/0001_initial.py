# Generated by Django 4.2 on 2023-05-03 23:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Import',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('type', models.IntegerField(choices=[(1, 'Qualifications'), (2, 'Departments'), (3, 'Users'), (4, 'Absences'), (5, 'Holiday'), (6, 'Demands')])),
                ('excel_file', models.FileField(upload_to='import_files', validators=[django.core.validators.FileExtensionValidator(['xlsx'])])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
