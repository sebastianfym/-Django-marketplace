from config.celery import app


@app.task
def load_data():
    print('задача выполнена')
