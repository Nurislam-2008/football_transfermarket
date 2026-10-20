from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlayerListView.as_view(), name='player_list'),
    path('player/<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
    path('club/<int:pk>/', views.ClubDetailView.as_view(), name='club_detail'),
]