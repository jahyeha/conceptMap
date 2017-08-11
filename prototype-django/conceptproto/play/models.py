from django.db import models

# Create your models here.
class Video(models.Model):
    vid = models.CharField(max_length=20, default="00000000000", editable=True)
    title = models.CharField(max_length=60, default="default title", editable=True)

    def __str__(self):
        return self.vid
