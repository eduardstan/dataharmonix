import ipywidgets as widgets

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

    # Event handler methods will be added here
