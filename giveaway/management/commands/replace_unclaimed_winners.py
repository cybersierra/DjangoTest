from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from giveaway.models import Winner, Entry

class Command(BaseCommand):
    help = "Replaces winners whoe prizes were not claimed within 40 days."

    def handle(self, *args, **options):
        cutoff_date = timezone.now() - timedelta(days=40) # the limit for claiming prizes is 40 days

        # builds a queryset of unclaimed winners
        unclaimed = Winner.objects.filter(
            prize_claimed=False,
            selected_date__lte=cutoff_date,
            replaced_by__isnull=True
        )

        count = 0
        # iterates through unclaimed winners and replaces them
        for winner in unclaimed:
            new_entry = (Entry.objects
                         .filter(giveaway=winner.entry.giveaway)
                         .exclude(id=winner.entry.id)
                         .order_by("?")
                         .first()
            )

            # if a new entry is found, create a new winner and link it
            if new_entry:
                new_winner = Winner.objects.create(entry=new_entry, prize=winner.prize)
                winner.replaced_by = new_winner
                winner.save()
                count += 1
                self.stdout.write(f"Replaced winner {winner.entry.user} with {new_entry.user}")

            else:
                self.stdout.write(f"No replacement found for {winner.entry.user}")

        self.stdout.write(f"Total winners replaced: {count}")

