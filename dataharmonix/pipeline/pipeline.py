import json
from ..operators.operator import Operator
import uuid

class PipelineNode:
    def __init__(self, operator_config, children=None):
        self.id = str(uuid.uuid4())  # Unique identifier
        self.operator_config = json.loads(operator_config)
        self.children = children or []
        self.is_statistical = self.operator_config.get('is_statistical', False)

    def add_child(self, child_node):
        self.children.append(child_node)

    def remove_child(self, child_node):
        self.children = [child for child in self.children if child.id != child_node.id]

    def execute(self, input_data):
        operator = Operator(config_json=json.dumps(self.operator_config))
        output_data = operator.execute(input_data) if not self.is_statistical else None

        child_results = {}
        for child in self.children:
            child_output = child.execute(output_data if not self.is_statistical else input_data)
            child_results[child.id] = child_output

        return output_data if not self.is_statistical else child_results

    
class DataPipeline:
    def __init__(self, root_node=None):
        self.root_node = root_node

    def set_root(self, root_node):
        self.root_node = root_node

    def remove_node(self, node):
        # Implement logic to remove a node and its subtree
        pass

    def run(self, input_data):
        if not self.root_node:
            raise ValueError("Pipeline has no root node.")
        return self.root_node.execute(input_data)