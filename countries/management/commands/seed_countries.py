from django.core.management.base import BaseCommand
from countries.models import Country

COUNTRIES = [
    ("Afghanistan", "AF", "AS", "🇦🇫", "Kabul", "Southern Asia", "004"),
    ("Albania", "AL", "EU", "🇦🇱", "Tirana", "Southern Europe", "008"),
    ("Algeria", "DZ", "AF", "🇩🇿", "Algiers", "Northern Africa", "012"),
    ("Argentina", "AR", "SA", "🇦🇷", "Buenos Aires", "South America", "032"),
    ("Australia", "AU", "OC", "🇦🇺", "Canberra", "Australia and New Zealand", "036"),
    ("Austria", "AT", "EU", "🇦🇹", "Vienna", "Western Europe", "040"),
    ("Belgium", "BE", "EU", "🇧🇪", "Brussels", "Western Europe", "056"),
    ("Brazil", "BR", "SA", "🇧🇷", "Brasília", "South America", "076"),
    ("Canada", "CA", "NA", "🇨🇦", "Ottawa", "Northern America", "124"),
    ("Chile", "CL", "SA", "🇨🇱", "Santiago", "South America", "152"),
    ("China", "CN", "AS", "🇨🇳", "Beijing", "Eastern Asia", "156"),
    ("Colombia", "CO", "SA", "🇨🇴", "Bogotá", "South America", "170"),
    ("Croatia", "HR", "EU", "🇭🇷", "Zagreb", "Southern Europe", "191"),
    ("Czech Republic", "CZ", "EU", "🇨🇿", "Prague", "Eastern Europe", "203"),
    ("Denmark", "DK", "EU", "🇩🇰", "Copenhagen", "Northern Europe", "208"),
    ("Egypt", "EG", "AF", "🇪🇬", "Cairo", "Northern Africa", "818"),
    ("Ethiopia", "ET", "AF", "🇪🇹", "Addis Ababa", "Eastern Africa", "231"),
    ("Finland", "FI", "EU", "🇫🇮", "Helsinki", "Northern Europe", "246"),
    ("France", "FR", "EU", "🇫🇷", "Paris", "Western Europe", "250"),
    ("Germany", "DE", "EU", "🇩🇪", "Berlin", "Western Europe", "276"),
    ("Ghana", "GH", "AF", "🇬🇭", "Accra", "Western Africa", "288"),
    ("Greece", "GR", "EU", "🇬🇷", "Athens", "Southern Europe", "300"),
    ("Hungary", "HU", "EU", "🇭🇺", "Budapest", "Eastern Europe", "348"),
    ("Iceland", "IS", "EU", "🇮🇸", "Reykjavik", "Northern Europe", "352"),
    ("India", "IN", "AS", "🇮🇳", "New Delhi", "Southern Asia", "356"),
    ("Indonesia", "ID", "AS", "🇮🇩", "Jakarta", "South-Eastern Asia", "360"),
    ("Ireland", "IE", "EU", "🇮🇪", "Dublin", "Northern Europe", "372"),
    ("Italy", "IT", "EU", "🇮🇹", "Rome", "Southern Europe", "380"),
    ("Jamaica", "JM", "NA", "🇯🇲", "Kingston", "Caribbean", "388"),
    ("Japan", "JP", "AS", "🇯🇵", "Tokyo", "Eastern Asia", "392"),
    ("Jordan", "JO", "AS", "🇯🇴", "Amman", "Western Asia", "400"),
    ("Kenya", "KE", "AF", "🇰🇪", "Nairobi", "Eastern Africa", "404"),
    ("South Korea", "KR", "AS", "🇰🇷", "Seoul", "Eastern Asia", "410"),
    ("Malaysia", "MY", "AS", "🇲🇾", "Kuala Lumpur", "South-Eastern Asia", "458"),
    ("Mexico", "MX", "NA", "🇲🇽", "Mexico City", "Central America", "484"),
    ("Morocco", "MA", "AF", "🇲🇦", "Rabat", "Northern Africa", "504"),
    ("Netherlands", "NL", "EU", "🇳🇱", "Amsterdam", "Western Europe", "528"),
    ("New Zealand", "NZ", "OC", "🇳🇿", "Wellington", "Australia and New Zealand", "554"),
    ("Nigeria", "NG", "AF", "🇳🇬", "Abuja", "Western Africa", "566"),
    ("Norway", "NO", "EU", "🇳🇴", "Oslo", "Northern Europe", "578"),
    ("Pakistan", "PK", "AS", "🇵🇰", "Islamabad", "Southern Asia", "586"),
    ("Peru", "PE", "SA", "🇵🇪", "Lima", "South America", "604"),
    ("Philippines", "PH", "AS", "🇵🇭", "Manila", "South-Eastern Asia", "608"),
    ("Poland", "PL", "EU", "🇵🇱", "Warsaw", "Eastern Europe", "616"),
    ("Portugal", "PT", "EU", "🇵🇹", "Lisbon", "Southern Europe", "620"),
    ("Romania", "RO", "EU", "🇷🇴", "Bucharest", "Eastern Europe", "642"),
    ("Russia", "RU", "EU", "🇷🇺", "Moscow", "Eastern Europe", "643"),
    ("Saudi Arabia", "SA", "AS", "🇸🇦", "Riyadh", "Western Asia", "682"),
    ("Senegal", "SN", "AF", "🇸🇳", "Dakar", "Western Africa", "686"),
    ("Singapore", "SG", "AS", "🇸🇬", "Singapore", "South-Eastern Asia", "702"),
    ("South Africa", "ZA", "AF", "🇿🇦", "Pretoria", "Southern Africa", "710"),
    ("Spain", "ES", "EU", "🇪🇸", "Madrid", "Southern Europe", "724"),
    ("Sri Lanka", "LK", "AS", "🇱🇰", "Colombo", "Southern Asia", "144"),
    ("Sweden", "SE", "EU", "🇸🇪", "Stockholm", "Northern Europe", "752"),
    ("Switzerland", "CH", "EU", "🇨🇭", "Bern", "Western Europe", "756"),
    ("Thailand", "TH", "AS", "🇹🇭", "Bangkok", "South-Eastern Asia", "764"),
    ("Turkey", "TR", "AS", "🇹🇷", "Ankara", "Western Asia", "792"),
    ("Ukraine", "UA", "EU", "🇺🇦", "Kyiv", "Eastern Europe", "804"),
    ("United Arab Emirates", "AE", "AS", "🇦🇪", "Abu Dhabi", "Western Asia", "784"),
    ("United Kingdom", "GB", "EU", "🇬🇧", "London", "Northern Europe", "826"),
    ("United States", "US", "NA", "🇺🇸", "Washington D.C.", "Northern America", "840"),
    ("Uruguay", "UY", "SA", "🇺🇾", "Montevideo", "South America", "858"),
    ("Venezuela", "VE", "SA", "🇻🇪", "Caracas", "South America", "862"),
    ("Vietnam", "VN", "AS", "🇻🇳", "Hanoi", "South-Eastern Asia", "704"),
]


class Command(BaseCommand):
    help = 'Seed the database with countries'

    def handle(self, *args, **kwargs):
        created = 0
        updated = 0
        for name, iso, continent, flag, capital, region, numeric in COUNTRIES:
            _, was_created = Country.objects.update_or_create(
                iso_code=iso,
                defaults={
                    'name': name,
                    'continent': continent,
                    'flag_emoji': flag,
                    'capital': capital,
                    'region': region,
                    'numeric_code': numeric,
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(f'Done. {created} countries added, {updated} countries updated.')
        )