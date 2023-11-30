import itertools
from utils.operator_registry import OperatorRegistry
from operators.operator_factory import create_operator

class PipelineNode:
    _id_counter = itertools.count()

    def __init__(self, operator, children=None, is_statistics_node=False):
        self.id = next(self._id_counter)
        self.operator = operator
        self.children = children if children else []
        self.is_statistics_node = is_statistics_node
        self.statistics = {}
        
class Pipeline:
    def __init__(self, registry: OperatorRegistry):
        self.registry = registry
        self.root = None

    def add_operator(self, parent_id, operator_id, config_id, custom_params=None):
        operator_config = self.registry.get_operator_config(config_id)
        
        # Validate custom_params against the operator's schema
        # and merge with default parameters from the operator_config
        
        new_operator = create_operator(operator_config, custom_params)
        new_node = PipelineNode(new_operator)

        if parent_id is None:
            if self.root is not None:
                raise ValueError("Root already exists. Can't add another root operator.")
            self.root = new_node
        else:
            parent_node = self.find_node(self.root, parent_id)
            if parent_node is None:
                raise ValueError(f"Parent operator {parent_id} not found.")
            parent_node.children.append(new_node)

        return operator_id
      
    def add_statistics_node(self, parent_id, stats_operator_config_id, stats_params=None):
        stats_operator = create_operator(self.registry.get_config(stats_operator_config_id), stats_params)
        stats_node = PipelineNode(stats_operator, is_statistics_node=True)
        parent_node = self.find_node(self.root, parent_id)
        if parent_node is None:
            raise ValueError(f"Parent operator {parent_id} not found.")
        parent_node.children.append(stats_node)
        return stats_node.id

    def find_node(self, current_node, operator_id):
        if current_node.operator.id == operator_id:
            return current_node
        for child in current_node.children:
            result = self.find_node(child, operator_id)
            if result is not None:
                return result
        return None

    def collect_statistics(data):
        pass
    
    def execute(self, node=None, data=None):
        if node is None:
            node = self.root
        if node is None:
            raise ValueError("Pipeline is empty. Add operators before executing.")

        output_data = node.operator.execute(data)
        if node.is_statistics_node:
            node.statistics = collect_statistics(output_data)  # Implement collect_statistics

        for child in node.children:
            self.execute(node=child, data=output_data)

        return output_data

    def remove_operator(self, operator_id):
        # Implement logic to remove an operator (node) from the pipeline
        # This might involve finding the node, detaching it from its parent, 
        # and reattaching its children to the parent or another node as needed

    # Additional methods like update_operator, get_statistics, etc., can be added here.