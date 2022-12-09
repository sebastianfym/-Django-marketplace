import csv
from decimal import Decimal
from typing import List
from goods.models import Goods, GoodsInMarket


def save_data_to_csv(file_name: str, field_names: list, list_data: List[dict]) -> None:
    """
    Функция записывает в csv файл список данных
    :param file_name: str путь к файлу
    :param field_names: List[str] список имён полей данных
    :param list_data: List[dict] список данных
    :return: None
    """
    with open(file_name, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
        csv_writer.writeheader()
        for item in list_data:
            csv_writer.writerow(item)


def goods_import(seller_id, file_path) -> None:
    with open(file_path, 'r') as csvfile:
        field_names = csvfile.readline().strip().split(';')
        csv_reader = csv.DictReader(csvfile, fieldnames=field_names, delimiter=';')
        list_success_added_goods = []
        list_missing_goods = []
        list_incorrects_data = []
        for row in csv_reader:
            try:
                goods = Goods.objects.filter(name=row['name']).first()
                if goods:
                    product = GoodsInMarket.objects.update_or_create(
                        seller_id=seller_id,
                        goods=goods,
                        price=Decimal(row['price']),
                        free_delivery=row['free_delivery'],
                    )
                    product[0].quantity += int(row['quantity'])
                    product[0].save(update_fields=['quantity'])
                    list_success_added_goods.append(row)
                    print('товар успешно добавлен')
                else:
                    list_missing_goods.append(row)
                    print('этот товар отсутвует в базе портала. Обратитесь к администратору для добавления'
                          ' товара в базу')
            except KeyError:
                list_incorrects_data.append(row)
                print('Некорректно введены данные о товаре.')
        save_data_to_csv('media/temp/success_added.csv', field_names, list_success_added_goods)
        save_data_to_csv('media/temp/missing_goods.csv', field_names, list_missing_goods)
        save_data_to_csv('media/temp/incorrect_data.csv', field_names, list_incorrects_data)
