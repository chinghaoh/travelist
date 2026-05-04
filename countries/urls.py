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
    path('my-countries/<int:entry_id>/regions/<int:region_id>/fetch-boundary/', views.RegionFetchBoundaryView.as_view(), name='region-fetch-boundary'),

    # Items within a country entry
    path('my-countries/<int:entry_id>/items/', views.TravelItemListView.as_view(), name='item-list'),

    # Single region and item management
    path('regions/<int:pk>/', views.RegionDetailView.as_view(), name='region-detail'),
    path('items/', views.RecentItemsView.as_view(), name='item-list-all'),
    path('items/<int:pk>/', views.TravelItemDetailView.as_view(), name='item-detail'),

    # Photos within a country entry
    path('photos/', views.PhotoView.as_view(), name='photo-list'),
    path('photos/<int:pk>/', views.PhotoView.as_view(), name='photo-detail'),

]