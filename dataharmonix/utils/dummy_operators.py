import numpy as np

def simple_add_function(data, constant=10.0):
    return [x + constant for x in data]

def create_dummy_normal_operator(name, description, input_type="number", output_type="number"):
    """Generates a dummy configuration for a normal operator."""
    return {
        "name": name,
        "description": description,
        "operator_type": "function",
        "callable": "dataharmonix.utils.dummy_operators.simple_add_function",
        "is_statistical": False,
        "input_type": input_type,
        "output_type": output_type,
        "parameters": [
            {
                "name": "constant",
                "type": "float",
                "description": "Constant to add",
                "default": 10.0,
                "required": False
            }
        ],
        "dependencies": []
    }

def simple_mean_function(data):
    return np.mean(data)

def create_dummy_statistical_operator(name, description, input_type="number", output_type="number"):
    """Generates a dummy configuration for a statistical operator."""
    return {
        "name": name,
        "description": description,
        "operator_type": "function",
        "callable": "dataharmonix.utils.dummy_operators.simple_mean_function",
        "is_statistical": True,
        "input_type": input_type,
        "output_type": output_type,
        "parameters": [],
        "dependencies": []
    }
    
def not_so_simple_mean_function(data, constant=1.0):
    return np.mean(data * constant)

def create_dummy_statistical_operator_with_params(name, description, input_type="number", output_type="number"):
    """Generates a dummy configuration for a statistical operator."""
    return {
        "name": name,
        "description": description,
        "operator_type": "function",
        "callable": "dataharmonix.utils.dummy_operators.not_so_simple_mean_function",
        "is_statistical": True,
        "input_type": input_type,
        "output_type": output_type,
        "parameters": [
            {
                "name": "constant",
                "type": "float",
                "description": "Constant to multiply",
                "default": 1.0,
                "required": False
            }
        ],
        "dependencies": []
    }

