from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from .tasks import country_visited_task


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
        qs = Country.objects.all()
        continent = self.request.query_params.get('continent')
        if continent:
            qs = qs.filter(continent=continent.upper())
        return qs

    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search', '')
        continent = request.query_params.get('continent', '')
        cache_key = f'countries_{continent}_{search}'
        cached = cache.get(cache_key)

        if cached:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 60 * 24)
        return response


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
    serializer_class = CountryEntrySerializer

    def get_queryset(self):
        qs = CountryEntry.objects.filter(user=self.request.user).select_related('country')
        status_filter = self.request.query_params.get('status')
        continent = self.request.query_params.get('continent')
        if status_filter:
            qs = qs.filter(status=status_filter)
        if continent:
            qs = qs.filter(country__continent=continent.upper())
        return qs

    def perform_create(self, serializer):
        serializer.save()
        cache.delete(f'stats_{self.request.user.id}')


class CountryEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/my-countries/<id>/
    PATCH  /api/my-countries/<id>/
    DELETE /api/my-countries/<id>/
    """
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CountryEntryDetailSerializer
        return CountryEntrySerializer

    def get_queryset(self):
        return CountryEntry.objects.filter(user=self.request.user).select_related('country')

    def perform_update(self, serializer):
        old_status = self.get_object().status
        instance = serializer.save()
        cache.delete(f'stats_{self.request.user.id}')

        if old_status != 'visited' and instance.status == 'visited':
            country_visited_task.delay(
                username=self.request.user.username,
                country_name=instance.country.name,
            )

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(f'stats_{self.request.user.id}')


class UserStatsView(APIView):
    """
    GET /api/my-countries/stats/
    """
    def get(self, request):
        cache_key = f'stats_{request.user.id}'
        cached = cache.get(cache_key)

        if cached:
            return Response(cached)

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

        cache.set(cache_key, stats, timeout=60 * 60)
        return Response(stats)


class TravelItemListView(generics.ListCreateAPIView):
    """
    GET  /api/my-countries/<entry_id>/items/  — list items for a country entry
    POST /api/my-countries/<entry_id>/items/  — add an item (landmark, food, etc.)
    Supports ?category=food filtering.
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
        cache.delete(f'stats_{self.request.user.id}')



class TravelItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/items/<id>/  — get a single item
    PATCH  /api/items/<id>/  — mark as done, edit notes
    DELETE /api/items/<id>/  — remove item
    """
    serializer_class = TravelItemSerializer

    def get_queryset(self):
        return TravelItem.objects.filter(country_entry__user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        cache.delete(f'stats_{self.request.user.id}')

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(f'stats_{self.request.user.id}')