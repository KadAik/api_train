from django.db import models
import uuid

class Book(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), editable=False)
    title = models.CharField(max_length=255, verbose_name="Book title")
    price = models.DecimalField(max_digits=5, decimal_places=2)
    inventory = models.IntegerField(default=0)
    author = models.ManyToManyField("Author", verbose_name="Write by")
    
    def __str__(self):
        return self.title
    