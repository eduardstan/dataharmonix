import json
import ipywidgets as widgets
from IPython.display import display
import ipycytoscape
from dataharmonix.utils.graph_utils import create_cytoscape_node, create_cytoscape_edge
from dataharmonix.pipeline.pipeline import PipelineNode

class MainView:
    def __init__(self, data_pipeline, operators):
        self.data_pipeline = data_pipeline
        self.operators = operators
        
        # Filter out statistical operators
        normal_operators = {name: op for name, op in operators.items() if not op['is_statistical']}
        self.operator_dropdown = widgets.Dropdown(options=[op['name'] for op in normal_operators.values()], description='Operator:')
        
        # Filter out non-statistical operators
        statistical_operators = {name: op for name, op in operators.items() if op['is_statistical']}
        self.stat_operator_dropdown = widgets.Dropdown(options=[op['name'] for op in statistical_operators.values()], description='Statistical Operator:')
        
        # Dropdowns for normal and statistical nodes
        self.parent_node_dropdown_normal = widgets.Dropdown(options=self.get_normal_node_options(), description='Parent Node (Normal):')
        self.parent_node_dropdown_statistical = widgets.Dropdown(options=self.get_normal_node_options(), description='Parent Node (Statistical):')
        
        self.parameter_widgets = widgets.VBox([])
        self.operator_dropdown.observe(self.on_operator_change, names='value')
        
        self.stat_parameter_widgets = widgets.VBox([])  # Container for statistical node parameters
        self.stat_operator_dropdown.observe(self.on_stat_operator_change, names='value')
                
        # Initialize parameter widgets for the default (first) operator
        if self.operators:
            first_operator = next(iter(self.operators.values()))
            self.parameter_widgets.children = [self.create_widget_for_parameter(p) for p in first_operator['parameters']]
        
        self.add_node_button = widgets.Button(description='Add Node')
        self.add_node_button.on_click(self.add_node)
        
        self.add_stat_node_button = widgets.Button(description='Add Statistical Node')
        self.add_stat_node_button.on_click(self.add_statistical_node)
        
        self.node_form = widgets.VBox([self.operator_dropdown, self.parent_node_dropdown_normal, self.parameter_widgets, self.add_node_button])
        self.stat_node_form = widgets.VBox([self.stat_operator_dropdown, self.parent_node_dropdown_statistical, self.add_stat_node_button])
        
        self.graph_widget = ipycytoscape.CytoscapeWidget()
        self.update_graph_view()
        # Attach event listener to nodes
        self.graph_widget.on('node', 'click', self.on_node_click)

        # Similarly, create other UI components for modify and delete

        self.output_widget = widgets.Output()
        
    def on_operator_change(self, change):
        operator_name = change['new']
        operator = self.operators[operator_name]
        if operator['parameters']:
            param_widgets = [self.create_widget_for_parameter(p) for p in operator['parameters']]
            self.parameter_widgets = widgets.VBox(param_widgets)
        else:
            self.parameter_widgets = widgets.VBox([])

        # Update the node form to include the new parameter_widgets
        self.node_form.children = [self.operator_dropdown, self.parent_node_dropdown_normal, self.parameter_widgets, self.add_node_button]

        
    def on_stat_operator_change(self, change):
        stat_operator_name = change['new']
        stat_operator = self.operators[stat_operator_name]
        if stat_operator['parameters']:
            param_widgets = [self.create_widget_for_parameter(p) for p in stat_operator['parameters']]
            self.stat_parameter_widgets = widgets.VBox(param_widgets)
        else:
            self.stat_parameter_widgets = widgets.VBox([])

        # Rebuild the stat node form with the new stat_parameter_widgets
        self.stat_node_form.children = [self.stat_operator_dropdown, self.parent_node_dropdown_statistical, self.stat_parameter_widgets, self.add_stat_node_button]
        
    def create_widget_for_parameter(self, param):
        if param['type'] == 'float':
            return widgets.FloatText(value=param.get('default', 0.0), description=param['name'])
        elif param['type'] == 'int':
            return widgets.IntText(value=param.get('default', 0), description=param['name'])
        # Add more types as needed
        else:
            return widgets.Text(value=param.get('default', ''), description=param['name'])
        
    def add_node(self, b):
        selected_operator_json = json.dumps(self.operators[self.operator_dropdown.value])
        parameters = {widget.description: widget.value for widget in self.parameter_widgets.children}
        new_node = PipelineNode(selected_operator_json, params=parameters)

        parent_node_id = self.parent_node_dropdown_normal.value
        if parent_node_id is None or parent_node_id == 'Root':
            self.data_pipeline.set_root(new_node)
        else:
             # Find the parent node by its ID
            parent_node = self.find_node_by_id(parent_node_id)
            assert parent_node is not None, "Parent node not found."
            self.data_pipeline.add_node(parent_node.id, new_node)
        
        self.update_graph_view()
        self.update_dropdowns()
        
    def add_statistical_node(self, b):
        selected_stat_operator_json = json.dumps(self.operators[self.stat_operator_dropdown.value])
        stat_parameters = {widget.description: widget.value for widget in self.stat_parameter_widgets.children}
        new_stat_node = PipelineNode(selected_stat_operator_json, params=stat_parameters)

        parent_node_id = self.parent_node_dropdown_statistical.value
        if parent_node_id and parent_node_id != 'Root':
            parent_node = self.find_node_by_id(parent_node_id)
            assert parent_node is not None, "Parent node not found."
            parent_node.add_node(new_stat_node)
        
        self.update_graph_view()
        self.update_dropdowns()

    def update_graph_view(self):
        pipeline_state = self.data_pipeline.get_current_state()
        self.graph_widget.graph.clear()
        self.graph_widget.graph.add_nodes(pipeline_state['nodes'])
        self.graph_widget.graph.add_edges(pipeline_state['edges'])
        self.apply_graph_styles()
        
    def update_dropdowns(self):
        normal_node_options = self.get_normal_node_options()
        self.parent_node_dropdown_normal.options = normal_node_options
        self.parent_node_dropdown_statistical.options = normal_node_options

    def get_normal_node_options(self):
        return [('Root', None)] + [(node.id, node.id) for node in self.data_pipeline.get_nodes_with_id() if not node.is_statistical]

    def on_node_click(self, event):
        # Extract node ID from the event
        node_id = event['data']['id']
        # Find the corresponding node in the data pipeline
        node = self.find_node_by_id(node_id)
        if node:
            # Extract parameters of the node
            params = node.params
            # Update the output widget with the node's parameters
            with self.output_widget:
                self.output_widget.clear_output()
                display(f"Parameters for node {node.operator_config['name']} ({node_id}): {params}")

    def find_node_by_id(self, node_id, current_node=None):
        if current_node is None:
            current_node = self.data_pipeline.root_node
        
        if current_node.id == node_id:
            return current_node

        for child in current_node.children + current_node.statistical_children:
            result = self.find_node_by_id(node_id, child)
            if result:
                return result

    def get_graph_elements(self):
        nodes = [create_cytoscape_node(node) for node in self.data_pipeline.get_nodes()]
        edges = [create_cytoscape_edge(edge) for edge in self.data_pipeline.get_edges()]
        return nodes, edges

    def apply_graph_styles(self):
        self.graph_widget.set_style([
            # Style for normal nodes
            {
                'selector': 'node.normal',
                'style': {
                    'background-color': 'blue',
                    'shape': 'ellipse'  # Change this to the desired shape
                }
            },
            # Style for statistical nodes
            {
                'selector': 'node.statistical',
                'style': {
                    'background-color': 'green',
                    'shape': 'rectangle'  # Change this to the desired shape
                }
            },
            # Style for operator->operator edge
            {
                'selector': 'edge.operator-edge', 
                'style': {
                    'line-color': 'black', 
                    'curve-style': 
                        'bezier', 
                        'target-arrow-shape': 'triangle'
                }
            },
            # Style for operator->statistical edge
            {
                'selector': 'edge.statistical-edge', 
                'style': {
                    'line-color': 'red', 
                    'curve-style': 'unbundled-bezier', 
                    'target-arrow-shape': 'none'
                }
            }
        ])

    def render(self):
        # Layout the graph and UI components
        ui_components = widgets.VBox([self.node_form, self.stat_node_form])
        return widgets.VBox([self.graph_widget, ui_components, self.output_widget])
