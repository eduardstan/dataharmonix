import ipywidgets as widgets
from IPython.display import display, clear_output
from .node_view import NodeView

class MainView:
    def __init__(self):
        self.pipeline_view = widgets.Output()
        self.controls_view = self.create_controls_view()

    def create_controls_view(self):
        # Buttons and other controls will be added here
        add_node_button = widgets.Button(description="Add Node")
        remove_node_button = widgets.Button(description="Remove Node")
        run_pipeline_button = widgets.Button(description="Run Pipeline")

        # Event handlers for buttons can be added here

        return widgets.VBox([add_node_button, remove_node_button, run_pipeline_button])

    def render(self):
        return widgets.VBox([self.pipeline_view, self.controls_view])

    def add_node_to_view(self, node):
        node_view = NodeView(node)
        self.pipeline_view.clear_output()
        with self.pipeline_view:
            display(node_view.render())

    # Add methods for handling button clicks and interactions

    # Example:
    def on_add_node_button_clicked(self, b):
        # Logic to add a new node
        # For demonstration, let's add a mock node
        mock_node = {
            "name": "Example Operator",
            "parameters": [{"name": "param1", "type": "float", "default": 1.2}]
        }
        self.add_node_to_view(mock_node, is_statistical=False)
