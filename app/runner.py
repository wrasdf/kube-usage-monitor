import os
import importlib
import json
import click
from prettytable import PrettyTable

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("parser", os.path.join(current_dir, "parser.py")).load_module()
from parser import Parser

@click.command()
@click.version_option('0.1')
@click.option('-e', '--env', default='europa-stg', help='Support Clusters')
@click.option('-c', '--updatea_cache', default=False, help='Generate Cluster Usage details to local.')
@click.option('-n', '--node', default='', help='Sortby node <cpu_usage | memory_usage | cpu_request | cpu_request | memory_request | memory_limit>')
@click.option('-p', '--pod', default='', help='Sortby pod <cpu_request | cpu_limit | memory_request | memory_limit> ')
@click.option('-t', '--top', default=20, help='Tops of usage list')

def main(**kwargs):
    """Kubernetes cluster usage monitor"""

    parser = Parser()

    argEnv = kwargs.get('env')
    argCache = kwargs.get('updatea_cache')
    argNode = kwargs.get('node')
    argDeploy = kwargs.get('pod')
    argTop = kwargs.get('top')

    if argCache == 'true':
       parser.update_cache(argEnv)

    supportNodesSortList = ['cpu_usage', 'memory_usage', 'cpu_request', 'cpu_limit', 'memory_request', 'memory_limit']
    if argNode != '' and argNode in supportNodesSortList:
       parser.top_nodes_usages(env=argEnv, key=argNode, top=argTop)

    supportPodsSortList = ['cpu_request', 'cpu_limit', 'memory_request', 'memory_limit']
    if argDeploy != '' and argDeploy in supportPodsSortList:
       parser.top_pods_usages(env=argEnv, key=argDeploy, top=argTop)

if __name__ == '__main__':
    main()
