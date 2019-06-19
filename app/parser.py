import os
import importlib
import json
import click
from prettytable import PrettyTable

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("usage", os.path.join(current_dir, "../kube/usage.py")).load_module()
from usage import UsageManager

class Parser:

    def __init__(self):
        self.usageManager = UsageManager()
        self.folder = "cache/{0}"
        self.nodes_usages_path = "cache/{0}/all_nodes_usages.txt"
        self.pods_usages_path = "cache/{0}/all_pods_usages.txt"

    def update_cache(self, env):

        cache_folder = self.folder.format(env)
        if not os.path.exists(cache_folder):
            os.makedirs(cache_folder)

        all_nodes_usages = open(self.nodes_usages_path.format(env),"w")
        all_nodes_usages.write(json.dumps(self.usageManager.list_nodes_usage()))
        all_nodes_usages.close()

        all_pods_usages = open(self.pods_usages_path.format(env),"w")
        all_pods_usages.write(json.dumps(self.usageManager.list_pods_usages()))
        all_pods_usages.close()


    # example:
    # self.top_nodes_usages(env='europa-stg', key='cpu_usage', top=10)
    # support keys:
    #   - cpu_usage
    #   - memory_usage
    def top_nodes_usages(self, **kwargs):
        env = kwargs.get('env', 'europa-stg')
        sort_key = kwargs.get('key', 'cpu_usage')
        top = kwargs.get('top', 5)
        with open(self.nodes_usages_path.format(env)) as f:
            data = json.load(f)

        print("========================================================================")
        print("Top {0} node {1} usaged.".format(top, sort_key))
        orderData = sorted(data, key=lambda k: k[sort_key], reverse=True)[:top]
        table = PrettyTable()
        table.field_names = ["Node", "CpuUsage", "MemUsages"]
        for item in orderData:
            table.add_row([item['node'], item['cpu_usage_show'], item['memory_usage_show']])
        print(table)

    # example:
    # self.top_pods_usages(env='europa-stg', key='cpu_request', top=10)
    # support keys:
    #   - cpu_request
    #   - cpu_limit
    #   - memory_request
    #   - memory_limit
    def top_pods_usages(self, **kwargs):
        env = kwargs.get('env', 'europa-stg')
        sort_key = kwargs.get('key', 'cpu_request')
        top = kwargs.get('top', 10)
        with open(self.pods_usages_path.format(env)) as f:
            data = json.load(f)

        print("========================================================================")
        print("Top {0} pod resource of {1}.".format(top, sort_key))
        orderData = sorted(data, key=lambda k: k[sort_key], reverse=True)[:top]
        table = PrettyTable()
        table.field_names = ["Node", "Namespace", "Pod", "CpuRequest", "CpuLimit", "MemRequest", "MemLimit"]
        for item in orderData:
            table.add_row([item['node'], item['namespace'], item['pod'][:30], item['cpu_request_show'], item['cpu_limit_show'], item['memory_request_show'], item['memory_limit_show']])
        print(table)
