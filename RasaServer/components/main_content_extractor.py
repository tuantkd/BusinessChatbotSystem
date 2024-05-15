import re
from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

# TODO: Correctly register your component with its type
@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_PROCESSOR], is_trainable=False
)
class MainContentExtractor(GraphComponent):
    def __init__(self, config: Dict[Text, Any]):
        self.config = config

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> "MainContentExtractor":
        return cls(config)

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            text = message.get('text')

            # TODO: Implement the main content extraction logic here
            # For now, we just replace the original text with the main content
            # This is where you'd add NLP techniques to extract the main content
            main_content = self.extract_main_content(text)

            # Set the extracted main content in the message
            message.set('text', main_content)
        return messages

    def extract_main_content(self, text: Text) -> Text:
        # Dummy implementation for content extraction
        # You can replace this with your actual content extraction logic
        # For now, we'll just return the text without stop words
        stop_words = {'tôi', 'muốn', 'cần', 'xin', 'làm ơn', 'vui lòng', 'chỉ'}
        words = text.split()
        main_content_words = [word for word in words if word not in stop_words]
        return ' '.join(main_content_words)
