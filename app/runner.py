import os
import importlib
import json
import click
from pprint import pprint

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("usage", os.path.join(current_dir, "../kube/usage.py")).load_module()
from usage import UsageManager

class Parser:

    def __init__(self):
        self.usageManager = UsageManager()

    def update_cache(self):
        self.usageManager.cache_outputs()

    # example:
    # self.top_nodes_usages(key='cpu_usage', top=10)
    # support keys:
    #   - cpu_usage
    #   - memory_usage
    def top_nodes_usages(self, **kwargs):
        sort_key = kwargs.get('key', 'cpu_usage')
        top = kwargs.get('top', 5)
        with open('all_nodes_usages.txt') as f:
            data = json.load(f)

        print("========================================================================")
        print("Top {0} node {1} usaged.".format(top, sort_key))
        pprint(sorted(data, key=lambda k: k[sort_key], reverse=True)[:top])
        print()
        print()

    # example:
    # self.top_deploys_usages(key='cpu_request', top=10)
    # support keys:
    #   - cpu_request
    #   - cpu_limit
    #   - memory_request
    #   - memory_limit
    def top_deploys_usages(self, **kwargs):
        sort_key = kwargs.get('key', 'cpu_request')
        top = kwargs.get('top', 10)
        with open('all_deployments_usages.txt') as f:
            data = json.load(f)

        print("========================================================================")
        print("Top {0} deployment resource of {1}.".format(top, sort_key))
        pprint(sorted(data, key=lambda k: k[sort_key], reverse=True)[:top])
        print()
        print()


@click.command()
@click.version_option('0.1')
@click.option('-c', '--updatea_cache', default=False, help='Generate Cluster Usage details to local.')
@click.option('-n', '--node', default='', help='Sortby node <cpu_usage | memory_usage>')
@click.option('-d', '--deployment', default='', help='Sortby deployment <cpu_request | cpu_limit | memory_request | memory_limit> ')
@click.option('-t', '--top', default=10, help='Top of list')

def main(**kwargs):
    """Kubernetes cluster usage monitor"""
    parser = Parser()

    argCache = kwargs.get('updatea_cache')
    argNode = kwargs.get('node')
    argDeploy = kwargs.get('deployment')
    argTop = kwargs.get('top')

    if argCache == 'true':
       print("Please wait for a while .... ")
       parser.update_cache()
       print("Data updated.")

    supportNodeSortList = ['cpu_usage', 'memory_usage']
    supportDeploymentSortList = ['cpu_request', 'cpu_limit', 'memory_request', 'memory_limit']

    if argNode != '' and argNode in supportNodeSortList:
       parser.top_nodes_usages(key=argNode, top=argTop)

    if argDeploy != '' and argDeploy in supportDeploymentSortList:
       parser.top_deploys_usages(key=argDeploy, top=argTop)

if __name__ == '__main__':
    main()
