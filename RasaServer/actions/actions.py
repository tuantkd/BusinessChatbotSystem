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
        
        business_types = get_business_types()
        formatted_business_types = ', '.join(f"{business_type[1]}" for business_type in business_types)
        
        dispatcher.utter_message(
            template="utter_business_types",
            entity_business_type=formatted_business_types
        )

        return []
