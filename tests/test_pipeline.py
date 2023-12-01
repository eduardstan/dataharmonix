import unittest
from dataharmonix.operators.operator import Operator
from dataharmonix.pipeline.pipeline import PipelineNode, DataPipeline
import json

function_config = {
    "name": "ArithmeticAddOperation",
    "description": "Adds a constant to data",
    "operator_type": "function",
    "callable": "dataharmonix.utils.arithmetic_operations.simple_add_function",
    "is_statistical": False,
    "input_type": "number",
    "output_type": "number",
    "parameters": [
        {
            "name": "constant",
            "type": "float",
            "description": "Constant to add",
            "default": 1.0,
            "required": False
        }
    ],
    "dependencies": []
}

statistical_function_config = {
    "name": "ArithmeticAddOperation",
    "description": "Adds a constant to data",
    "operator_type": "function",
    "callable": "dataharmonix.utils.arithmetic_operations.simple_add_function",
    "is_statistical": True,
    "input_type": "number",
    "output_type": "number",
    "parameters": [
        {
            "name": "constant",
            "type": "float",
            "description": "Constant to add",
            "default": 1.0,
            "required": False
        }
    ],
    "dependencies": []
}
        
class TestPipelineNode(unittest.TestCase):

    def test_node_creation(self):
        config = json.dumps({
            "name": "TestNode",
            "operator_type": "function",
            "callable": "some_module.some_function",
            "is_statistical": False
        })
        node = PipelineNode(config, None)
        self.assertIsNotNone(node.id)
        self.assertFalse(node.is_statistical)

    def test_add_remove_child(self):
        
        function_params = {"constant": 2.0}
        
        parent_node = PipelineNode(json.dumps(function_config), function_params)
        child_node = PipelineNode(json.dumps(function_config), function_params)

        parent_node.add_child(child_node)
        self.assertEqual(len(parent_node.children), 1)

        parent_node.remove_child(child_node)
        self.assertEqual(len(parent_node.children), 0)

    # Add more tests for execution, statistical nodes, etc.

class TestDataPipeline(unittest.TestCase):

    def test_pipeline_execution(self):
        
        root_params = {"constant": 10.0}
        child_params = {"constant": -20.0}
        statistical_params = {"constant": 1000.0}
        
        root_node = PipelineNode(json.dumps(function_config), root_params)
        child_node = PipelineNode(json.dumps(function_config), child_params)
        statistical_node = PipelineNode(json.dumps(statistical_function_config), statistical_params)

        root_node.add_child(statistical_node)
        statistical_node.add_child(child_node)
        pipeline = DataPipeline(root_node)

        # Assuming you have a way to mock or provide input data
        input_data = [0,1,2,3]
        results = pipeline.run(input_data)

        expected_output = [-10.0, -9, -8.0, -7.0]
        self.assertEqual(results, expected_output)


if __name__ == '__main__':
    unittest.main()
