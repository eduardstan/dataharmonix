import ipycytoscape
from dataharmonix.utils.graph_utils import create_cytoscape_node, create_cytoscape_edge

class MainView:
    def __init__(self, data_pipeline):
        self.data_pipeline = data_pipeline
        self.graph_widget = ipycytoscape.CytoscapeWidget()
        self.update_graph_view()

    def update_graph_view(self):
        pipeline_state = self.data_pipeline.get_current_state()
        self.graph_widget.graph.clear()
        for node in pipeline_state['nodes']:
            print(node.classes, node.data)
        self.graph_widget.graph.add_nodes(pipeline_state['nodes'])
        self.graph_widget.graph.add_edges(pipeline_state['edges'])
        self.apply_graph_styles()


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
                    'shape': 'triangle'  # Change this to the desired shape
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
        return self.graph_widget
