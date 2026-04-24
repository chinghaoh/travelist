from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Country, CountryEntry, TravelItem
from .serializers import (
    CountrySerializer,
    CountryEntrySerializer,
    CountryEntryDetailSerializer,
    TravelItemSerializer,
)

class CountryListView(generics.ListAPIView):
    """
    GET /api/countries/
    Browse all countries. Supports ?search=japan and ?continent=EU
    """
    serializer_class = CountrySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'iso_code', 'region']

    def get_queryset(self):
        query_set = Country.objects.all()
        continent = self.request.query_params.get('continent')
        if continent:
            query_set = query_set.filter(continent=continent.upper())
        return query_set


class CountryDetailView(generics.RetrieveAPIView):
    """
    GET /api/countries/<iso_code>/
    """
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    lookup_field = 'iso_code'


class CountryEntryListView(generics.ListCreateAPIView):
    """
    GET  /api/my-countries/  — list user's tracked countries
    POST /api/my-countries/  — add a country
    """
    def get_serializer_class(self):
        return CountryEntrySerializer

    def get_queryset(self):
        query_set = CountryEntry.objects.filter(user=self.request.user).select_related('country')
        status_filter = self.request.query_params.get('status')
        continent = self.request.query_params.get('continent')
        if status_filter:
            query_set = query_set.filter(status=status_filter)
        if continent:
            query_set = query_set.filter(country__continent=continent.upper())
        return query_set


class CountryEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/my-countries/<id>/  — full detail with items
    PATCH  /api/my-countries/<id>/  — update status or notes
    DELETE /api/my-countries/<id>/  — remove from list
    """
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CountryEntryDetailSerializer
        return CountryEntrySerializer

    def get_queryset(self):
        return CountryEntry.objects.filter(user=self.request.user).select_related('country')


class UserStatsView(APIView):
    """
    GET /api/my-countries/stats/
    """

    def get(self,request):
        entries = CountryEntry.objects.filter(user=request.user)
        stats = {
            'total_tracked': entries.count(),
            'visited': entries.filter(status='visited').count(),
            'want_to_visit': entries.filter(status='want_to_visit').count(),
            'living_there': entries.filter(status='living_there').count(),
            'total_items': TravelItem.objects.filter(
                country_entry__user=request.user
            ).count(),
            'items_done': TravelItem.objects.filter(
                country_entry__user=request.user, is_done=True
            ).count(),
        }
        return Response(stats)


class TravelItemListView(generics.ListCreateAPIView):
    """
    GET  /api/my-countries/<entry_id>/items/
    POST /api/my-countries/<entry_id>/items/
    """
    serializer_class = TravelItemSerializer

    def get_entry(self):
        return generics.get_object_or_404(
            CountryEntry, pk=self.kwargs['entry_id'], user=self.request.user
        )

    def get_queryset(self):
        qs = TravelItem.objects.filter(country_entry=self.get_entry())
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs

    def perform_create(self, serializer):
        serializer.save(country_entry=self.get_entry())


class TravelItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/items/<id>/
    PATCH  /api/items/<id>/
    DELETE /api/items/<id>/
    """
    serializer_class = TravelItemSerializer

    def get_queryset(self):
        return TravelItem.objects.filter(country_entry__user=self.request.user)