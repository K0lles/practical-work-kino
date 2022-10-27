import os

from django.db import models
from django.utils import timezone


class MailFile(models.Model):
    file = models.FileField(upload_to='mail-files/')
    created_at = models.DateTimeField(default=timezone.now)

    def filename(self):
        return os.path.basename(self.file.name)
