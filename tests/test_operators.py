import unittest
from dataharmonix.operators import Operator
import json

class TestOperator(unittest.TestCase):

    def test_validate_config(self):
        valid_config = {
          "name": "PAA",
          "description": "Applies Piecewise Aggregate Approximation",
          "operator_type": "class",
          "callable": "sktime.transformers.series_as_features.PiecewiseAggregateApproximation",
          "methods": ["fit", "transform"],
          "operator_category": "normal",
          "input_type": "Timeseries",
          "output_type": "Timeseries",
          "parameters": [
            {
              "name": "num_intervals",
              "type": "integer",
              "description": "Number of intervals of the transformation",
              "default": 8,
              "required": True
            }
          ],
          "dependencies": [
            {
              "package_name": "sktime",
              "doc_link": "https://www.sktime.org"
            }
          ]
        }
        
        invalid_config = {
          "name": "InvalidPAAOperator",
          "description": "Applies Piecewise Aggregate Approximation",
          "operator_type": "class",
          "callable": "sktime.transformers.series_as_features.PiecewiseAggregateApproximation",
          "methods": ["fit", "transform"],
          "operator_category": "normal",
          "input_type": "Timeseries",
          "output_type": "Timeseries",
          "parameters": [
            {
              "name": "num_intervals",
              "type": "integer",
              "description": "Number of intervals of the transformation",
              "default": "eight", # Invalid type
              "required": True
            }
          ],
          "dependencies": [
            {
              "package_name": "sktime",
              "doc_link": "https://www.sktime.org"
            }
          ]
        }
        
        # Testing valid configuration (Should pass without raising exception)
        try:
            _ = Operator(config_json=json.dumps(valid_config))
            print("Valid config test passed.")
        except Exception as e:
            print(f"Unexpected exception for valid config: {e}")

        # Testing invalid configuration (Should raise ValueError)
        # TODO: not working
        with self.assertRaises(ValueError):
            print("Testing invalid config...")
            _ = Operator(config_json=json.dumps(invalid_config))

    # def test_execute_function(self):
        
    #     function_config = {
    #         "name": "ArithmeticAddOperation",
    #         "description": "Adds a constant to data",
    #         "operator_type": "function",
    #         "callable": "dataharmonix.utils.arithmetic_operations.simple_add_function",
    #         "operator_category": "normal",
    #         "input_type": "number",
    #         "output_type": "number",
    #         "parameters": [
    #             {
    #                 "name": "constant",
    #                 "type": "float",
    #                 "description": "Constant to add",
    #                 "default": 1.0,
    #                 "required": False
    #             }
    #         ],
    #         "dependencies": []
    #     }
        
    #     operator = Operator(config_json=json.dumps(function_config))
    #     data = [1,2,3,4]
    #     result = operator.execute(data, {"constant": 1.0})
    #     self.assertEqual(result, [2,3,4,5])

if __name__ == '__main__':
    unittest.main()
