import requests

DJ_BASE_URL = "http://localhost:8000"
SENDER_API = f"{DJ_BASE_URL}/api/senders/"
BUSINESS_TYPE_STATUS_API = f"{DJ_BASE_URL}/api/business_type_status/"
BUSINESS_TYPES_API = f"{DJ_BASE_URL}/api/business_type/"
BUSINESS_PROCEDURE_STEP_API = f"{DJ_BASE_URL}/api/business_procedure_step/"
INDUSTRY_API = f"{DJ_BASE_URL}/api/industry/"
ACTIVITY_FIELD_API = f"{DJ_BASE_URL}/api/activity_field/"
LAWS_API = f"{DJ_BASE_URL}/api/document_laws/"
DECREES_API = f"{DJ_BASE_URL}/api/document_decrees/"
CIRCULARS_API = f"{DJ_BASE_URL}/api/document_circulars/"
DECISIONS_API = f"{DJ_BASE_URL}/api/document_decisions/"
SUBINDUSTRIES_API = f"{DJ_BASE_URL}/api/subindustries/"
HISTORY_API = f"{DJ_BASE_URL}/api/history/"

def get_senders(sender_id=None, sender_name=None):
    params = []
    if sender_id:
        params += [f"sender_id={sender_id}"]
    if sender_name:
        params += [f"sender_name={sender_name}"]
    query_params = "&".join(params)
    response = requests.get(f"{SENDER_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()

def get_history(sender_id=None):
    response = requests.get(f"{SENDER_API}{sender_id}/history/")
    if response.status_code != 200:
        return None
    return response.json()

def get_business_types():
    response = requests.get(BUSINESS_TYPES_API)
    if response.status_code != 200:
        return []
    return response.json()

def get_business_states(business_type=None, business_type_status=None):
    params = []
    if business_type:
        params += [f"business_type_name={business_type}"]
    if business_type_status:
        params += [f"status={business_type_status}"]
    query_params = "&".join(params)
    response = requests.get(f"{BUSINESS_TYPE_STATUS_API}?{query_params}")
    if response.status_code != 200:
        return []
    return response.json()

def get_step_details(step_name=None, business_type=None, business_type_status=None):
    params = []
    if step_name:
        params += [f"step_name={step_name}"]
    if business_type:
        params += [f"business_type_name={business_type}"]
    if business_type_status:
        params += [f"status={business_type_status}"]
    query_params = "&".join(params)

    response = requests.get(f"{BUSINESS_PROCEDURE_STEP_API}?{query_params}")
    if response.status_code != 200:
        return []
    return response.json()

def get_industries(industry_id=None, industry_name=None):
    params = []
    if industry_id:
        params += [f"id={industry_id}"]
    if industry_name:
        params += [f"activity_name={industry_name}"]
    query_params = "&".join(params)
    response = requests.get(f"{INDUSTRY_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()

def get_activity_fields(field_id=None, field_name=None):
    query_params = []
    if field_id:
        query_params += [f"id={field_id}"]
    if field_name:
        query_params += [f"field_name={field_name}"]
    response = requests.get(f"{ACTIVITY_FIELD_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()
    
def get_laws(law_id=None, law_name=None):
    params = []
    if law_id:
        params += [f"id={law_id}"]
    if law_name:
        params += [f"law_name={law_name}"]
    query_params = "&".join(params)
    response = requests.get(f"{LAWS_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()

def get_decrees(decree_id=None, decree_name=None):
    params = []
    if decree_id:
        params += [f"id={decree_id}"]
    if decree_name:
        params += [f"decree_name={decree_name}"]
    query_params = "&".join(params)
    response = requests.get(f"{DECREES_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()
    
def get_circulars(circular_id=None, circular_name=None):
    params = []
    if circular_id:
        params += [f"id={circular_id}"]
    if circular_name:
        params += [f"circular_name={circular_name}"]
    query_params = "&".join(params)
    response = requests.get(f"{CIRCULARS_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()
    
def get_decisions(decision_id=None, decision_name=None):
    params = []
    if decision_id:
        params += [f"id={decision_id}"]
    if decision_name:
        params += [f"decision_name={decision_name}"]
    query_params = "&".join(params)
    response = requests.get(f"{DECISIONS_API}?{query_params}")
    if response.status_code != 200:
        return None
    return response.json()

def get_subindustries(parent_name):
    response = requests.get(f"{SUBINDUSTRIES_API}?parent_name={parent_name}")
    if response.status_code != 200:
        return None
    return response.json()


def update_history(history_id, data):
    response = requests.put(f"{HISTORY_API}{history_id}/", json=data)
    if response.status_code != 200:
        return None
    return response.json()
