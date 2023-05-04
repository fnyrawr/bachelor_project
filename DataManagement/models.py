from django.core.validators import FileExtensionValidator
from django.db import models


class File(models.Model):
    file_upload = models.FileField(upload_to='import_files', validators=[FileExtensionValidator(['xlsx'])])
