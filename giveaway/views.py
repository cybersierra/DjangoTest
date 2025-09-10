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
        merssages.error(request, "You have already entered this giveaway.")
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