#from goods.models import Goods
import csv
import json
from goods.models import FeatureName, Feature



def create_features(features: dict):
    for key, value in features.items():
        feature_name = FeatureName.objects.get_or_create(name=key)[0]
        feature = Feature.objects.get_or_create(value=value)[0]
        feature.name = feature_name
        feature.save()





def data_import():
    #model = globals()['Goods']
    file_path = 'goods.csv'
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for num, row in enumerate(reader):
            if num == 0:
                key = row
            else:
                fields = dict(zip(key, row[0:4]))
                print(fields)
                features = json.loads(row[5])
                print(features)


        #for row in file:
        #    values = file.readline().split(';')
        #    print(values)
        #    product = dict(zip(field_name, values))
        #    features = product['features']
        #    #features = features[1:-1]
        #    #while features.count('""') > 0:
        #    #    features = features.replace('""', '')
        #    #features = json.loads(product['features'])
        #    break
        #print(features, sep='\n')

data_import()




