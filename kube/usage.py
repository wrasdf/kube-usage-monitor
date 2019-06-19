import os
import importlib
import re
import json
from pprint import pprint

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("exec", os.path.join(current_dir, "exec.py")).load_module()
importlib.machinery.SourceFileLoader("node", os.path.join(current_dir, "node.py")).load_module()
from exec import EXEC
from node import NodeManager

class UsageManager:
    def __init__(self):
        self.nodeManager = NodeManager()
        self.exec = EXEC()
        self.nodes_usage = []
        self.deployments_usages = []

    def p2f(self, x):
        percent_str = re.sub(r'[\(|\|%)]', '', x)
        if percent_str == "0":
            return 0
        return float(percent_str)/100

    def top_node_bash(self, column_index):
        bash = "kubectl top node | awk '{print $%s}'" % column_index
        return self.exec.exec_sh(bash, print_enable=False).split('\n')

    def list_nodes_usage(self):
        # self.exec.exec_sh("kubectl top nodes")
        nodes = self.top_node_bash('1')
        nodes.remove(nodes[0])

        cpuUsageData = self.top_node_bash('2')
        cpuUsageData.remove(cpuUsageData[0])

        cpuUsages = self.top_node_bash('3')
        cpuUsages.remove(cpuUsages[0])

        memUsageData = self.top_node_bash('4')
        memUsageData.remove(memUsageData[0])

        memUsages = self.top_node_bash('5')
        memUsages.remove(memUsages[0])

        for i in range(len(nodes)):
            usage = {
                'cpu_usage': self.p2f(cpuUsages[i]),
                'cpu_usage_detail': "use: {0} {1}, Total: {2}".format(cpuUsages[i], cpuUsageData[i], '4000m'),
                'memory_usage': self.p2f(memUsages[i]),
                'memory_usage_detail': "use: {0} {1}, Total: {2}".format(memUsages[i], memUsageData[i], '16000Mi'),
                'node': nodes[i]
            }
            self.nodes_usage.append(usage)

        return self.nodes_usage

    def list_deployments_usages(self):
        nodes = self.nodeManager.list_node()
        for node in nodes:
            self.get_deployment_usage(node=node)

        return self.deployments_usages

    def node_describe_bash(self, node, column_index):
        bash = "kubectl describe node %s | grep Namespace -A 20 | grep -ve 'Total' -ve 'Allocated' -ve 'Events' -ve '--' | awk '{print $%s}'" % (node, column_index)
        return self.exec.exec_sh(bash, print_enable=False).split('\n')

    def get_deployment_usage(self, node=""):
        print('Processing node {0}'.format(node))
        # self.exec.exec_sh("kubectl describe node " + node + " | grep Namespace -A 20 | grep -ve Total -ve Allocated -ve Events -ve -- ")

        namespaces = self.node_describe_bash(node, '1')
        namespaces.remove(namespaces[0])

        deployments = self.node_describe_bash(node, '2')
        deployments.remove(deployments[0])

        cpu_requests = self.node_describe_bash(node, '4')
        cpu_requests.remove(cpu_requests[0])

        cpu_limits = self.node_describe_bash(node, '6')
        cpu_limits.remove(cpu_limits[0])

        memory_requests = self.node_describe_bash(node, '8')
        memory_requests.remove(memory_requests[0])

        memory_limits = self.node_describe_bash(node, '10')
        memory_limits.remove(memory_limits[0])

        for i in range(len(memory_limits)):
            usage = {
                'namespace': namespaces[i],
                'deployment': deployments[i],
                'cpu_request': self.p2f(cpu_requests[i]),
                'cpu_limit': self.p2f(cpu_limits[i]),
                'memory_request': self.p2f(memory_requests[i]),
                'memory_limit': self.p2f(memory_limits[i]),
                'node': node
            }
            self.deployments_usages.append(usage)

        print('Done for node {0}'.format(node))

    def cache_outputs(self):
        all_nodes_usages = open("all_nodes_usages.txt","w")
        all_nodes_usages.write(json.dumps(self.list_nodes_usage()))
        all_nodes_usages.close()

        all_deployments_usages = open("all_deployments_usages.txt","w")
        all_deployments_usages.write(json.dumps(self.list_deployments_usages()))
        all_deployments_usages.close()
