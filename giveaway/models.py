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
    
# model for prizes
class Prize(models.Model):
    giveaway = models.ForeignKey(Giveaway, on_delete=models.CASCADE, related_name='prizes') # link to Giveaway model
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    alert_threshold = models.PositiveIntegerField(default=1) # if the quantity gets this low, an alert is sent

    def __str__(self):
        return f"{self.name} ({self.quantity} remaining)" # low quantity alert
    
    def is_low_stock(self):
        return self.quantity <= self.alert_threshold    # function to check if the prize quantity is low
    
# model for entries
class Entry(models.Model):
    giveaway = models.ForeignKey(Giveaway, on_delete=models.CASCADE, related_name='entries') # link to Giveaway model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries') # link to User model
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    extra_fields = models.JSONField(default=dict, blank = True)

    # Meta classes are used to define additional properties for the model
    class Meta:
        unique_together = ('giveaway', 'user') # ensures a user can only enter a giveaway once
        ordering = ['-created_at'] # orders entries by creation date, newest first
    
    # when printing an Entry object, show the username and giveaway title
    def __str__(self):
        return f"{self.user.username} - {self.giveaway.title}"
    
    # check if the user is 18+ 
    def is_eligible_age(self):
        from datetime import date
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age >= 18

# model for winners
class Winner(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='winner') # link to Entry model
    prize = models.ForeignKey(Prize, on_delete=models.SET_NULL, null=True, blank=True) # link to Prize model (using SET_NULL to keep winner record if prize is deleted)
    selected_date = models.DateTimeField(auto_now_add=True)
    prize_claimed = models.BooleanField(default=False)
    prize_claimed_at = models.DateTimeField(null=True, blank=True)
    replaced_by = models.OneToOneField('self', null=True, blank=True, on_delete=models.SET_NULL) # if the winner is replaced, link to the new winner

    # list of choices for prize status
    PRIZE_STATUS_CHOICE =[
        ('pending', 'Pending'),
        ('claimed', 'Claimed'),
        ('expired', 'Expired'),
    ]
    # field to store the current status of the prize
    prize_status = models.CharField(max_length=10, choices=PRIZE_STATUS_CHOICE, default='pending')

    # when printing a Winner object, show the username and giveaway title
    def __str__(self):
        return f"Winner: {self.entry.user.username} ({self.entry.giveaway.title})"