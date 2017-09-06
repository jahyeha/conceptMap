from django.db import models


# Create your models here.
class Video(models.Model):
    vid = models.CharField(max_length=100, default="", editable=True)
    title = models.CharField(max_length=60, default="default title", editable=True)
    #
    # def Video(self, _vid, _title):
    #     self.vid = _vid
    #     self.title = _title

    def __str__(self):
        return self.vid
