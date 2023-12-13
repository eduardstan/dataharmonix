import ipywidgets as widgets
from IPython.display import display

class NodeView:
    def __init__(self, node, on_update_callback=None, on_delete_callback=None):
        self.node = node
        self.on_update_callback = on_update_callback
        self.on_delete_callback = on_delete_callback
        self.view = self.create_view()

    def create_view(self):
        # Node info
        name_label = widgets.Label(value=f"Node: {self.node.operator_config['name']} ({self.node.id})")

        # Parameter editing widgets
        parameter_widgets = [self.create_widget_for_parameter(param) for param in self.node.operator_config['parameters']]
        parameters_box = widgets.VBox(parameter_widgets)

        # Update and delete buttons
        buttons = []
        if self.node.operator_config['parameters']:  # Check if there are parameters
            update_button = widgets.Button(description='Update')
            update_button.on_click(self.on_update)
            buttons.append(update_button)

        delete_button = widgets.Button(description='Delete')
        delete_button.on_click(self.on_delete)
        buttons.append(delete_button)

        # Assembling the view with conditional buttons
        return widgets.VBox([name_label, parameters_box] + buttons)

    def create_widget_for_parameter(self, param):
        # Fetch the current value of the parameter or fallback to the default
        current_value = self.node.params.get(param['name'], param.get('default', 0))
        if param['type'] == 'float':
            return widgets.FloatText(value=current_value, description=param['name'])
        elif param['type'] == 'int':
            return widgets.IntText(value=current_value, description=param['name'])
        else:
            return widgets.Text(value=current_value, description=param['name'])

    def on_update(self, b):
        # Collect updated parameter values
        new_params = {widget.description: widget.value for widget in self.view.children[1].children}
        # Update node with new parameters
        self.node.params = new_params
        # Call update callback with a message
        if self.on_update_callback:
            self.on_update_callback(f"Node {self.node.id} updated.")

    def on_delete(self, b):
        # Call delete callback with a message
        if self.on_delete_callback:
            self.on_delete_callback(self.node.id, f"Node {self.node.id} deleted.")

    def render(self):
        return self.view
