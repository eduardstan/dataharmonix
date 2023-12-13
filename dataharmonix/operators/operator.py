import importlib
import json
from jsonschema import validate, ValidationError
import pkg_resources
import os

class Operator:
    def __init__(self, config_json=None, params=None):
        self.config = json.loads(config_json)
        self._validate_config()
        self.data_loader = self.config['operator_category'] == 'loader'
        # Validate parameters using defaults during initialization
        self.validate_parameters(params, use_default=True)

    def _validate_config(self):
        schema_path = pkg_resources.resource_filename('dataharmonix', 'operators/schema.json')
        with open(schema_path, 'r') as schema_file:
            schema = json.load(schema_file)
        try:
            print("Validating config:", self.config)
            validate(instance=self.config, schema=schema)
            print("Config validation passed.")
        except ValidationError as e:
            print("Validation error caught:", e)
            print("Error details:", e.message)
            print("Failed schema part:", e.schema)
            print("Failed data part:", e.instance)
            raise ValueError(f"Invalid operator configuration: {e}")

    def validate_parameters(self, params, use_default=False):
        for param in self.config['parameters']:
            expected_type = param['type']
            actual_value = params.get(param['name']) if params else param.get('default') if use_default else None
                        
            if expected_type == "input":
            # Assuming 'input' type refers to a file path
                if not isinstance(actual_value, str) or not os.path.isfile(actual_value):
                    raise ValueError(f"Parameter {param['name']} should be a valid file path")
            elif expected_type == "boolean" and not isinstance(actual_value, bool):
                raise ValueError(f"Parameter {param['name']} should be boolean")
            elif expected_type == "integer":
                if not (isinstance(actual_value, int) or (isinstance(actual_value, str) and actual_value.isdigit())):
                    raise ValueError(f"Parameter {param['name']} should be an integer")
            elif expected_type == "float" and not isinstance(actual_value, float):
                raise ValueError(f"Parameter {param['name']} should be float")
            elif expected_type == "string" and not isinstance(actual_value, str):
                raise ValueError(f"Parameter {param['name']} should be string")
            elif expected_type == "list of string" and (not isinstance(actual_value, list) or not all(isinstance(item, str) for item in actual_value)):
                raise ValueError(f"Parameter {param['name']} should be a list of strings")
    
    def execute(self, data=None, params=None):
        self.validate_parameters(params)
        
        # For data loader operators, the data is loaded within the operator
        if self.data_loader:
            return self._execute_loader(params)
        
        # For other operators, they can have a callable function or class (with methods)
        if self.config['operator_type'] == 'function':
            return self._execute_function(params, data)
        elif self.config['operator_type'] == 'class':
            return self._execute_class(params, data)
        
    def _execute_loader(self, params):
        # Implementation for data loader operators
        module_name, function_name = self.config['callable'].rsplit('.', 1)
        module = importlib.import_module(module_name)
        loader_func = getattr(module, function_name)
        return loader_func(**params)

    def _execute_function(self, params, data):
        module_name, function_name = self.config['callable'].rsplit('.', 1)
        module = importlib.import_module(module_name)
        func = getattr(module, function_name)
        return func(data, **params)

    def _execute_class(self, params, data):
        class_name = self.config['callable']
        module_name, class_name = class_name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
        instance = cls(**params)
        
        for method in self.config.get('methods', []):
            if hasattr(instance, method):
                data = getattr(instance, method)(data)
            else:
                raise AttributeError(f"Method {method} not found in class {class_name}")

        return data
