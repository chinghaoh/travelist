from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    CONTINENT_CHOICES = [
        ('AF', 'Africa'),
        ('AN', 'Antarctica'),
        ('AS', 'Asia'),
        ('EU', 'Europe'),
        ('NA', 'North America'),
        ('OC', 'Oceania'),
        ('SA', 'South America'),
    ]

    name = models.CharField(max_length=100, unique=True, db_index=True)
    iso_code = models.CharField(max_length=2, unique=True)
    continent = models.CharField(max_length=2, choices=CONTINENT_CHOICES)
    flag_emoji = models.CharField(max_length=10, blank=True)
    capital = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    numeric_code = models.CharField(max_length=3, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'countries'

    def __str__(self):
        return f"{self.flag_emoji} {self.name}"

class CountryEntry(models.Model):
    STATUS_CHOICES = [
        ('want_to_visit', 'Want to visit'),
        ('visited', 'Visited'),
        ('living_there', 'Living there'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='country_entries')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='entries')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='want_to_visit')
    visited_at = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'country')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} — {self.country.name} ({self.get_status_display()})"

class Region(models.Model):
    TYPE_CHOICES = [
        ('city', 'City'),
        ('province', 'Province'),
        ('region', 'Region'),
        ('island', 'Island'),
        ('other', 'Other'),
    ]

    country_entry = models.ForeignKey(
        CountryEntry, on_delete=models.CASCADE, related_name='regions'
    )
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='city')
    created_at = models.DateTimeField(auto_now_add=True)
    boundary = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        unique_together = ('country_entry', 'name')

    def __str__(self):
        return f"{self.name} ({self.get_type_display()}) — {self.country_entry.country.name}"

class TravelItem(models.Model):
    CATEGORY_CHOICES = [
        ('landmark', 'Landmark'),
        ('food', 'Food / Dish'),
        ('restaurant', 'Restaurant'),
        ('activity', 'Activity'),
        ('accommodation', 'Accommodation'),
        ('other', 'Other'),
    ]

    country_entry = models.ForeignKey(
        CountryEntry, on_delete=models.CASCADE, related_name='items'
    )
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='items'
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='landmark')
    name = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        status = 'done' if self.is_done else 'pending'
        return f"[{self.get_category_display()}] {self.name} ({status})"
