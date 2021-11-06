from django.db import models

# Create your models here.

class File(models.Model):
    wFile = models.FileField()



class Audio(models.Model):
    d_notes = models.TextField(blank=True)
    accuracy = models.TextField(blank=True)
    decibel_l = models.TextField(blank=True)

    def get_absolute_url(self):
        return f"/products/{self.id}/"