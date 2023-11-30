import unittest
from dataharmonix.utils.register import register_operator

class TestRegistry(unittest.TestCase):

    def test_register_operator(self):
        operator_json = '''
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
        register_operator(operator_json)

if __name__ == '__main__':
    unittest.main()
