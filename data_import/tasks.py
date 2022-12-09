from config.celery import app
from .services import goods_import


@app.task
def load_data(seller_id, file_name):
    goods_import(seller_id, file_name)

    print('задача выполнена')
