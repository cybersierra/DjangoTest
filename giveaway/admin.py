from django.contrib import admin
from .models import Giveaway, Prize, Entry, Winner

# Register your models here.
# this is the admin interface for the Giveaway model
@admin.register(Giveaway)   # this is a decorator which adds the model to the admin site without changing the model itself
class GiveawayAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'giveaway_type', 'station')
    search_fields = ('title', 'description', 'station')
    list_filter = ('start_date', 'end_date')

# this is the admin interface for the Prize model
@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'giveaway', 'quantity', 'alert_threshold', 'is_low_stock')
    list_filter = ('giveaway',)

    def is_low_stock(self, obj):
        return obj.is_low_stock()
    is_low_stock.boolean = True

# this is the admin interface for the Entry model
@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'giveaway', 'phone_number', 'date_of_birth', 'created_at')
    search_fields = ('user__username', 'phone_number')
    list_filter = ('giveaway', 'created_at')

# this is the admin interface for the Winner model
@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('entry', 'prize', 'selected_date', 'prize_status', 'prize_claimed')
    list_filter = ('selected_date', 'prize_status', 'prize_claimed')
    search_fields = ('entry__user__username',)
