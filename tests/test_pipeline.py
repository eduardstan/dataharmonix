import unittest
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
    "name": "StatisticalOperation",
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
        statistical_params = {"constant": 1000.0}
        
        root_node = PipelineNode(json.dumps(function_config), function_params)
        child_node = PipelineNode(json.dumps(function_config), function_params)
        statistical_node =PipelineNode(json.dumps(statistical_function_config), statistical_params)

        root_node.add_node(statistical_node)
        root_node.add_node(statistical_node)
        root_node.add_node(child_node)
        self.assertEqual(len(root_node.statistical_children), 2)
        self.assertEqual(len(root_node.children), 1)

        root_node.remove_node(child_node.id)
        self.assertEqual(len(root_node.children), 0)


class TestDataPipeline(unittest.TestCase):

    def test_pipeline_execution(self):
        
        root_params = {"constant": 10.0}
        child_params = {"constant": -20.0}
        statistical_params = {"constant": 1000.0}
        
        root_node = PipelineNode(json.dumps(function_config), root_params)
        child_node = PipelineNode(json.dumps(function_config), child_params)
        statistical_node = PipelineNode(json.dumps(statistical_function_config), statistical_params)

        root_node.add_node(statistical_node)
        root_node.add_node(child_node)
        pipeline = DataPipeline(root_node)

        # Perhaps mocking would be ideal here
        input_data = [0,1,2,3]
        results = pipeline.run(input_data)

        expected_output = [-10.0, -9, -8.0, -7.0]
        self.assertEqual(results, expected_output)
        
    # Setup a basic pipeline structure for testing
    def setUp(self):
        self.root_node = PipelineNode(json.dumps(function_config), {"constant": 5.0})
        self.pipeline = DataPipeline(self.root_node)
        self.child_node = PipelineNode(json.dumps(function_config), {"constant": 10.0})
        self.statistical_node = PipelineNode(json.dumps(statistical_function_config), {"constant": 15.0})

    def test_add_node_successfully(self):
        self.pipeline.add_node(self.root_node.id, self.child_node)
        self.assertIn(self.child_node, self.root_node.children)

    def test_add_existing_node(self):
        self.pipeline.add_node(self.root_node.id, self.child_node)
        with self.assertRaises(AssertionError):
            self.pipeline.add_node(self.root_node.id, self.child_node)

    def test_add_node_to_nonexistent_parent(self):
        with self.assertRaises(AssertionError):
            self.pipeline.add_node("nonexistent_id", self.child_node)

    def test_add_statistical_node_under_statistical_node(self):
        self.pipeline.add_node(self.root_node.id, self.statistical_node)
        with self.assertRaises(AssertionError):
            self.pipeline.add_node(self.statistical_node.id, PipelineNode(json.dumps(statistical_function_config), {"constant": 20.0}))

    def test_remove_node_successfully(self):
        self.pipeline.add_node(self.root_node.id, self.child_node)
        self.pipeline.remove_node(self.child_node.id)
        self.assertNotIn(self.child_node, self.root_node.children)

    def test_remove_nonexistent_node(self):
        with self.assertRaises(AssertionError):
            self.pipeline.remove_node("nonexistent_id")

    def test_remove_node_also_removes_children(self):
        self.pipeline.add_node(self.root_node.id, self.child_node)
        self.pipeline.add_node(self.child_node.id, self.statistical_node)
        self.pipeline.remove_node(self.child_node.id)
        self.assertNotIn(self.child_node, self.root_node.children)
        self.assertNotIn(self.statistical_node, self.child_node.statistical_children)


if __name__ == '__main__':
    unittest.main()
