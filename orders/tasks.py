from config.celery import app


@app.task
def add_order(order_id, *args, **kwargs):
    print(order_id)
    return order_id

