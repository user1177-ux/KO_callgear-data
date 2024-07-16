import requests
import csv
import os
from datetime import datetime

def fetch_call_data():
    access_token = os.getenv('CALLGEAR_ACCESS_TOKEN')
    account_id = os.getenv('CALLGEAR_ACCOUNT_ID')

    if not access_token or not account_id:
        print("ACCESS_TOKEN или ACCOUNT_ID не установлены")
        return

    url = f'https://api.callgear.com/api/v2/calls'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'date_from': '2020-01-01T00:00:00Z',  # Установить на прошлую дату для получения всех данных
        'date_to': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),  # Текущая дата
        'account_id': account_id,
        'fields': 'call_id,call_date_time,call_type,call_status'
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Ошибка при получении данных: {response.text}")
        return

    data = response.json()
    if 'data' not in data:
        print("Данные не найдены")
        return

    calls = data['data']
    result = []
    for call in calls:
        result.append({
            'Дата': call['call_date_time'],
            'Тип': call['call_type'],
            'Статус': call['call_status']
        })

    incoming_calls = len([call for call in result if call['Тип'] == 'incoming'])
    missed_calls = len([call for call in result if call['Статус'] == 'missed'])
    answered_calls = incoming_calls - missed_calls

    with open('call_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['Дата', 'Кол-во входящих звонков', 'Кол-во пропущенных звонков', 'Кол-во принятых звонков']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            'Дата': datetime.now().strftime('%Y-%m-%d'),
            'Кол-во входящих звонков': incoming_calls,
            'Кол-во пропущенных звонков': missed_calls,
            'Кол-во принятых звонков': answered_calls
        })
    print("Данные успешно экспортированы в call_data.csv")

if __name__ == "__main__":
    fetch_call_data()
