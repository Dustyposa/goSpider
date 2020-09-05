from typing import Text, List, Any

from rasa.nlu.classifiers.classifier import IntentClassifier
from rasa.nlu.training_data import Message


class CustomPipeline(IntentClassifier):

    @classmethod
    def required_packages(cls) -> List[Text]:
        return []

    def process(self, message: Message, **kwargs: Any) -> None:
        message.set(self.__class__.__name__, {
            "topic": {},
            "risk": {},
            "sensitive_words": {},
        }, add_to_output=True)

    @property
    def name(self):
        return self.__class__.__name__


if __name__ == '__main__':
    print(CustomPipeline.__name__)
