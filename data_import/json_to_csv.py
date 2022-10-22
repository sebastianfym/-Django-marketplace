import json
import csv

with open('new_goods/robot_vacuum_cleaner.json') as file:
    goods = json.load(file)
    #print(*goods, sep='\n')

with open('goods.csv', 'w') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(list(goods[1].keys()))
    for item in goods:
        print(item['features'])
        item['features'] = json.dumps(item['features'])
        print(item['features'])
        writer.writerow(list(item.values()))

