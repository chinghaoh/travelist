from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def country_visited_task(username, country_name):
    logger.info(f'{username} just marked {country_name} as visited!')
    return f'Logged visit for {username} to {country_name}'

@shared_task
def refresh_currency_rates():
    from django.conf import settings
    from .services.currency import fetch_and_store_rates
    fetch_and_store_rates(
        api_key=settings.EXCHANGERATE_API_KEY,
        base='EUR'
    )