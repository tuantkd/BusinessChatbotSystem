from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.domain import Domain
from rasa.shared.core.events import UserUttered, BotUttered
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from typing import List, Dict, Text, Any
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter
from rasa.core.policies.policy import PolicyPrediction
from typing import Optional
import requests

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.POLICY_WITHOUT_END_TO_END_SUPPORT], is_trainable=True
)
class ConversationLoggingPolicy(GraphComponent):
    def __init__(self, config: Dict[Text, Any]):
        self.config = config

    def predict_action_probabilities(
        self,
        tracker: DialogueStateTracker,
        domain: Domain,
        rule_only_data: Optional[Dict[Text, Any]] = None,
        **kwargs: Any,
    ) -> PolicyPrediction:
        
        last_message = tracker.latest_message
        # call api
        payload = {
            "intent": last_message.intent["name"],
            "session_id": tracker.sender_id,
            "entities": last_message.entities,
            "text": last_message.text,
            "confidence": last_message.intent["confidence"]

        }

        return PolicyPrediction.for_action_name(domain, "action_listen")

    def _metadata(self) -> Dict[Text, Any]:
        return {"lookup": self.lookup}
    

    def train(self, training_data: TrainingData, domain: Domain) -> Resource:
        # This method is called during the training phase
        # You can add any training code here if necessary
        return Resource(self.__class__.__name__)
