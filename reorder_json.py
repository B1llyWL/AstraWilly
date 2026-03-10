import json

# Загружаем исправленный ранее файл
with open('iprovider_data_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Разделим записи по моделям
vacancies = [obj for obj in data if obj['model'] == 'iprovider.vacancy']
vacancy_locations = [obj for obj in data if obj['model'] == 'iprovider.vacancylocation']
other = [obj for obj in data if obj['model'] not in ['iprovider.vacancy', 'iprovider.vacancylocation']]

# Новый порядок: сначала все остальные, потом вакансии, потом связи
new_data = other + vacancies + vacancy_locations

with open('iprovider_data_ordered.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print("Файл переупорядочен и сохранён как iprovider_data_ordered.json")