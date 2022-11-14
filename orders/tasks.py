from config.celery import app


@app.task
def add_order(order_id):
    print(order_id)
    return order_id
