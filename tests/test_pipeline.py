import unittest
from dataharmonix.operators.operator import Operator
from dataharmonix.pipeline.pipeline import PipelineNode, DataPipeline
import json

class TestPipelineNode(unittest.TestCase):

    def test_node_creation(self):
        config = json.dumps({
            "name": "TestNode",
            "operator_type": "function",
            "callable": "some_module.some_function",
            "is_statistical": False
        })
        node = PipelineNode(config)
        self.assertIsNotNone(node.id)
        self.assertFalse(node.is_statistical)

    def test_add_remove_child(self):
        parent_config = json.dumps({"name": "Parent"})
        child_config = json.dumps({"name": "Child"})

        parent_node = PipelineNode(parent_config)
        child_node = PipelineNode(child_config)

        parent_node.add_child(child_node)
        self.assertEqual(len(parent_node.children), 1)

        parent_node.remove_child(child_node)
        self.assertEqual(len(parent_node.children), 0)

    # Add more tests for execution, statistical nodes, etc.

# class TestDataPipeline(unittest.TestCase):

    def test_pipeline_execution(self):
        root_config = json.dumps({"name": "Root"})
        child_config = json.dumps({"name": "Child"})

        root_node = PipelineNode(root_config)
        child_node = PipelineNode(child_config)

        root_node.add_child(child_node)
        pipeline = DataPipeline(root_node)

        # Assuming you have a way to mock or provide input data
        input_data = ...
        results = pipeline.run(input_data)

        # Assertions based on expected results

if __name__ == '__main__':
    unittest.main()
