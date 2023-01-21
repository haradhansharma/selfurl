from django.db import models

class Licences(models.Model):
    party_domain = models.URLField()
    key = models.BooleanField()
    validaty = models.DateTimeField()

    def __str__(self):
        return self.party_domain
