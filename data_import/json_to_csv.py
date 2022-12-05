import json
import csv
import random

import reader as reader

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

with open('goods.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    with open('purchase.csv', 'w') as purchase_file:
        writer = csv.writer(purchase_file, delimiter=';')
        for num, item in enumerate(reader):
            row = []
            row.extend(item)
            if num == 0:
                row.extend(['quantity', 'free_delivery'])
            else:
                row.extend([random.randint(20, 30),
                            random.randint(0, 1)])
            writer.writerow(row)






