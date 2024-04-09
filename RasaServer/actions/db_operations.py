import requests
from .db_config import cursor, connection
import json

DJ_BASE_URL = "http://localhost:8000"
GET_SENDER = f"{DJ_BASE_URL}/chat/get_current_user"
BUSINESS_REGISTRATION_BUSINESSTYPE = f"{DJ_BASE_URL}/api/business_registration_businesstype"
GET_BUSINESS_TYPE_STATUS = f"{DJ_BASE_URL}/api/business_type_status"


# def get_business_types():
#     # query = f"SELECT * FROM business_registration_businesstype"
#     # cursor.execute(query)
#     # result = cursor.fetchall()
#     # return result
#     response = requests.get(BUSINESS_REGISTRATION_BUSINESSTYPE)
#     if response.status_code != 200:
#         return []
#     return response.json()

def get_business_type_status(business_type_id):
    if business_type_id is None:
        return []
    query = f"SELECT * FROM business_registration_businesstypestatus WHERE business_type_id = {business_type_id}"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_business_type_status_names(status_codes_db, business_type_status_enum):
    status_names = []
    for code in status_codes_db:
        business_type_status = find_business_type_status_by_code(code, business_type_status_enum)
        if business_type_status != None:
            status_names.append(business_type_status)
    return status_names


def find_business_type_status(status_code, business_type_status_enum):
    for business_type_status in business_type_status_enum:
        if business_type_status != None and business_type_status['code'].strip().lower() == status_code.strip().lower():
            return business_type_status
    return None


def find_business_type_status_by_code(status_code, business_type_status_enum):
    for business_type_status in business_type_status_enum:
        if business_type_status['code'] == status_code:
            return business_type_status
    return None

def find_business_type_status_by_code_and_business_type_id(status_code, business_type_id):
    query = f"SELECT * FROM business_registration_businesstypestatus WHERE business_type_id = {business_type_id} AND status = '{status_code}'"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_business_registration_businessprocessstep(business_type_status_id):
    query = f"SELECT * FROM business_registration_businessprocessstep WHERE business_type_status_id = {business_type_status_id}"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_business_type_id(business_type_name, business_types):
    for business_type in business_types:
        if business_type[1].lower().strip() == business_type_name.lower().strip():
            return business_type[0]
    return None

def check_business_type_status_name(name, status_names):
    for status_name in status_names:
        if status_name['name'].lower().strip() == name.lower().strip():
            return status_name
    return None

def insert_data(data, table_name):
    # Create a cursor object
    cur = connection.cursor()

    # Construct the INSERT query with placeholders for values
    columns = ", ".join(data.keys())
    values = ", ".join(["%s"] * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

    # Execute the query with the data values
    cur.execute(query, tuple(data.values()))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor
    cur.close()


# Get api
def get_api(url_link):
    response = requests.get(url=url_link)
    return response.json()

def get_saved_slots(sender_id):

    query = f"SELECT slot_values FROM chatbot_data_history WHERE sender_id = '{sender_id}' ORDER BY id DESC LIMIT 1"

    saved_slots = {}
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        # Phân tích chuỗi JSON thành đối tượng Python
        slot_values = json.loads(row[0].replace("'", "\""))
        for slot in slot_values:
            saved_slots[slot['name']] = slot['value']
    return saved_slots