import ipycytoscape
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
        self.operator_category = self.operator_config["operator_category"]

    # Add a node
    # TODO: check if the input node already exists in the pipeline
    def add_node(self, node):
        if node.operator_category == 'statistical':
            self.statistical_children.append(node)
        else:
            self.children.append(node)
           
    # Remove a node
    def remove_node(self, node_id):
        assert self.root_node is not None, "The pipeline is empty."

        def recursive_remove(current_node, target_id):
            for child in current_node.children + current_node.statistical_children:
                if child.id == target_id:
                    if child.operator_category == 'statistical':
                        current_node.statistical_children.remove(child)
                    else:
                        current_node.children.remove(child)
                    return True
                if recursive_remove(child, target_id):
                    return True
            return False

        if self.root_node.id == node_id:
            self.root_node = None
        else:
            removed = recursive_remove(self.root_node, node_id)
            assert removed, f"Node with ID {node_id} not found in the pipeline."


    def execute(self, input_data):
        operator = Operator(config_json=json.dumps(self.operator_config))
        node_output = operator.execute(input_data, self.params)

        # Execute statistical children without altering the node_output
        for stat_child in self.statistical_children:
            stat_child.execute(node_output)  # Execute but do not use its output for main flow

        # Store the output to pass to the main children
        final_output = node_output if not self.operator_category == 'statistical' else input_data
        
        # If there are main children, process them and return their output
        if self.children:
            for child in self.children:
                final_output = child.execute(final_output)  # Update node_output with main child node's output
        
        return final_output


    
class DataPipeline:
    def __init__(self, root_node=None):
        self.root_node = root_node

    def set_root(self, root_node):
        self.root_node = root_node

    def add_node(self, parent_node_id, new_node):
        assert self.root_node is not None, "The pipeline is empty."
        assert new_node is not None, "The new node to add cannot be None."

        # print("Before addition:", self.get_current_state())
        
        # Helper function to recursively find and add node
        def recursive_add(current_node, target_id, node_to_add):
            if current_node.id == target_id:
                # If the new node is statistical, ensure the parent is not statistical
                assert not (node_to_add.operator_category == 'statistical' and current_node.operator_category == 'statistical'), \
                    "Statistical nodes cannot be children of other statistical nodes."
                # Check if node already exists
                for child in current_node.children:
                    assert child.id != node_to_add.id, "Node with this ID already exists."

                # Add the new node
                current_node.add_node(node_to_add)
                return True
            for child in current_node.children:
                if recursive_add(child, target_id, node_to_add):
                    return True
            return False

        # Start recursive addition process
        added = recursive_add(self.root_node, parent_node_id, new_node)
        assert added, f"Parent node with ID {parent_node_id} not found in the pipeline."
        
        # print("After addition:", self.get_current_state())
    
    def remove_node(self, node_id):
        assert self.root_node is not None, "The pipeline is empty."

        def recursive_remove(current_node, target_id):
            # Check children and statistical children
            for child_list in [current_node.children, current_node.statistical_children]:
                for child in child_list:
                    if child.id == target_id:
                        # Recursively remove all children of the target node
                        for subchild in child.children + child.statistical_children:
                            recursive_remove(child, subchild.id)
                        # Remove the target node
                        child_list.remove(child)
                        return True
                    elif recursive_remove(child, target_id):
                        return True
            return False

        if self.root_node.id == node_id:
            self.root_node = None
        else:
            removed = recursive_remove(self.root_node, node_id)
            assert removed, f"Node with ID {node_id} not found in the pipeline."
        
        # print("After deletion:", self.get_current_state())


    def run(self, input_data):
        if not self.root_node:
            raise ValueError("Pipeline has no root node.")
        return self.root_node.execute(input_data)
    
    def get_current_state(self):
        # Return a representation of the current pipeline state
        # This should include nodes and their connections
        return {
            'nodes': self.get_nodes(),
            'edges': self.get_edges()
        }

    def collect_nodes_and_edges(self, current_node, nodes, edges, processed_nodes=None):
        if processed_nodes is None:
            processed_nodes = set()

        if current_node.id in processed_nodes:
            return  # Skip processing if this node has already been processed

        processed_nodes.add(current_node.id)

        # Create a node for ipycytoscape
        node_data = {
            'id': current_node.id,
            'label': current_node.operator_config.get('name', 'Unknown')
        }
        # node_classes = 'statistical' if current_node.is_statistical else 'normal'
        nodes.append(ipycytoscape.Node(data=node_data, classes=current_node.operator_category))
        # nodes.append(current_node)

        # Recursively traverse child nodes
        for child in current_node.children:
            edge_data = {'source': current_node.id, 'target': child.id}
            edges.append(ipycytoscape.Edge(data=edge_data, classes='operator-edge'))
            self.collect_nodes_and_edges(child, nodes, edges, processed_nodes)

        # Recursively traverse statistical child nodes
        for stat_child in current_node.statistical_children:
            edge_data = {'source': current_node.id, 'target': stat_child.id}
            edges.append(ipycytoscape.Edge(data=edge_data, classes='statistical-edge'))
            self.collect_nodes_and_edges(stat_child, nodes, edges, processed_nodes)

    def get_nodes(self):
        nodes = []
        if self.root_node:
            self.collect_nodes_and_edges(self.root_node, nodes, [])
        return nodes
    
    def get_nodes_with_id(self):
        nodes = []
        if self.root_node:
            self.collect_pipeline_nodes(self.root_node, nodes)
        return nodes

    def get_edges(self):
        edges = []
        if self.root_node:
            self.collect_nodes_and_edges(self.root_node, [], edges)
        return edges
    
    def collect_pipeline_nodes(self, current_node, nodes, processed_nodes=None):
        if processed_nodes is None:
            processed_nodes = set()

        if current_node.id in processed_nodes:
            return

        processed_nodes.add(current_node.id)
        nodes.append(current_node)

        for child in current_node.children:
            self.collect_pipeline_nodes(child, nodes, processed_nodes)

        for stat_child in current_node.statistical_children:
            self.collect_pipeline_nodes(stat_child, nodes, processed_nodes)