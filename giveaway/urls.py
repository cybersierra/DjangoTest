from django.urls import path
from . import views

urlpatterns = [
    path('giveaway/<int:giveaway_id>/enter/', views.enter_giveaway, name='enter_giveaway'),
    path('giveaway/<int:giveaway_id>/select-winner/', views.select_winner_view, name='select_winner'),
]