from django.core.management.base import BaseCommand
from countries.models import Country

COUNTRIES = [
    ("Afghanistan", "AF", "AS", "🇦🇫", "Kabul", "Southern Asia"),
    ("Albania", "AL", "EU", "🇦🇱", "Tirana", "Southern Europe"),
    ("Algeria", "DZ", "AF", "🇩🇿", "Algiers", "Northern Africa"),
    ("Argentina", "AR", "SA", "🇦🇷", "Buenos Aires", "South America"),
    ("Australia", "AU", "OC", "🇦🇺", "Canberra", "Australia and New Zealand"),
    ("Austria", "AT", "EU", "🇦🇹", "Vienna", "Western Europe"),
    ("Belgium", "BE", "EU", "🇧🇪", "Brussels", "Western Europe"),
    ("Brazil", "BR", "SA", "🇧🇷", "Brasília", "South America"),
    ("Canada", "CA", "NA", "🇨🇦", "Ottawa", "Northern America"),
    ("Chile", "CL", "SA", "🇨🇱", "Santiago", "South America"),
    ("China", "CN", "AS", "🇨🇳", "Beijing", "Eastern Asia"),
    ("Colombia", "CO", "SA", "🇨🇴", "Bogotá", "South America"),
    ("Croatia", "HR", "EU", "🇭🇷", "Zagreb", "Southern Europe"),
    ("Czech Republic", "CZ", "EU", "🇨🇿", "Prague", "Eastern Europe"),
    ("Denmark", "DK", "EU", "🇩🇰", "Copenhagen", "Northern Europe"),
    ("Egypt", "EG", "AF", "🇪🇬", "Cairo", "Northern Africa"),
    ("Ethiopia", "ET", "AF", "🇪🇹", "Addis Ababa", "Eastern Africa"),
    ("Finland", "FI", "EU", "🇫🇮", "Helsinki", "Northern Europe"),
    ("France", "FR", "EU", "🇫🇷", "Paris", "Western Europe"),
    ("Germany", "DE", "EU", "🇩🇪", "Berlin", "Western Europe"),
    ("Ghana", "GH", "AF", "🇬🇭", "Accra", "Western Africa"),
    ("Greece", "GR", "EU", "🇬🇷", "Athens", "Southern Europe"),
    ("Hungary", "HU", "EU", "🇭🇺", "Budapest", "Eastern Europe"),
    ("Iceland", "IS", "EU", "🇮🇸", "Reykjavik", "Northern Europe"),
    ("India", "IN", "AS", "🇮🇳", "New Delhi", "Southern Asia"),
    ("Indonesia", "ID", "AS", "🇮🇩", "Jakarta", "South-Eastern Asia"),
    ("Ireland", "IE", "EU", "🇮🇪", "Dublin", "Northern Europe"),
    ("Italy", "IT", "EU", "🇮🇹", "Rome", "Southern Europe"),
    ("Jamaica", "JM", "NA", "🇯🇲", "Kingston", "Caribbean"),
    ("Japan", "JP", "AS", "🇯🇵", "Tokyo", "Eastern Asia"),
    ("Jordan", "JO", "AS", "🇯🇴", "Amman", "Western Asia"),
    ("Kenya", "KE", "AF", "🇰🇪", "Nairobi", "Eastern Africa"),
    ("South Korea", "KR", "AS", "🇰🇷", "Seoul", "Eastern Asia"),
    ("Malaysia", "MY", "AS", "🇲🇾", "Kuala Lumpur", "South-Eastern Asia"),
    ("Mexico", "MX", "NA", "🇲🇽", "Mexico City", "Central America"),
    ("Morocco", "MA", "AF", "🇲🇦", "Rabat", "Northern Africa"),
    ("Netherlands", "NL", "EU", "🇳🇱", "Amsterdam", "Western Europe"),
    ("New Zealand", "NZ", "OC", "🇳🇿", "Wellington", "Australia and New Zealand"),
    ("Nigeria", "NG", "AF", "🇳🇬", "Abuja", "Western Africa"),
    ("Norway", "NO", "EU", "🇳🇴", "Oslo", "Northern Europe"),
    ("Pakistan", "PK", "AS", "🇵🇰", "Islamabad", "Southern Asia"),
    ("Peru", "PE", "SA", "🇵🇪", "Lima", "South America"),
    ("Philippines", "PH", "AS", "🇵🇭", "Manila", "South-Eastern Asia"),
    ("Poland", "PL", "EU", "🇵🇱", "Warsaw", "Eastern Europe"),
    ("Portugal", "PT", "EU", "🇵🇹", "Lisbon", "Southern Europe"),
    ("Romania", "RO", "EU", "🇷🇴", "Bucharest", "Eastern Europe"),
    ("Russia", "RU", "EU", "🇷🇺", "Moscow", "Eastern Europe"),
    ("Saudi Arabia", "SA", "AS", "🇸🇦", "Riyadh", "Western Asia"),
    ("Senegal", "SN", "AF", "🇸🇳", "Dakar", "Western Africa"),
    ("Singapore", "SG", "AS", "🇸🇬", "Singapore", "South-Eastern Asia"),
    ("South Africa", "ZA", "AF", "🇿🇦", "Pretoria", "Southern Africa"),
    ("Spain", "ES", "EU", "🇪🇸", "Madrid", "Southern Europe"),
    ("Sri Lanka", "LK", "AS", "🇱🇰", "Colombo", "Southern Asia"),
    ("Sweden", "SE", "EU", "🇸🇪", "Stockholm", "Northern Europe"),
    ("Switzerland", "CH", "EU", "🇨🇭", "Bern", "Western Europe"),
    ("Thailand", "TH", "AS", "🇹🇭", "Bangkok", "South-Eastern Asia"),
    ("Turkey", "TR", "AS", "🇹🇷", "Ankara", "Western Asia"),
    ("Ukraine", "UA", "EU", "🇺🇦", "Kyiv", "Eastern Europe"),
    ("United Arab Emirates", "AE", "AS", "🇦🇪", "Abu Dhabi", "Western Asia"),
    ("United Kingdom", "GB", "EU", "🇬🇧", "London", "Northern Europe"),
    ("United States", "US", "NA", "🇺🇸", "Washington D.C.", "Northern America"),
    ("Uruguay", "UY", "SA", "🇺🇾", "Montevideo", "South America"),
    ("Venezuela", "VE", "SA", "🇻🇪", "Caracas", "South America"),
    ("Vietnam", "VN", "AS", "🇻🇳", "Hanoi", "South-Eastern Asia"),
]


class Command(BaseCommand):
    help = 'Seed the database with countries'

    def handle(self, *args, **kwargs):
        created = 0
        for name, iso, continent, flag, capital, region in COUNTRIES:
            _, was_created = Country.objects.get_or_create(
                iso_code=iso,
                defaults={
                    'name': name,
                    'continent': continent,
                    'flag_emoji': flag,
                    'capital': capital,
                    'region': region,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f'Done. {created} countries added, {len(COUNTRIES) - created} already existed.')
        )