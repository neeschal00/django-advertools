from django.db import models

# Create your models here.

class DatasetFile(models.Model):
    file_title = models.CharField(max_length=250)
    file_field = models.FileField(upload_to='datasets/',unique=True)
    added_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["file_title","file_field","added_dt"]

    def __str__(self):
        return self.file_title + " " + str(self.file_field)


