from config.celery import app
from app_shop.services import get_limited_edition_goods


@app.task
def update_offer_day():
    get_limited_edition_goods()
