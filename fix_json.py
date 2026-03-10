import json

# Список полей, которые нужно проверить (все переводимые поля из ваших моделей)
fields_to_fix = [
    'name_de', 'name_nl',           
    'address_de', 'address_nl',     
    'title_de', 'title_nl',      
    'description_de', 'description_nl',  
    'details_html_de', 'details_html_nl',  
    'features_text_de', 'features_text_nl',  
]

# Загружаем дамп
with open('iprovider_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Проходим по всем объектам
for obj in data:
    fields = obj.get('fields', {})
    for field in fields_to_fix:
        if field in fields and fields[field] is None:
            fields[field] = ""

# Сохраняем исправленный файл
with open('iprovider_data_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Файл исправлен и сохранён как iprovider_data_fixed.json")
