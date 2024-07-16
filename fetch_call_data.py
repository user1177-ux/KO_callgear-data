import requests
import csv
import os
from datetime import datetime

def fetch_call_data():
    api_key = os.getenv('CALLGEAR_API_KEY')
    base_url = "https://api.callgear.com"

    # Начальная дата
    start_date_str = '2000-01-01'  # Используем дату, которая раньше всех возможных данных
    end_date_str = datetime.now().strftime('%Y-%m-%d')

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Запрос данных
    url = f"{base_url}/v1/statistics/calls"
    params = {
        'start': start_date_str,
        'end': end_date_str,
        'group': 'day'
    }

    print(f"Отправка запроса на {url} с параметрами {params}")

    response = requests.get(url, headers=headers, params=params)
    
    print(f"Код состояния ответа: {response.status_code}")
    print(f"Тело ответа: {response.text}")

    # Добавим проверку кода состояния
    if response.status_code != 200:
        print(f"Ошибка HTTP: {response.status_code}")
        return
    
    try:
        data = response.json()
        print(f"Декодированные данные: {data}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return

    if 'error' in data:
        print(f"Ошибка в ответе API: {data['error']}")
        return

    if 'data' not in data:
        print("Ответ API не содержит ключ 'data'")
        print("Полный ответ:", data)
        return

    print(f"Получено {len(data['data'])} записей")

    result = []
    for record in data['data']:
        result.append({
            'Дата': record['date'],
            'Кол-во входящих звонков': record['incoming_calls'],
            'Кол-во пропущенных звонков': record['missed_calls'],
            'Кол-во принятых звонков': record['answered_calls']
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
