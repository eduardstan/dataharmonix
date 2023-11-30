import unittest
from dataharmonix.operators import Operator

class TestOperator(unittest.TestCase):

    # def test_load_config(self):
      
    #     config_json = '''
    #     {
    #         "name": "SimpleAddition",
    #         "description": "Performs simple addition",
    #         "operator_type": "function",
    #         "callable": "math_operations.add",
    #         "input_type": "number",
    #         "output_type": "number",
    #         "parameters": [
    #             {
    #                 "name": "addend",
    #                 "type": "integer",
    #                 "description": "The number to add",
    #                 "default": 5,
    #                 "required": true
    #             }
    #         ],
    #         "dependencies": []
    #     }
    #     '''
    #     operator = Operator(config_json=config_json)
    #     self.assertIsNotNone(operator.config, "Config should not be None")

    def test_validate_config(self):
        valid_config = '''
        {
          "name": "PAAOperator",
          "description": "Applies Piecewise Aggregate Approximation",
          "operator_type": "class",
          "callable": "sktime.transformers.series_as_features.PiecewiseAggregateApproximation",
          "methods": ["fit", "transform"],
          "input_type": "Timeseries",
          "output_type": "Timeseries",
          "parameters": [
            {
              "name": "num_intervals",
              "type": "integer",
              "description": "Number of intervals of the transformation",
              "default": 8,
              "required": true
            }
          ],
          "dependencies": [
            {
              "package_name": "sktime",
              "doc_link": "https://www.sktime.org"
            }
          ]
        }
        '''
        
        invalid_config = '''
        {
          "name": "InvalidOperator",
          "description": "This is an invalid operator configuration",
          "operator_type": "function",
          "callable": "math_operations.subtract",
          "input_type": "number",
          "output_type": "number",
          "parameters": [
            {
              "name": "subtrahend",
              "type": "integer",
              "description": "The number to subtract",
              "default": "five",  // Incorrect data type (string instead of integer)
              "required": true
            }
          ],
          "dependencies": []
        }
        '''
        _ = Operator(config_json=valid_config)
        self.assertRaises(ValueError, Operator, invalid_config)

    def test_execute_function(self):
        
        function_config = '''
        {
          "name": "ArithmeticAddOperation",
          "description": "Adds a costant to data",
          "operator_type": "function",
          "callable": "dataharmonix.utils.arithmetic_operations.simple_add_function",
          "input_type": "number",
          "output_type": "number",
          "parameters": [
            {
              "name": "constant",
              "type": "float",
              "description": "Constant to add",
              "default": 1.0,
              "required": false
            }
          ],
          "dependencies": []
        }
        '''
        operator = Operator(config_json=function_config)
        data = [1,2,3,4]
        result = operator.execute(data, {"constant": 1.0})
        self.assertEqual(result, [2,3,4,5])

    # def test_execute_class(self):
    #     class_config = '''
    #     {
    #       "name": "TimeSeriesTransformer",
    #       "description": "Transforms time series data",
    #       "operator_type": "class",
    #       "callable": "sktime.transformations.panel.dictionary_based.PAA",
    #       "methods": ["fit", "transform"],
    #       "input_type": "time_series",
    #       "output_type": "time_series",
    #       "parameters": [
    #         {
    #           "name": "num_intervals",
    #           "type": "integer",
    #           "description": "Number of intervals for the transformation.",
    #           "default": 8,
    #           "required": true
    #         }
    #       ],
    #       "dependencies": [
    #         {
    #           "package_name": "sktime",
    #           "doc_link": "https://www.sktime.org"
    #         }
    #       ]
    #     }
    #     '''
    #     from sktime.datasets import load_basic_motions
    #     import numpy as np
    #     X, _ = load_basic_motions(return_X_y=True)
    #     indices = np.random.RandomState(4).choice(len(X), 5, replace=False)
    #     # Similar to test_execute_function, but for a class-based operator
    #     operator = Operator(config_json=class_config)
    #     result = operator.execute(X.iloc[indices], {'num_intervals': 8})
    #     # self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
