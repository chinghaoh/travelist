import requests
from ..models import CurrencyRate, CountryEntry

CURRENCY_MAP = {
    'JP': ('JPY', 'Japanese Yen'),
    'AR': ('ARS', 'Argentine Peso'),
    'US': ('USD', 'US Dollar'),
    'GB': ('GBP', 'British Pound'),
    'TR': ('TRY', 'Turkish Lira'),
    'TH': ('THB', 'Thai Baht'),
    'AU': ('AUD', 'Australian Dollar'),
    'CN': ('CNY', 'Chinese Yuan'),
    'IN': ('INR', 'Indian Rupee'),
    'MX': ('MXN', 'Mexican Peso'),
    'KR': ('KRW', 'South Korean Won'),
    'SG': ('SGD', 'Singapore Dollar'),
    'CH': ('CHF', 'Swiss Franc'),
    'SE': ('SEK', 'Swedish Krona'),
    'NO': ('NOK', 'Norwegian Krone'),
    'DK': ('DKK', 'Danish Krone'),
    'PL': ('PLN', 'Polish Zloty'),
    'CZ': ('CZK', 'Czech Koruna'),
    'HU': ('HUF', 'Hungarian Forint'),
    'RO': ('RON', 'Romanian Leu'),
    'BR': ('BRL', 'Brazilian Real'),
    'CA': ('CAD', 'Canadian Dollar'),
    'NZ': ('NZD', 'New Zealand Dollar'),
    'ZA': ('ZAR', 'South African Rand'),
    'EG': ('EGP', 'Egyptian Pound'),
    'MA': ('MAD', 'Moroccan Dirham'),
    'NG': ('NGN', 'Nigerian Naira'),
    'ID': ('IDR', 'Indonesian Rupiah'),
    'MY': ('MYR', 'Malaysian Ringgit'),
    'PH': ('PHP', 'Philippine Peso'),
    'VN': ('VND', 'Vietnamese Dong'),
}

def get_tracked_currencies():
    entries = CountryEntry.objects.select_related('country').all()
    currencies = {}
    for entry in entries:
        iso = entry.country.iso_code
        if iso in CURRENCY_MAP:
            code, name = CURRENCY_MAP[iso]
            currencies[code] = name
    return currencies

def fetch_and_store_rates(api_key, base='EUR'):
    currencies = get_tracked_currencies()
    if not currencies:
        return

    if base != 'EUR':
        currencies['EUR'] = 'Euro'
    if base != 'USD':
        currencies['USD'] = 'US Dollar'

    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}'
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    rates = data.get('conversion_rates', {})

    for code, name in currencies.items():
        if code in rates:
            CurrencyRate.objects.update_or_create(
                code=code,
                base=base,
                defaults={
                    'name': name,
                    'rate': rates[code],
                }
            )