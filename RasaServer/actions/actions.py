from typing import Any, Text, Dict, List
from .utils import cleaned_text, get_json
from .api_operations import get_business_process_step, get_business_type_status, get_business_types, get_senders
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

class ActionWelcome(Action):
    
    def name(self) -> Text:
        return "action_session_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        sender_id = tracker.sender_id
        sender = get_senders(sender_id=sender_id)
        sender_name = "Bạn"

        if len(sender) > 0:
            sender_name = sender[0]['sender_name']

        dispatcher.utter_message(response="utter_welcome", sender_name=sender_name)
        return [SlotSet("sender_name", sender_name)]
    
class ActionBusinessTypes(Action):

    def name(self) -> Text:
        # Liệt kê các loại hình doanh nghiệp
        return "action_list_business_types"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        business_types = get_business_types()
        type_names = [f"- _{business_type['type_description']}_" for business_type in business_types]
        type_names_formatted = '\n'.join(type_names)

        return [SlotSet("business_types", type_names_formatted)]

class ActionRegisterBusinessProcedure(Action):

    def name(self) -> Text:
        # Chọn loại hình doanh nghiệp
        return "action_list_business_type_in_procedure"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        business_types = get_business_types()
        type_names = [f"- _{business_type['type_description']}_" for business_type in business_types]
        type_names_formatted = '\n'.join(type_names)
        
        return [SlotSet("business_types", type_names_formatted)]
    
class ActionRegisterBusinessTypeStatus(Action):

    def name(self) -> Text:
        # Chọn trạng thái của loai hình doanh nghiệp
        return "action_list_business_type_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        business_type_name = tracker.get_slot("business_type")
        business_type_status = get_business_type_status(business_type_name)
        status = [f"- _+st['status_display_full']+_" for st in business_type_status]
        business_type_status_list = '\n'.join(status)
        
        return [SlotSet("business_type_status_list", business_type_status_list)]
    

class ActionListBusinessProcessSteps(Action):

    def name(self) -> Text:
        # Danh sách các bước đăng ký doanh nghiệp
        return "action_list_business_procedure_steps"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        business_type = tracker.get_slot("business_type")
        business_status = tracker.get_slot("business_status")

        business_process_steps = get_business_process_step(business_type=business_type, business_type_status=business_status)
        has_process_steps = True
        if len(business_process_steps) == 0:
            has_process_steps = False
        
        process_steps_formatted = '\n'.join([f'- _{step["step_name"]}_\n' for step in business_process_steps])
        return [SlotSet("has_process_steps", has_process_steps), SlotSet("process_steps", process_steps_formatted)]

class ActionBusinessProcessStepDescription(Action):
    
        def name(self) -> Text:
            # Mô tả bước đăng ký doanh nghiệp
            return "action_business_procedure_step_description"
    
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            business_type = tracker.get_slot("business_type")
            business_status = tracker.get_slot("business_status")
            process_step = tracker.get_slot("process_step")
            
            process_step_description = get_business_process_step(step_name=process_step, business_type=business_type, business_type_status=business_status)
            has_process_step_description = True
            if len(process_step_description) == 0:
                has_process_step_description = False
            
            return [SlotSet("has_process_step_description", has_process_step_description),
                    SlotSet("process_step_description", process_step_description[0]['step_description']), 
                    SlotSet("process_step", process_step)]
        
class ActionLookupBusinessLines(Action):
    
    def name(self) -> Text:
        return "action_lookup_business_lines"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        industrys = get_json('../DjangoServer/sql_data/industry-filter.json')
        industry_name = tracker.latest_message['text']
        
        text_message = f'Một số ngành nghề kinh doanh liên quan (<b>{industry_name})</b> gồm:'
        text_message += '<ul>'
        for industry in industrys:
            if cleaned_text(industry['primary_name']).upper().strip() == cleaned_text(industry_name).upper().strip():
                text_message += ''.join(f"<li>{name}</li>" for name in industry['names'])
        text_message += '</ul>'
        
        dispatcher.utter_message(text=text_message)
        return []
    
class ActionDocumentsBusinessRegistration(Action):
    
    def name(self) -> Text:
        return "action_documents_business_registration"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        document_name = tracker.latest_message['text']
        
        dispatcher.utter_message(text='')
        return []

# class ActionDefaultFallback(Action):
    
#     def name(self) -> Text:
#         return "action_default_fallback"
    
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         dispatcher.utter_message(response="utter_default")
#         return []