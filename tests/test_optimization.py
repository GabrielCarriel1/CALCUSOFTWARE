import unittest
import numpy as np
import sys
import os

# Adjust path to import from module_logic
# This is necessary because the 'tests' directory is a sibling to 'module_logic'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from module_logic.optimization import gradient_descent

class TestGradientDescent(unittest.TestCase):

    def test_simple_quadratic_1d(self):
        """Test with f(x) = x^2"""
        objective_fn = lambda p: p[0]**2
        gradient_fn = lambda p: [2*p[0]]
        initial_point = [5.0]
        learning_rate = 0.1
        iterations = 100
        
        optimal_point, min_value = gradient_descent(objective_fn, gradient_fn, initial_point, learning_rate, iterations)
        
        self.assertAlmostEqual(optimal_point[0], 0.0, places=4, msg="1D optimal point not close to 0.0")
        self.assertAlmostEqual(min_value, 0.0, places=4, msg="1D minimum value not close to 0.0")

    def test_simple_quadratic_2d(self):
        """Test with f(x,y) = x^2 + y^2"""
        objective_fn = lambda p: p[0]**2 + p[1]**2
        gradient_fn = lambda p: [2*p[0], 2*p[1]]
        initial_point = [3.0, 4.0]
        learning_rate = 0.1
        iterations = 100
        
        optimal_point, min_value = gradient_descent(objective_fn, gradient_fn, initial_point, learning_rate, iterations)
        
        self.assertAlmostEqual(optimal_point[0], 0.0, places=4, msg="2D optimal point[0] not close to 0.0")
        self.assertAlmostEqual(optimal_point[1], 0.0, places=4, msg="2D optimal point[1] not close to 0.0")
        self.assertAlmostEqual(min_value, 0.0, places=4, msg="2D minimum value not close to 0.0")

    def test_shifted_quadratic_1d(self):
        """Test with f(x) = (x - 3)^2"""
        objective_fn = lambda p: (p[0] - 3)**2
        gradient_fn = lambda p: [2*(p[0] - 3)]
        initial_point = [-2.0]
        learning_rate = 0.1
        iterations = 100
        
        optimal_point, min_value = gradient_descent(objective_fn, gradient_fn, initial_point, learning_rate, iterations)
        
        self.assertAlmostEqual(optimal_point[0], 3.0, places=4, msg="Shifted 1D optimal point not close to 3.0")
        self.assertAlmostEqual(min_value, 0.0, places=4, msg="Shifted 1D minimum value not close to 0.0")

    def test_dimension_mismatch_error(self):
        """Test that a ValueError is raised if point and gradient dimensions differ."""
        objective_fn = lambda p: p[0]**2 + p[1]**2
        # Gradient function intentionally returns a 1D gradient for a 2D point
        gradient_fn_mismatch = lambda p: np.array([2*p[0]]) 
        initial_point = [1.0, 2.0] # 2D point
        learning_rate = 0.1
        iterations = 5

        with self.assertRaisesRegex(ValueError, "dimensions of the point .* and its gradient .* must be the same"):
            gradient_descent(objective_fn, gradient_fn_mismatch, initial_point, learning_rate, iterations)
            
    def test_non_vector_gradient_output(self):
        """Test gradient function that doesn't return a list or np.array (should be handled by UI, but good to test optimizer too)"""
        # This test is more about how the gradient_descent function itself handles it.
        # The UI layer should ideally prevent this from reaching the optimizer.
        objective_fn = lambda p: p[0]**2
        gradient_fn_scalar = lambda p: 2*p[0] # Incorrectly returns a scalar, not array/list
        initial_point = [5.0]
        learning_rate = 0.1
        iterations = 5

        # The gradient_descent function converts gradient_function output to np.array.
        # If it's a scalar, np.array(scalar) is valid but might lead to unexpected behavior if not caught.
        # The current gradient_descent function's internal np.array(gradient_function(point))
        # will make a 0-d array from a scalar, which will then fail the shape check.
        with self.assertRaisesRegex(ValueError, "dimensions of the point .* and its gradient .* must be the same"):
             gradient_descent(objective_fn, gradient_fn_scalar, initial_point, learning_rate, iterations)


if __name__ == '__main__':
    # This allows running the tests from the command line: python -m tests.test_optimization
    # or if in the tests directory: python test_optimization.py
    unittest.main()
```
