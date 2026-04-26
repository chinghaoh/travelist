from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    # Reference data — all countries
    path('countries/', views.CountryListView.as_view(), name='country-list'),
    path('countries/<str:iso_code>/', views.CountryDetailView.as_view(), name='country-detail'),

    # User's travel list
    path('my-countries/', views.CountryEntryListView.as_view(), name='entry-list'),
    path('my-countries/stats/', views.UserStatsView.as_view(), name='user-stats'),
    path('my-countries/<int:pk>/', views.CountryEntryDetailView.as_view(), name='entry-detail'),

    # Regions within a country entry
    path('my-countries/<int:entry_id>/regions/', views.RegionListView.as_view(), name='region-list'),

    # Items within a country entry
    path('my-countries/<int:entry_id>/items/', views.TravelItemListView.as_view(), name='item-list'),

    # Single region and item management
    path('regions/<int:pk>/', views.RegionDetailView.as_view(), name='region-detail'),
    path('items/<int:pk>/', views.TravelItemDetailView.as_view(), name='item-detail'),
]