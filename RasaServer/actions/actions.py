import json
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from .api_operations import (get_business_states, get_business_types,
                             get_history, get_senders, get_step_details, get_subindustries)
from .utils import cleaned_text, get_closest_activity, get_closest_step, get_first_level_code, get_json


class ActionWelcome(Action):

    def name(self) -> Text:
        return "action_session_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

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
            history_latest = history[-1]
            slot_values_str = history_latest['slot_values'].replace("'", "\"").replace("None", "null").replace("True", "true").replace("False", "false")

            try:
                slot_values = json.loads(slot_values_str)
                if isinstance(slot_values, list):
                    for slot_dict in slot_values:
                        if isinstance(slot_dict, dict) and "name" in slot_dict and "value" in slot_dict:
                            events.append(SlotSet(slot_dict["name"], slot_dict["value"]))
                else:
                    raise ValueError("Slot values should be a list of dictionaries")
            except json.JSONDecodeError as e:
                dispatcher.utter_message(text=f"Error parsing slot values: {e}")
            except ValueError as e:
                dispatcher.utter_message(text=f"Error: {e}")

        dispatcher.utter_message(response="utter_welcome", sender_name=sender_name)
        return events
    

class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Lấy intent dự đoán và độ tự tin
        latest_message = tracker.latest_message
        intent_ranking = latest_message.get('intent_ranking', [])

        # Kiểm tra độ tự tin lớn nhất của intent
        if intent_ranking and intent_ranking[0]['confidence'] >= 0.5:
            top_intents = intent_ranking[:3]  # Lấy 3 intent có độ tự tin cao nhất
            buttons = []

            for intent in top_intents:
                intent_name = intent['name']
                metadata = domain['intents'][intent_name].get('metadata', {})
                title = metadata.get('title', intent_name)
                buttons.append({
                    "title": title,
                    "payload": f"/{intent_name}"
                })

            dispatcher.utter_message(
                text="Tôi không chắc chắn về câu hỏi của bạn. Bạn có thể chọn một trong các tùy chọn sau:",
                buttons=buttons
            )
        else:
            dispatcher.utter_message(response="utter_default")

        return []
    
class ActionListBusinessTypes(Action):

    def name(self) -> Text:
        return "action_list_business_types"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        sender_name = tracker.get_slot("sender_name")
        if sender_name is None:
            sender_name = "Bạn"

        business_types = get_business_types()
        if not business_types:
            dispatcher.utter_message(text="Không tìm thấy loại hình doanh nghiệp nào.")
            return []

        type_names = [f"- {index+1}. _{business_type['type_description']}_" for index, business_type in enumerate(business_types)]
        type_names_formatted = '\n'.join(type_names)
        buttons = [{"title": f"{index+1}",
                    "description": f"{business_type['type_description']}",
                    "payload": f"/business_type{{\"business_type\": \"{business_type['type_description']}\"}}"
                    } for index, business_type in enumerate(business_types)
                ]
        
        text = f"""
        Để đăng ký doanh nghiệp, bước đầu tiên bạn chọn loại hình doanh nghiệp mà bạn muốn đăng ký. \n
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

        return []

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
    
class ActionListBusinessStates(Action):

    def name(self) -> Text:
        return "action_list_business_states"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        business_type = tracker.get_slot("business_type")
        if not business_type:
            dispatcher.utter_message(text="Vui lòng chọn loại hình doanh nghiệp trước.")
            return []

        business_states = get_business_states(business_type)
        if not business_states:
            dispatcher.utter_message(text=f"Không tìm thấy trạng thái nào cho loại hình doanh nghiệp {business_type}.")
            return []

        state_names = [f"- {index+1}. _{business_state['status_display_full']}_" for index, business_state in enumerate(business_states)]
        state_names_formatted = '\n'.join(state_names)
        buttons = [{"title": f"{index+1}",
                    "description": f"{business_state['status_display_full']}",
                    "payload": f"/select_business_state{{\"business_state\": \"{business_state['status_display_full']}\"}}"
                    } for index, business_state in enumerate(business_states)
                ]
        
        text = f"""
        Bạn đã chọn loại hình doanh nghiệp: **{business_type}** \n
        Vui lòng chọn trạng thái của doanh nghiệp:\n
        {state_names_formatted}\n
        Bạn chọn trạng thái nào?
        """
        message_json = {
            "type": "quick_replies",
            "content": {
                "title": text,
                "buttons": buttons
            },
        }

        dispatcher.utter_message(json_message=message_json)

        return []
class ActionBusinessStates(Action):
    
    def name(self) -> Text:
        return "action_business_states"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Lấy entity loại hình doanh nghiệp
        entities = tracker.latest_message['entities']
        business_type = None
        for entity in entities:
            if entity['entity'] == 'business_type':
                business_type = entity['value']
                break
        
        if business_type:
            # Lấy các trạng thái của loại hình doanh nghiệp
            business_states = get_business_states(business_type)
            if business_states:
                states_list = [state for state in business_states]
                states_text = ", ".join(states_list)
                dispatcher.utter_message(text=f"Đây là các trạng thái của loại hình doanh nghiệp {business_type}: {states_text}")
            else:
                dispatcher.utter_message(text=f"Không tìm thấy trạng thái nào cho loại hình doanh nghiệp {business_type}.")
        else:
            # Lấy danh sách các loại hình doanh nghiệp
            business_types = get_business_types()
            if business_types:
                type_names = [f"- _{business_type['type_description']}_" for business_type in business_types]
                type_names_formatted = '\n'.join(type_names)
                buttons = [{"title": f"{index+1}. {business_type}",
                            "payload": f"/inform{{\"business_type\": \"{business_type}\"}}"
                            } for index, business_type in enumerate(business_types)]
                
                message_json = {
                    "type": "quick_replies",
                    "content": {
                        "title": f"Tùy thuộc vào loại hình doanh nghiệp nào thì sẽ có các trạng thái tương ứng. Sau đây là danh sách các loại hình doanh nghiệp:\n{type_names_formatted}",
                        "buttons": buttons
                    },
                }
                dispatcher.utter_message(json_message=message_json)
            else:
                dispatcher.utter_message(text="Không tìm thấy loại hình doanh nghiệp nào.")
        
        return []

class ActionListBusinessSteps(Action):

    def name(self) -> Text:
        return "action_list_business_steps"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        business_type = tracker.get_slot("business_type")
        if not business_type:
            dispatcher.utter_message(text="Vui lòng chọn loại hình doanh nghiệp trước.")
            return []
        
        business_state = tracker.get_slot("business_state")
        if not business_state:
            dispatcher.utter_message(text="Vui lòng chọn trạng thái doanh nghiệp trước.")
            return []

        business_steps = get_step_details(business_type=business_type, business_type_status=business_state)
        if not business_steps:
            dispatcher.utter_message(text=f"Không tìm thấy bước hoặc trường hợp nào cho trạng thái **{business_state}** của loại hình doanh nghiệp **{business_type}**.")
            return []

        step_names = [f"- {index+1}. _{business_step['step_name']}_" for index, business_step in enumerate(business_steps)]
        step_names_formatted = '\n'.join(step_names)
        buttons = [{"title": f"{index+1}",
                    "description": f"{business_step['step_name']}",
                    "payload": f"/select_business_step{{\"business_step\": \"{business_step['step_name']}\"}}"
                    } for index, business_step in enumerate(business_steps)
                ]
        
        text = f"""
        Bạn đã chọn trạng thái doanh nghiệp: **{business_state}** của loại hình doanh nghiệp: **{business_type}**\n
        Vui lòng chọn bước hoặc trường hợp:\n
        {step_names_formatted}\n
        Bạn chọn bước hoặc trường hợp nào?
        """
        message_json = {
            "type": "quick_replies",
            "content": {
                "title": text,
                "buttons": buttons
            },
        }

        dispatcher.utter_message(json_message=message_json)

        return []
    
class ActionListStepDetails(Action):
    
    def name(self) -> Text:
        return "action_list_step_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        last_message = tracker.latest_message.get('text')

        business_type = tracker.get_slot("business_type")
        if not business_type:
            dispatcher.utter_message(text="Vui lòng chọn loại hình doanh nghiệp trước.")
            return []

        business_state = tracker.get_slot("business_state")
        if not business_state:
            dispatcher.utter_message(text="Vui lòng chọn trạng thái doanh nghiệp trước.")
            return []
        
        business_step = tracker.get_slot("business_step")
        process_steps = get_step_details(business_type=business_type, business_type_status=business_state)
        if not business_step:
            step_detail = get_closest_step(input_text=last_message, steps=process_steps)
            
        else:
            step_detail = get_closest_step(input_text=business_step, steps=process_steps)
        
        if not step_detail:
            dispatcher.utter_message(text=f"Không tìm thấy chi tiết nào cho bước **{business_step}**, trạng thái **{business_state}** của loại hình doanh nghiệp **{business_type}**.")
            return []
        business_step = step_detail['step_name']
        step_details = [step_detail]
        
        if not step_details:
            dispatcher.utter_message(text=f"Không tìm thấy chi tiết nào cho bước **{business_step}**, trạng thái **{business_state}** của loại hình doanh nghiệp **{business_type}**.")
            return []

        # Construct a single message string
        details_formatted = '\n'.join([f"{detail['step_description']}" for detail in step_details])
        
        text = f"""
        Bạn đã chọn: **{business_step}** trạng thái: **{business_state}** của loại hình doanh nghiệp: **{business_type}**\n
        Dưới đây là chi tiết thực hiện:\n
        {details_formatted}
        """
        
        # Send the entire message as a single string
        dispatcher.utter_message(text=text.strip())

        return []

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

class ActionListSubIndustries(Action):

    def name(self) -> Text:
        return "action_list_subindustries"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Lấy tên ngành cha từ intent hoặc slot
        industry_name = tracker.get_slot("industry_name")

        # Gọi API để lấy danh sách subindustries
        if not industry_name:
            last_message = tracker.latest_message.get('text')
            activity = get_closest_activity(input_text=last_message, activities=subindustries)

            if not activity:
                dispatcher.utter_message(text=f"Bạn vui loại chọn lĩnh vực kinh doanh trước.")
                return []

            industry_name = activity['activity_name']

        subindustries = get_subindustries(industry_name)

        if not subindustries:
            dispatcher.utter_message(text=f"Không tìm thấy ngành nghề nào thuộc lĩnh vực {industry_name}.")
            return []

        # Tạo danh sách quick-replies
        subindustry_names = [f"- {index+1}. _{subindustry['activity_name']} (**MS: {get_first_level_code(subindustry)}**)_" for index, subindustry in enumerate(subindustries)]
        subindustry_names_formatted = '\n'.join(subindustry_names)
        buttons = [{"title": f"{index+1}",
                    "payload": f"/inform{{\"subindustry_name\": \"{subindustry['activity_name']}\"}}"
                    } for index, subindustry in enumerate(subindustries)
                ]

        text = f"""
        Các ngành nghề thuộc lĩnh vực {industry_name} bao gồm:\n
        {subindustry_names_formatted}\n
        Bạn chọn ngành nghề nào?
        """
        message_json = {
            "type": "quick_replies",
            "content": {
                "title": text,
                "buttons": buttons
            },
        }

        dispatcher.utter_message(json_message=message_json)

        return []
