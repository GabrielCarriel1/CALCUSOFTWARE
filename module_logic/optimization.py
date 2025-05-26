"""
This module provides functions for numerical optimization algorithms.
It currently includes an implementation of the Gradient Descent algorithm.
"""
import numpy as np

def gradient_descent(objective_function, gradient_function, initial_point, learning_rate, num_iterations):
    """
    Performs gradient descent to find the minimum of an objective function.

    Args:
        objective_function (callable): A function that takes a point (list or np.ndarray)
                                       and returns a scalar value (the objective).
        gradient_function (callable): A function that takes a point (list or np.ndarray)
                                      and returns the gradient (list or np.ndarray) at that point.
        initial_point (list | np.ndarray): The starting point for the descent.
        learning_rate (float): The step size for each iteration.
        num_iterations (int): The number of iterations to perform.

    Returns:
        tuple: A tuple containing:
            - np.ndarray: The point that minimizes the objective function after the iterations.
            - float: The value of the objective function at the minimized point.

    Raises:
        ValueError: If the dimensions of the point and its gradient do not match.
    """
    # Ensure initial_point is a numpy array for easier calculations
    point = np.array(initial_point, dtype=float)

    for i in range(num_iterations):
        grad = np.array(gradient_function(point), dtype=float)

        # Basic dimension check
        if point.shape != grad.shape:
            raise ValueError(
                f"Iteration {i+1}: The dimensions of the point {point.shape} "
                f"and its gradient {grad.shape} must be the same."
            )

        point = point - learning_rate * grad
        
        # Optional: You can uncomment the line below to see the progress of the optimization
        # print(f"Iteration {i+1}: point={point}, value={objective_function(point)}")

    return point, objective_function(point)

# Example usage (can be commented out or removed later for production code)
if __name__ == '__main__':
    # Define a simple objective function: f(x, y) = x^2 + y^2
    # The minimum is at (0, 0) with value 0.
    def objective_fn_example(p):
        return p[0]**2 + p[1]**2

    # Define the gradient of the objective function: df/dx = 2x, df/dy = 2y
    def gradient_fn_example(p):
        return np.array([2*p[0], 2*p[1]])

    # Set parameters for gradient descent
    initial_coords = [5.0, 5.0]
    learn_rate = 0.1
    num_iters = 100

    print(f"Starting gradient descent with initial point: {initial_coords}, learning rate: {learn_rate}, iterations: {num_iters}")

    try:
        final_point, min_value = gradient_descent(
            objective_fn_example, 
            gradient_fn_example, 
            initial_coords, 
            learn_rate, 
            num_iters
        )
        print(f"Optimal point found: {final_point}")
        print(f"Minimum value of objective function: {min_value}")

        # Example with a dimension mismatch to test error handling
        def gradient_fn_mismatch(p):
            return np.array([2*p[0]]) # Incorrect gradient dimension

        # print("\nTesting error handling with mismatched gradient dimension...")
        # final_point_error, min_value_error = gradient_descent(
        #     objective_fn_example,
        #     gradient_fn_mismatch,
        #     initial_coords,
        #     learn_rate,
        #     num_iters
        # )

    except ValueError as e:
        print(f"An error occurred during gradient descent: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
