import unittest
from dataharmonix.operators import Operator
import json
import pandas as pd
import os
from dataharmonix.utils.dummy_operators import create_dummy_loader_operator

class TestLoaderOperator(unittest.TestCase):

    def test_loader_operator_creation(self):
        operator = Operator(config_json=json.dumps(create_dummy_loader_operator(name="L1", description="Desc L1")))
        self.assertIsNotNone(operator)

    def test_loader_operator_execution(self):
        operator = Operator(config_json=json.dumps(create_dummy_loader_operator(name="L1", description="Desc L1")))
        # Adjust the file path to correctly point to the data folder
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_table.csv')
        result = operator.execute(None, {"filepath": file_path})
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(not result.empty)

    def test_loader_operator_with_invalid_path(self):
        operator = Operator(config_json=json.dumps(create_dummy_loader_operator(name="L1", description="Desc L1")))
        with self.assertRaises(ValueError):
            operator.execute(None, {"filepath": "nonexistent_file.txt"})

if __name__ == '__main__':
    unittest.main()
