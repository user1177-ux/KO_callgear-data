import requests
import csv
import os
from datetime import datetime

def fetch_call_data():
    api_key = os.getenv('CALLGEAR_API_KEY')
    account_id = os.getenv('CALLGEAR_ACCOUNT_ID')

    if not api_key or not account_id:
        print("API key or Account ID not set")
        return

    url = f'https://api.callgear.com/v1/accounts/{account_id}/calls/search'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "dateFrom": "2000-01-01",  # начальная дата
        "dateTo": datetime.now().strftime('%Y-%m-%d')  # сегодняшняя дата
    }
    
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return

    try:
        call_data = response.json()
    except Exception as e:
        print(f"Error decoding JSON: {str(e)}")
        return

    if 'items' not in call_data:
        print(f"Unexpected data format: {call_data}")
        return

    print(f"Fetched {len(call_data['items'])} call records")

    calls = call_data['items']

    # Подсчет необходимых данных
    call_stats = {}
    for call in calls:
        date = call['date'].split('T')[0]
        if date not in call_stats:
            call_stats[date] = {'incoming': 0, 'missed': 0, 'answered': 0}
        call_stats[date]['incoming'] += 1
        if call['status'] == 'missed':
            call_stats[date]['missed'] += 1
        else:
            call_stats[date]['answered'] += 1

    # Запись данных в CSV файл
    file_path = 'call_data.csv'
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Дата', 'Кол-во входящих звонков', 'Кол-во пропущенных звонков', 'Кол-во принятых звонков']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for date, stats in sorted(call_stats.items()):
            writer.writerow({
                'Дата': date,
                'Кол-во входящих звонков': stats['incoming'],
                'Кол-во пропущенных звонков': stats['missed'],
                'Кол-во принятых звонков': stats['answered']
            })

    print(f"Data successfully exported to {file_path}")

if __name__ == "__main__":
    fetch_call_data()
