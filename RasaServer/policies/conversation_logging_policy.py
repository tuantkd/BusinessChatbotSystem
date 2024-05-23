from __future__ import annotations
from datetime import datetime, timezone
import json
import logging

from rasa.core.policies.policy import Policy, PolicyPrediction
from typing import List, Dict, Text, Any, Type
from rasa.shared.core.domain import Domain
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from actions.api_operations import update_history
from pathlib import Path

logger = logging.getLogger(__name__)

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
            "priority": 1
        }

    @classmethod
    def create(
        cls: Type[ConversationLoggingPolicy],
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> ConversationLoggingPolicy:
        return cls(config, model_storage, resource, execution_context)

    def __init__(
        self, config: Dict[Text, Any], model_storage: ModelStorage, resource: Resource, execution_context: ExecutionContext
    ) -> None:
        self.config = config
        self.model_storage = model_storage
        self.resource = resource
        self.execution_context = execution_context
        self.priority = config.get("priority", 1) 

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
            intent_ranking = tracker.latest_message.parse_data['intent_ranking'] if hasattr(tracker.latest_message.parse_data, 'intent_ranking') else []
            response = tracker.latest_action_name
            timestamp = tracker.events[-1].timestamp

            # Determine next action
            next_action = self.predict_next_action(tracker, domain)
            if not next_action:
                next_action = "default_action"  # Provide a default action if none is predicted

            # Convert timestamp to ISO 8601 format
            if isinstance(timestamp, (int, float)):
                timestamp = datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
            else:
                timestamp = str(timestamp)

             # Proceed with the default action prediction
            probabilities = self._default_predictions(domain)
            prediction = self._prediction(probabilities)

            # Log the predicted action and its confidence
            predicted_action_index = prediction.probabilities.index(max(prediction.probabilities))
            predicted_action = domain.action_names_or_texts[predicted_action_index]
            confidence = max(prediction.probabilities)

            logger.info(f"Predicted action: {predicted_action} with confidence: {confidence}")
            # Prepare data for update
            data = {
                "intent": intent,
                "entities": json.dumps(entities),  # Convert to JSON string
                "user_say": user_say,
                "confidence": confidence,
                "sender_id": sender_id,
                "slot_values": json.dumps(slot_values),  # Convert to JSON string
                "intent_ranking": json.dumps(intent_ranking),  # Convert to JSON string
                "response": response,
                "timestamp": timestamp,
                "next_action": next_action,
                "current_action": predicted_action
            }
            # Update History record
            update_history(history_id, data)

        # Log predictions and confidence of all policies
        all_predictions = []
        for policy_name, policy_prediction in tracker.latest_message.metadata.get('policy_predictions', {}).items():
            all_predictions.append((policy_name, policy_prediction["confidence"]))
            logger.info(f"Policy {policy_name} predicted action {policy_prediction['action']} with confidence {policy_prediction['confidence']}")
            
        # Proceed with the default action prediction
        probabilities = self._default_predictions(domain)
        return self._prediction(probabilities)

    def predict_next_action(self, tracker: DialogueStateTracker, domain: Domain) -> Text:
        # Use the tracker and domain to predict the next action
        # You can customize this logic based on your needs
        probabilities = self._default_predictions(domain)
        max_probability_index = probabilities.index(max(probabilities))
        next_action = domain.action_names_or_texts[max_probability_index]
        return next_action

    def train(
        self,
        training_trackers: List[DialogueStateTracker],
        domain: Domain,
        **kwargs: Any,
    ) -> Resource:
        """Huấn luyện chính sách trên các tracker đã cung cấp."""
        logger.info(f"Training policy with {len(training_trackers)} trackers.")

        with self.model_storage.write_to(self.resource) as path:
            # Save any necessary data to the path
            # Here we are just creating an empty file as a placeholder
            (Path(path) / "empty_model.txt").write_text("This is a placeholder for model data.")

        return self.resource

    def _metadata(self) -> Dict[Text, Any]:
        return {"priority": self.priority}

    def persist(self) -> None:
        pass

    @classmethod
    def load(
        cls: Type[ConversationLoggingPolicy],
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
        **kwargs: Any,
    ) -> ConversationLoggingPolicy:
        return cls(config, model_storage, resource, execution_context)
