import json
from ..operators.operator import Operator
import uuid

class PipelineNode:
    def __init__(self, operator_config_json, params=None, children=None, statistical_children=None):
        self.id = str(uuid.uuid4())  # Unique identifier
        self.operator_config = json.loads(operator_config_json)
        self.params = params or {}
        self.children = children or []  # Main pipeline nodes
        self.statistical_children = statistical_children or []  # Statistical analysis nodes
        self.is_statistical = self.operator_config.get('is_statistical', False)

    def add_child(self, child_node):
        if child_node.is_statistical:
            self.statistical_children.append(child_node)
        else:
            self.children.append(child_node)
            
    def remove_child(self, child_node):
        self.children = [child for child in self.children if child.id != child_node.id]

    def execute(self, input_data):
        print(f"\nEntering node: {self.operator_config['name']} (ID: {self.id})")
        print(f"Input data: {input_data}")

        operator = Operator(config_json=json.dumps(self.operator_config))
        node_output = operator.execute(input_data, self.params)
        print(f"Output after main operator in {self.operator_config['name']}: {node_output}")

        # Execute statistical children without altering the node_output
        for stat_child in self.statistical_children:
            print(f"\nExecuting statistical child: {stat_child.operator_config['name']} (ID: {stat_child.id})")
            stat_child.execute(node_output)  # Execute but do not use its output for main flow

        # Store the output to pass to the main children
        final_output = node_output if not self.is_statistical else input_data
        
        # If there are main children, process them and return their output
        if self.children:
            for child in self.children:
                print(f"\nPassing data to main child node: {child.operator_config['name']} (ID: {child.id})")
                final_output = child.execute(final_output)  # Update node_output with main child node's output
                print(f"Output after processing main child node: {final_output}")
        
        print(f"\nNode {self.operator_config['name']} (ID: {self.id}) returning: {final_output}")
        return final_output


    
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