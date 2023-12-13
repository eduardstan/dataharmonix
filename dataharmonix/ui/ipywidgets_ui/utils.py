import ipycytoscape

def create_cytoscape_graph(pipeline_state):
    graph = ipycytoscape.CytoscapeWidget()
    graph.graph.add_nodes(pipeline_state['nodes'])
    graph.graph.add_edges(pipeline_state['edges'])

    # Define custom styles
    # Define custom styles for nodes and edges
    graph.set_style([
        # Node styles
        {
            'selector': '.statistical', 
            'style': {
                'shape': 'triangle', 
                'background-color': 'red'
            }
        },
        {
            'selector': '.non-statistical', 
            'style': {
                'shape': 'ellipse', 
                'background-color': 'blue'
            }
        },
        # Edge styles
        {
            'selector': '.operator-edge', 
            'style': {
                'line-color': 'green', 
                'curve-style': 'bezier', 
                'target-arrow-shape': 'triangle'
            }
        },
        {
            'selector': '.statistical-edge', 
            'style': {
                'line-color': 'orange', 
                'curve-style': 'unbundled-bezier', 
                'target-arrow-shape': 'none'
            }
        }
    ])

    return graph