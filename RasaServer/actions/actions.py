# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from .db_operations import get_business_types

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
        type_of_business_name = tracker.get_slot("type_of_business")
        
        dispatcher.utter_message(template="utter_register_business_type_name", type_of_business="Các loại đăng ký doanh nghiệp")

        return []
    

class ActionRegisterTypeOfBusiness(Action):

    def name(self) -> Text:
        return "action_register_type_of_business"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        business_types = get_business_types()
        formatted_business_types = ', '.join(f"{business_type[1]}" for business_type in business_types)
        
        dispatcher.utter_message(template="utter_register_type_of_business", contents="Nội dung chi tiết của từng loại")

        return []
