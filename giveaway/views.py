from django.shortcuts import render, redirect
from .forms import EntryForm
from .models import Entry, Giveaway
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

# Create your views here.

# view to display a giveaway and allow user to enter
@login_required
def enter_giveaway(request, giveaway_id):
    giveaway = Giveaway.objects.get(id=giveaway_id)

    # prevent uers from entering twice
    if Entry.objects.filter(user=request.user, giveaway=giveaway).exists():
        messages.error(request, "You have already entered this giveaway.")
        return redirect('giveaway_already_entered')  # redirect to a page saying they've already entered)
    
    # if form is correctly filled out, save the entry
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.giveaway = giveaway
            entry.save()
            messages.success(request, "You have successfully entered the giveaway!")
            return redirect('giveaway_success')  # redirect to a success page
    else:
        form = EntryForm()

    return render(request, 'giveaway/enter_giveaway.html', {'form': form, 'giveaway': giveaway})

# view to select a winner - this should be restricted to staff users
@staff_member_required
def select_winner_view(request, giveaway_id):
    giveaway = get_object_or_404(Giveaway, id=giveaway_id)
    winner, error = pick_winner_for_giveaway(giveaway)

    if winner:
        messages.success(request, f"Winner selected: {winner.entry.user.username}")
    else:
        messages.error(request, error)
    
    return redirect('admin:giveaway_giveaway_changelist')