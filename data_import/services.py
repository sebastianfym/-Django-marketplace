#from goods.models import Goods, GoodsInMarket
import csv
import json
from typing import List


# from goods.models import FeatureName, Feature


# def create_features(features: dict):
#    for key, value in features.items():
#        feature_name = FeatureName.objects.get_or_create(name=key)[0]
#        feature = Feature.objects.get_or_create(value=value)[0]
#        feature.name = feature_name
#        feature.save()


def goods_import() -> List[dict]:
    # model = globals()['Goods']
    file_path = 'goods.csv'
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        list_goods = []
        for num, row in enumerate(reader):
            print(row)
            # dict_goods = {}
            if num == 0:
                key = row
            else:
                fields = dict(zip(key, row[0:4]))
                features = json.loads(row[5])
                fields.update({'features': features})
                list_goods.append(fields)
    return list_goods

goods_import()
#def goods_in_market_impotrt(seller_id: int, goods_for_import: List[dict]):
#   for goods in goods_for_import:
#       goods_name = goods['name']
#       if Goods.objects.filter(name=goods_name):
#           GoodsInMarket.objects.

