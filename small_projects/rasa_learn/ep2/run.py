# -*- coding:utf-8 -*-
import rasa
from rasa.cli.shell import shell
from rasa.constants import DEFAULT_DOMAIN_PATH, DEFAULT_ENDPOINTS_PATH, DEFAULT_MODELS_PATH
from rasa.core.processor import MessageProcessor
from rasa.core.tracker_store import TrackerStore
from rasa.core.trackers import DialogueStateTracker
from rasa.nlu.registry import component_classes, registered_components

from small_projects.rasa_learn.ep2.train import PROJECT_PATH, CustomPipeline

# component_classes.append(CustomPipeline)
# registered_components[CustomPipeline.name] = CustomPipeline

# class O:
#     model = "/Users/dustyposa/Documents/code/github/goSpider/small_projects/rasa_learn/ep2/models"
#     endpoints = "/Users/dustyposa/Documents/code/github/goSpider/small_projects/rasa_learn/ep2/endpoints.yml"
#     credentials = None
#     enable_api = False
#
#
# shell(O())
from rasa.core.channels import RestInput

# rasa.run(model="/Users/dustyposa/Documents/code/github/goSpider/small_projects/rasa_learn/ep2/models",
#          endpoints="/Users/dustyposa/Documents/code/github/goSpider/small_projects/rasa_learn/ep2/endpoints.yml")
rasa.run(model=str((PROJECT_PATH / DEFAULT_MODELS_PATH)),
         endpoints=str((PROJECT_PATH / DEFAULT_ENDPOINTS_PATH)),
         credentials="./credentials.yml"
         )
from rasa.nlu.registry import Any

