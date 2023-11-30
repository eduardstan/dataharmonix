from ..operators.operator import Operator

class OperatorRegistry:
    def __init__(self):
        self.operators = {}

    def register(self, operator_json):
        operator = Operator(config_json=operator_json)  # Validation happens here
        self.operators[operator.config['name']] = operator.config

    def get_operator_config(self, name):
        return self.operators.get(name)

operator_registry = OperatorRegistry()