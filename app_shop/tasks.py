from config.celery import app
from app_shop.services import get_limited_edition_goods, limit_edition_goods


@app.task
def update_offer_day():
    limit_edition_goods.pop(0)
    limit_edition_goods.append(get_limited_edition_goods())


#@app.task
#    def test():
