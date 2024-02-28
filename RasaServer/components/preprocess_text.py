import re
from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
import csv

import yaml

# TODO: Correctly register your component with its type
@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER], is_trainable=False
)
class Preprocess(GraphComponent):
    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ):
        # TODO: Implement this
        ...
        
    def train(self, training_data: TrainingData) -> Resource:
        # TODO: Implement this if your component requires training
        return Resource(self.__class__.__name__)

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        # TODO: Implement this if your component augments the training data with
        #       tokens or message features which are used by other components
        #       during training.
        print("Training data before preprocessing:")
        return training_data

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            # Get the text from the message
            text = message.get('text')

            # Remove special characters
            text = re.sub(r'\W', ' ', text)

            # Tokenize the text into words
            words = text.split()

            # Read teencode.txt
            with open('data/teencode.yml', 'r', encoding='utf-8') as file:
                teencode = yaml.load(file, Loader=yaml.FullLoader)

            # Replace teencode words
            for i in range(len(words)):
                if words[i] in teencode:
                    words[i] = teencode[words[i]]

            # Join the words back into a processed text
            processed_text = ' '.join(words)

            # Set the processed text in the message
            message.set('text', processed_text)
        return messages
