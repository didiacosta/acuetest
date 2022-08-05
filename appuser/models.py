from django.db import models
from django.conf import settings
# Create your models here.

class AppUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.PROTECT)

    def __str__(self):
        return str(self.user.username) or u''