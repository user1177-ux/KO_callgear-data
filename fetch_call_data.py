import requests
import json
import csv
import os
from datetime import datetime

def fetch_call_data():
    api_key = os.getenv('CALLGEAR_API_KEY')
    account_id = os.getenv('CALLGEAR_ACCOUNT_ID')

    # Установка URL для получения данных
    url = f'https://api.callgear.com/v1/accounts/{account_id}/calls'

    # Параметры запроса
    params = {
        'api_key': api_key,
        'date_from': '2020-01-01T00:00:00',  # Начальная дата для получения всех данных
        'date_to': datetime.now().isoformat(),  # Конечная дата - текущая дата
        'status': 'all'  # Получение всех звонков
    }

    # Выполнение запроса
    response = requests.get(url, params=params)

    # Проверка статуса ответа
    if response.status_code == 200:
        data = response.json()
        calls = data.get('calls', [])

        # Создание CSV файла
        with open('call_data.csv', 'w', newline='') as csvfile:
            fieldnames = ['date', 'incoming_calls', 'missed_calls', 'answered_calls']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for call in calls:
                writer.writerow({
                    'date': call.get('startTime'),
                    'incoming_calls': call.get('incoming', 0),
                    'missed_calls': call.get('missed', 0),
                    'answered_calls': call.get('answered', 0)
                })

        print("Данные успешно экспортированы в call_data.csv")
    else:
        print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")

if __name__ == "__main__":
    fetch_call_data()
