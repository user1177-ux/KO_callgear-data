import requests
import csv
import os
import json
from datetime import datetime

def fetch_call_data():
    api_key = os.getenv('CALLGEAR_API_KEY')
    account_id = os.getenv('CALLGEAR_ACCOUNT_ID')

    if not api_key or not account_id:
        print("CALLGEAR_API_KEY или CALLGEAR_ACCOUNT_ID не установлены")
        return

    url = f'https://api.callgear.com/v2/calls'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    params = {
        'account_id': account_id,
        'from': '2022-01-01',
        'to': datetime.now().strftime('%Y-%m-%d')
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if 'error' in data:
        print(f"Ошибка в ответе API: {data['error']}")
        return

    if 'data' not in data:
        print("Ответ API не содержит ключ 'data'")
        print("Полный ответ:", data)
        return

    result = []
    for call in data['data']:
        result.append({
            'Дата': call.get('startTime'),
            'Кол-во входящих звонков': call.get('incoming'),
            'Кол-во пропущенных звонков': call.get('missed'),
            'Кол-во принятых звонков': call.get('answered')
        })

    if result:
        print(f"Запись {len(result)} записей в файл")
        keys = result[0].keys()
        file_path = 'call_data.csv'
        with open(file_path, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(result)
        
        # Добавляем метку времени в конец файла, чтобы GitHub видел изменения
        with open(file_path, 'a') as f:
            f.write(f"\n# Last updated: {datetime.now().isoformat()}\n")
        
        print("Данные успешно экспортированы в", file_path)
    else:
        print("Нет данных для экспорта")

if __name__ == "__main__":
    fetch_call_data()
