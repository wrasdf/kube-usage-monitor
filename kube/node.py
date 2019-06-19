import os
import importlib
from kubernetes import client, config

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "config_manager.py")).load_module()
from config_manager import ConfigManager


class NodeManager:

    def __init__(self):
        ConfigManager()
        self.coreApi = client.CoreV1Api()

    def list_node(self):
        return list(map(lambda x: x.metadata.name, self.coreApi.list_node().items))
