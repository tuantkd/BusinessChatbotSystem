# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from .enum import DATA_BUSINESS
from .db_operations import check_business_type_status_name, find_business_type_status_by_code_and_business_type_id, get_business_type_id, get_business_type_status, get_business_type_status_names, get_business_types
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionBusinessTypes(Action):

    def name(self) -> Text:
        return "action_business_types"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent_name = tracker.latest_message['intent']['name']
        
        business_types = get_business_types()
        formatted_business_types = ', '.join(f"{business_type[1]}" for business_type in business_types)
        
        if intent_name == "register_business_procedure":
            dispatcher.utter_message(template="utter_register_business_procedure", business_types=formatted_business_types)
        
        dispatcher.utter_message(template="utter_business_types", entity_business_type=formatted_business_types)
        
        return []
    

class ActionRegisterBusinessProcedure(Action):

    def name(self) -> Text:
        return "action_register_business_procedure"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        business_types = get_business_types()
        formatted_business_types = ', '.join(f"{business_type[1]}" for business_type in business_types)
        
        dispatcher.utter_message(template="utter_register_business_procedure", business_types=formatted_business_types)
        return []
    
    
class ActionRegisterBusinessTypeName(Action):

    def name(self) -> Text:
        return "action_register_business_type_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        business_type_name = tracker.get_slot("business_type")
        
        business_type_id = get_business_type_id(business_type_name, get_business_types())
        business_type_status = get_business_type_status(business_type_id)
        
        status_codes = [code[1] for code in business_type_status]
        status_names = get_business_type_status_names(status_codes, DATA_BUSINESS.BUSINESS_TYPE_STATUS.value)
        
        formatted_business_type_status = ', '.join(f"{status_name['name']}" for status_name in status_names)
        message_text = f"Tiếp theo hãy chọn loại trạng thái đăng ký doanh nghiệp ({business_type_name}): type_of_business={formatted_business_type_status}"
        
        dispatcher.utter_message(text=message_text)
        return []
    

class ActionRegisterTypeOfBusiness(Action):

    def name(self) -> Text:
        return "action_register_type_of_business"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        business_type_name = tracker.get_slot("business_type")
        type_of_business_name = tracker.get_slot("type_of_business")
        
        business_type_id = get_business_type_id(business_type_name, get_business_types())
        business_type_status_all = get_business_type_status(business_type_id)
        status_codes = [code[1] for code in business_type_status_all]
        status_names = get_business_type_status_names(status_codes, DATA_BUSINESS.BUSINESS_TYPE_STATUS.value)
        
        business_type_status_single_enum = check_business_type_status_name(type_of_business_name, status_names)
        business_type_status = find_business_type_status_by_code_and_business_type_id(business_type_status_single_enum['code'], business_type_id)
        
        message_text = f"Đang lấy thông tin"
        dispatcher.utter_message(text=message_text)
        return []
