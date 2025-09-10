import random
from datetime import timedelta
from django.utils import timezone
from .models import Entry, Winner, Prize

# this will handle winner selection

def has_won_in_the_last_30_days(user):
    thirty_days_ago = timezone.now() - timedelta(days=30)
    return Winner.objects.filter(
        entry__user=user, selected_date__gte=thirty_days_ago,
        replaced_by__isnull=True
    ).exists()

def pick_winner_for_giveaway(giveaway):
    entries = Entry.objects.filter(giveaway=giveaway)

    eligible_entries = [
        entry for entry in entries
        if entry.is_eligible_age() and not has_won_in_the_last_30_days(entry.user)
    ]

    if not eligible_entries:
        return None, "No available prizes"
    
    selected_entry = random.choice(eligible_entries)

    # assign a prize
    prize = Prize.objects.filter(giveaway=giveaway, quantity__gt=0).first()

    if not prize:
        return None, "No available prizes"
    
    # create winner
    winner = Winner.objects.create(
        entry=selected_entry,
        prize=prize,
    )

    # decrement prize quantity
    prize.quantity -= 1
    prize.save()

    return winner, None

