import json
from typing import Any, Text, Dict, List
from .utils import cleaned_text, get_json
from .api_operations import get_business_procedure_step, get_business_type_status, get_business_types, get_history, get_senders
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
        history = get_history(sender_id=sender_id)
        events = []
        if len(history) == 0:
            sender_name = "Bạn"

            if len(sender) > 0:
                sender_name = sender[0]['sender_name']
            events.append(SlotSet("sender_name", sender_name))
        else:
            history = sorted(history, key=lambda x: x['timestamp'])
            history_lastest = history[-1]
            slot_values = json.loads(history_lastest['slot_values'].replace("'", "\"").replace("None", "null").replace("True", "true").replace("False", "false"))
            
            for slot, value in slot_values.items():
                events.append(SlotSet(slot, value))

        dispatcher.utter_message(response="utter_welcome", sender_name=sender_name)
        return [events]
    
class ActionBusinessTypes(Action):

    def name(self) -> Text:
        # Liệt kê các loại hình doanh nghiệp
        # return "action_list_business_types"
        return "action_lay_danh_sach_business_types"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        sender_name = tracker.get_slot("sender_name")
        if sender_name is None:
            sender_name = "Bạn"

        business_types = get_business_types()
        type_names = [f"- {index+1}. _{business_type['type_description']}_" for index, business_type in enumerate(business_types)]
        type_names_formatted = '\n'.join(type_names)
        buttons = [{"title": f"{index+1}", "payload": f"/business_type{{\"business_type\": \"{business_type['type_description']}\"}}"} for index, business_type in enumerate(business_types)]
        
        text = f"""
        Để đăng ký doanh nghiệp, bạn cần thực hiện các bước sau:\n
        Bước đầu tiên bạn chọn Loại hình doanh nghiệp mà bạn muốn đăng ký. \n
        Đây có nhiều loại hình doanh nghiệp:\n
        {type_names_formatted}\n
        **{sender_name}** Bạn chọn loại hình doanh nghiệp nào?
        """
        message_json = {
            "type": "quick_replies",
            "content": {
                "title": text,
                "buttons": buttons
            },
        }
        dispatcher.utter_message(json_message=message_json)

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
        # return "action_list_business_type_status"
        return "action_lay_danh_sach_trang_thai_cua_loai_hinh_nay"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        business_type_name = tracker.get_slot("business_type")
        if business_type_name is None:
            return [SlotSet("has_business_type", False)]
        
        business_type_status = get_business_type_status(business_type_name)
        status = [f"- _{st['status_display_full']}_" for st in business_type_status]
        business_type_status_list = '\n'.join(status)
        
        return [SlotSet("business_type_status_list", business_type_status_list)]
    

class ActionListBusinessProcessSteps(Action):

    def name(self) -> Text:
        # Danh sách các bước đăng ký doanh nghiệp
        # return "action_list_business_procedure_steps"
        return "action_dua_ra_cac_thu_tuc_cua_cong_ty"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        business_type = tracker.get_slot("business_type")
        business_status = tracker.get_slot("business_status")

        if business_type is None:
            return [SlotSet("has_business_type", False)]
        if business_status is None:
            return [SlotSet("has_business_status", False)]

        business_procedure_steps = get_business_procedure_step(business_type=business_type, business_type_status=business_status)
        has_procedure_steps = True
        if len(business_procedure_steps) == 0:
            has_procedure_steps = False
        procedure_steps = [step["step_name"] for step in business_procedure_steps]
        procedure_steps_formatted = '\n'.join([f"- _{step}_" for step in procedure_steps])
        return [SlotSet("has_procedure_steps", has_procedure_steps), SlotSet("procedure_steps", procedure_steps_formatted)]

class ActionBusinessProcessStepDescription(Action):
    
        def name(self) -> Text:
            # Mô tả bước đăng ký doanh nghiệp
            # return "action_business_procedure_step_description"
            return "action_dua_ra_thong_tin_chi_tiet_cua_buoc_thu_tuc"
    
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            business_type = tracker.get_slot("business_type")
            business_status = tracker.get_slot("business_status")
            procedure_step = tracker.get_slot("procedure_step")
            
            if business_type is None:
                return [SlotSet("has_business_type", False)]
            if business_status is None:
                return [SlotSet("has_business_status", False)]
            if procedure_step is None:
                return [SlotSet("has_procedure_step", False)]
            
            procedure_step_description = get_business_procedure_step(step_name=procedure_step, business_type=business_type, business_type_status=business_status)
            has_procedure_step_description = True
            if len(procedure_step_description) == 0:
                has_procedure_step_description = False
            return [SlotSet("has_procedure_step_description", has_procedure_step_description),
                    SlotSet("procedure_step_description", procedure_step_description[0]['step_description']),
                    SlotSet("has_business_type", True),
                    SlotSet("has_business_status", True),
                    SlotSet("has_procedure_step", True)]
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

class ActionDefaultFallback(Action):
    
    def name(self) -> Text:
        return "action_default_fallback"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(response="utter_default")
        return []