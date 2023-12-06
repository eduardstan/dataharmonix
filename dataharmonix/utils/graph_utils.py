def create_cytoscape_node(node):
    node_style = 'statistical' if node.operator_config.get('is_statistical', False) else 'normal'
    return {
        'data': {'id': node.id, 'label': node.name},
        'classes': node_style
    }

def create_cytoscape_edge(source_id, target_id):
    return {
        'data': {'source': source_id, 'target': target_id}
    }
