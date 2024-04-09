import requests
from .db_config import cursor, connection
import json

DJ_BASE_URL = "http://localhost:8000"
SENDER_API = f"{DJ_BASE_URL}/api/senders/"
BUSINESS_TYPE_STATUS_API = f"{DJ_BASE_URL}/api/business_type_status/"
BUSINESS_TYPES_API = f"{DJ_BASE_URL}/api/business_type/"
BUSINESS_PROCESS_STEP_API = f"{DJ_BASE_URL}/api/business_process_step/"
BUSINESS_INDUSTRY_API = f"{DJ_BASE_URL}/api/business_industry/"
BUSINESS_ACTIVITY_FIELD_API = f"{DJ_BASE_URL}/api/business_activity_field/"
LAWS_API = f"{DJ_BASE_URL}/api/document_laws/"
DECREES_API = f"{DJ_BASE_URL}/api/document_decrees/"
CIRCULARS_API = f"{DJ_BASE_URL}/api/document_circulars/"
DECISIONS_API = f"{DJ_BASE_URL}/api/document_decisions/"

def get_senders(sender_id=None, sender_name=None):
    query_params = ""
    if sender_id:
        query_params += f"sender_id={sender_id}"
    if sender_name:
        query_params += f"sender_name={sender_name}"
    response = requests.get(f"{SENDER_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()

def get_business_types():
    response = requests.get(BUSINESS_TYPES_API)
    if response.status_code != 200:
        return []
    return response.json()

def get_business_type_status(business_type=None, business_type_status=None):
    query_params = ""
    if business_type:
        query_params += f"business_type_name={business_type}"
    if business_type_status:
        query_params += f"status={business_type_status}"
    response = requests.get(f"{BUSINESS_TYPE_STATUS_API}?{query_params}")
    if response.status_code != 200:
        return []
    return response.json()

def get_business_process_step(step_name=None, business_type=None, business_type_status=None):
    query_params = ""
    if step_name:
        query_params += f"step_name={step_name}"
    if business_type:
        query_params += f"business_type_name={business_type}"
    if business_type_status:
        query_params += f"status={business_type_status}"
    response = requests.get(f"{BUSINESS_PROCESS_STEP_API}?{query_params}")
    if response.status_code != 200:
        return []
    return response.json()

def get_industries(industry_id=None, industry_name=None):
    query_params = ""
    if industry_id:
        query_params += f"id={industry_id}"
    if industry_name:
        query_params += f"activity_name={industry_name}"
    response = requests.get(f"{BUSINESS_INDUSTRY_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()

def get_activity_fields(field_id=None, field_name=None):
    query_params = ""
    if field_id:
        query_params += f"id={field_id}"
    if field_name:
        query_params += f"field_name={field_name}"
    response = requests.get(f"{BUSINESS_ACTIVITY_FIELD_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()
    
def get_laws(law_id=None, law_name=None):
    query_params = ""
    if law_id:
        query_params += f"id={law_id}"
    if law_name:
        query_params += f"law_name={law_name}"
    response = requests.get(f"{LAWS_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()

def get_decrees(decree_id=None, decree_name=None):
    query_params = ""
    if decree_id:
        query_params += f"id={decree_id}"
    if decree_name:
        query_params += f"decree_name={decree_name}"
    response = requests.get(f"{DECREES_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()
    
def get_circulars(circular_id=None, circular_name=None):
    query_params = ""
    if circular_id:
        query_params += f"id={circular_id}"
    if circular_name:
        query_params += f"circular_name={circular_name}"
    response = requests.get(f"{CIRCULARS_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()
    
def get_decisions(decision_id=None, decision_name=None):
    query_params = ""
    if decision_id:
        query_params += f"id={decision_id}"
    if decision_name:
        query_params += f"decision_name={decision_name}"
    response = requests.get(f"{DECISIONS_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()