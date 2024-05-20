import requests

from enterprise_registration_app.settings import RASA_SERVER_URL

def get_version():
    response = requests.get(f'{RASA_SERVER_URL}/version')
    return response.json()

def get_status():
    response = requests.get(f'{RASA_SERVER_URL}/status')
    return response.json()

def get_tracker(conversation_id):
    response = requests.get(f'{RASA_SERVER_URL}/conversations/{conversation_id}/tracker')
    return response.json()

def add_events_to_tracker(conversation_id, events):
    response = requests.post(f'{RASA_SERVER_URL}/conversations/{conversation_id}/tracker/events', json=events)
    return response.json()

def replace_events_in_tracker(conversation_id, events):
    response = requests.put(f'{RASA_SERVER_URL}/conversations/{conversation_id}/tracker/events', json=events)
    return response.json()

def get_conversation_story(conversation_id):
    response = requests.get(f'{RASA_SERVER_URL}/conversations/{conversation_id}/story')
    return response.content.decode('utf-8')

def execute_action(conversation_id, action):
    response = requests.post(f'{RASA_SERVER_URL}/conversations/{conversation_id}/execute', json=action)
    return response.json()

def trigger_intent(conversation_id, intent):
    response = requests.post(f'{RASA_SERVER_URL}/conversations/{conversation_id}/trigger_intent', json=intent)
    return response.json()

def predict_next_action(conversation_id):
    response = requests.post(f'{RASA_SERVER_URL}/conversations/{conversation_id}/predict')
    return response.json()

def add_message_to_tracker(conversation_id, message):
    response = requests.post(f'{RASA_SERVER_URL}/conversations/{conversation_id}/messages', json=message)
    return response.json()

def train_model(data):
    response = requests.post(f'{RASA_SERVER_URL}/model/train', json=data)
    return response.json()

def evaluate_stories(stories):
    headers = {'Content-Type': 'text/yml'}
    response = requests.post(f'{RASA_SERVER_URL}/model/test/stories', data=stories, headers=headers)
    return response.json()

def evaluate_intents(intents):
    headers = {'Content-Type': 'application/x-yaml'}
    response = requests.post(f'{RASA_SERVER_URL}/model/test/intents', data=intents, headers=headers)
    return response.json()

def predict_action(data):
    response = requests.post(f'{RASA_SERVER_URL}/model/predict', json=data)
    return response.json()

def parse_message(message):
    response = requests.post(f'{RASA_SERVER_URL}/model/parse', json=message)
    return response.json()

def replace_model(model_data):
    response = requests.put(f'{RASA_SERVER_URL}/model', json=model_data)
    return response.json()

def unload_model():
    response = requests.delete(f'{RASA_SERVER_URL}/model')
    return response.json()

def get_domain():
    response = requests.get(f'{RASA_SERVER_URL}/domain')
    return response.json()
