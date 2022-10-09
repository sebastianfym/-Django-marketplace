import json

with open('discount_types.json', 'r', encoding='1251') as file:
    f = file.read()
    s = f.encode('utf-8')
    t = s.decode()

with open('discount_types_fix.json', 'w', encoding='utf-8') as new_file:
    json.dump(t, new_file)

