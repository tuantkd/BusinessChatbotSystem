from __future__ import annotations

from rasa.core.policies.policy import Policy, PolicyPrediction
from typing import List, Dict, Text, Any, Type
from rasa.shared.core.domain import Domain
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from actions.api_operations import update_history

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.POLICY_WITHOUT_END_TO_END_SUPPORT], is_trainable=True
)
class ConversationLoggingPolicy(Policy):

    @classmethod
    def required_components(cls) -> List[Type[GraphComponent]]:
        return []

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {
            "priority": 2
        }

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(config, model_storage, resource, execution_context)

    def __init__(
        self, config: Dict[Text, Any], model_storage: ModelStorage, resource: Resource, execution_context: ExecutionContext
    ) -> None:
        self.config = config
        self.model_storage = model_storage
        self.resource = resource
        self.execution_context = execution_context

    def predict_action_probabilities(
        self,
        tracker: DialogueStateTracker,
        domain: Domain,
    ) -> PolicyPrediction:
        # Extract metadata from the tracker
        metadata = tracker.latest_message.metadata
        history_id = metadata.get("history_id", None)
        
        if history_id:
            # Get intent, entities, user_say, etc.
            intent = tracker.latest_message.intent.get("name")
            entities = tracker.latest_message.entities
            user_say = tracker.latest_message.text
            confidence = tracker.latest_message.intent.get("confidence")
            sender_id = tracker.sender_id
            slot_values = tracker.current_slot_values()
            intent_ranking = tracker.latest_message.intent_ranking
            response = tracker.latest_action_name
            timestamp = tracker.events[-1].timestamp
            next_action = None

            # Prepare data for update
            data = {
                "intent": intent,
                "entities": str(entities),
                "user_say": user_say,
                "confidence": confidence,
                "sender_id": sender_id,
                "slot_values": str(slot_values),
                "intent_ranking": str(intent_ranking),
                "response": response,
                "timestamp": timestamp,
                "next_action": next_action
            }
            # Update History record
            update_history(history_id, data)

        # Proceed with the default action prediction
        probabilities = self._default_predictions(domain)
        return self._prediction(probabilities)

    def _metadata(self) -> Dict[Text, Any]:
        return {"priority": self.priority}

    def persist(self) -> None:
        pass

    @classmethod
    def load(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
        **kwargs: Any,
    ) -> GraphComponent:
        return cls(config, model_storage, resource, execution_context)
