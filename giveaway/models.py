from django.db import models
from django.contrib.auth.models import User #needed for Entry.user

# Create your models here.

# model for a giveaway entry
class Giveaway(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    terms_and_conditions = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    giveaway_type = models.CharField(max_length=100, blank=True)    # not sure what this will be used for, but it might be useful
    station = models.CharField(max_length=100, blank=True)

    def __str__(self):  # if you print an object of this class, you'll see the title
        return self.title
    

