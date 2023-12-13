import importlib
import json
from jsonschema import validate, ValidationError
import pkg_resources

class Operator:
    def __init__(self, config_json=None):
        self.config = json.loads(config_json)
        self._validate_config()

    def _validate_config(self):
        schema_path = pkg_resources.resource_filename('dataharmonix', 'operators/schema.json')
        with open(schema_path, 'r') as schema_file:
            schema = json.load(schema_file)
        try:
            # print("Validating config:", self.config)
            validate(instance=self.config, schema=schema)
        except ValidationError as e:
            # print("Validation error caught:", e)
            raise ValueError(f"Invalid operator configuration: {e}")
        # print("Config validation passed.")

    def validate_parameters(self, params):
        for param in self.config['parameters']:
            expected_type = param['type']
            actual_value = params.get(param['name'])
            
            if expected_type == "boolean" and not isinstance(actual_value, bool):
                raise TypeError(f"Parameter {param['name']} should be boolean")
            elif expected_type == "integer" and not isinstance(actual_value, int):
                raise TypeError(f"Parameter {param['name']} should be integer")
            elif expected_type == "float" and not isinstance(actual_value, float):
                raise TypeError(f"Parameter {param['name']} should be float")
            elif expected_type == "string" and not isinstance(actual_value, str):
                raise TypeError(f"Parameter {param['name']} should be string")
            elif expected_type == "list of string" and (not isinstance(actual_value, list) or not all(isinstance(item, str) for item in actual_value)):
                raise TypeError(f"Parameter {param['name']} should be a list of strings")
    
    def execute(self, data, params):
        self.validate_parameters(params)
        if self.config['operator_type'] == 'function':
            return self._execute_function(params, data)
        elif self.config['operator_type'] == 'class':
            return self._execute_class(params, data)

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
