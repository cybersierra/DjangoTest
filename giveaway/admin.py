from django.contrib import admin
from .models import Giveaway, Prize, Entry, Station, Winner

# In this file, we create the admin interface


# Register your models here.
# this is the admin interface for the Giveaway model
@admin.register(Giveaway)   # this is a decorator which adds the model to the admin site without changing the model itself
class GiveawayAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'giveaway_type', 'station')
    search_fields = ('title', 'description', 'station')
    list_filter = ('station', 'giveaway_type', 'start_date', 'end_date')

# this is the admin interface for the Prize model
@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'giveaway', 'quantity', 'alert_threshold', 'is_low_stock')
    list_filter = ('giveaway',)
    search_fields = ('name', 'giveaway__title')

    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True

# this is the admin interface for the Entry model
@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'giveaway', 'phone_number', 'date_of_birth', 'created_at')
    search_fields = ('user__username', 'phone_number')
    list_filter = ('giveaway__station', 'giveaway__giveaway_type', 'giveaway__start_date', 'giveaway__end_date')
    list_select_related = ('giveaway__station',)

# this is the admin interface for the Winner model
@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('entry_user', 'giveaway', 'prize', 'prize_status',  'selected_date', 'prize_claimed', 'replaced_by')
    list_filter = ('selected_date', 'prize_status', 'prize_claimed')
    search_fields = ('entry__user__username',)
    list_search_related = ('entry', 'prize')

    @admin.display(ordering="entry__user__username", description="Winner")
    def entry_user(self, obj):
        return obj.entry.user.username
    
    @admin.display(description="Giveaway")
    def giveaway(self, obj):
        return obj.entry.giveaway.title

# this is the admin interface for the Station model
@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code", "market", "contact_email")
    ordering = ("name",)