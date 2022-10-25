import requests
from datetime import datetime
import os

NUTRITION_APP_ID = os.environ['NUTRITION_APP_ID']
NUTRITION_API_KEY = os.environ['NUTRITION_API_KEY']
NUTRITION_EXERCISE_ENDPOINT = os.environ['NUTRITION_EXERCISE_ENDPOINT']
SHEET_ENDPOINT = os.environ['SHEET_ENDPOINT']
auth = (os.environ['USERNAME'], os.environ['PASSWORD'])
query = str(input('Tell me which exercises you did: '))

nutrition_parameters = {
    'query': query,
    'gender': 'male',
    'weight_kg': 183,
    'height_cm': 183,
    'age': 22
}

nutrition_headers = {
    'x-app-id': NUTRITION_APP_ID,
    'x-app-key': NUTRITION_API_KEY,
    'x-remote-user-id': '0'
}

response = requests.post(url=NUTRITION_EXERCISE_ENDPOINT, headers=nutrition_headers, json=nutrition_parameters)
result = response.json()

today = datetime.now().strftime('%d/%m/%Y')
now_time = datetime.now().strftime('%X')

for exercise in result['exercises']:
    sheet_input = {
       'workout': {
           'date': today,
           'time': now_time,
           'exercise': exercise['name'].title(),
           'duration': exercise['duration_min'],
           'calories': exercise['nf_calories']
       }
    }
    sheet_response = requests.post(url=SHEET_ENDPOINT, json=sheet_input, auth=auth)
    print(sheet_response.text)

