from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def country_visited_task(username, country_name):
    logger.info(f'{username} just marked {country_name} as visited!')
    return f'Logged visit for {username} to {country_name}'