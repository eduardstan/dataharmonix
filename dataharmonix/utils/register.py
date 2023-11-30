from .operator_registry import operator_registry

def register_operator(operator_json):
    operator_registry.register(operator_json)