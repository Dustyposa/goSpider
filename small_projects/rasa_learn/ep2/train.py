from pathlib import Path

from rasa import train as rasa_train
from rasa.constants import DEFAULT_MODELS_PATH, DEFAULT_DOMAIN_PATH, DEFAULT_CONFIG_PATH, DEFAULT_DATA_PATH
from rasa.core.trackers import DialogueStateTracker
from rasa.nlu.registry import component_classes, registered_components

from small_projects.rasa_learn.ep2.classification import CustomPipeline

component_classes.append(CustomPipeline)
registered_components[CustomPipeline.name] = CustomPipeline


def get_project_path() -> Path:
    tmp_path = Path(".").absolute()
    while tmp_path.name != "ep2":
        tmp_path = tmp_path.parent
    return tmp_path


PROJECT_PATH = get_project_path()


def train_gj_ai():
    """训练所有模块"""
    project_path = PROJECT_PATH
    print(str((project_path / DEFAULT_DOMAIN_PATH)))
    return rasa_train(
        domain=str((project_path / DEFAULT_DOMAIN_PATH)),
        config=str((project_path / DEFAULT_CONFIG_PATH)),
        training_files=str((project_path / DEFAULT_DATA_PATH)),
        output=str(project_path / DEFAULT_MODELS_PATH),
    )


if __name__ == '__main__':
    train_gj_ai()
    DialogueStateTracker
