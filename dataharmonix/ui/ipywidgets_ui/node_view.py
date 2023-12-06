import ipywidgets as widgets

class NodeView:
    def __init__(self, node):
        self.node = node
        self.view = self.create_view()

    def create_view(self):
        # Access properties of PipelineNode object
        name_label = widgets.Label(value=f"Node: {self.node.operator_config['name']} ({self.node.id})")
        parameters_view = self.create_parameters_view(self.node.operator_config['parameters'])

        if self.node.is_statistical:
            return widgets.VBox([name_label, parameters_view], layout=widgets.Layout(border='1px solid blue'))
        else:
            return widgets.VBox([name_label, parameters_view], layout=widgets.Layout(border='1px solid black'))


    def create_parameters_view(self, parameters):
        # Create widgets for node parameters
        param_widgets = []
        for param in parameters:
            label = widgets.Label(value=param['name'])
            input_widget = self.create_input_widget(param)
            param_widgets.append(widgets.HBox([label, input_widget]))
        return widgets.VBox(param_widgets)

    def create_input_widget(self, param):
        # Create appropriate widget based on parameter type
        if param['type'] == 'float':
            return widgets.FloatText(value=param.get('default', 0.0))
        # Add more cases for different parameter types
        return widgets.Text()  # Fallback widget

    def render(self):
        return self.view
