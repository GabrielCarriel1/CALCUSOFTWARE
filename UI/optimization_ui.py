"""
This module provides the user interface for optimization algorithms,
specifically for the Gradient Descent method. It allows users to input
parameters for the optimization and view the results.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
# Ensure this import works. If module_logic is not in PYTHONPATH, this might fail at runtime.
# It might need to be adjusted based on how the main application runs (e.g., if the root project folder is in sys.path)
try:
    from module_logic.optimization import gradient_descent
except ImportError:
    # Try relative import if the above fails, common if script is run directly from UI folder
    # or if module_logic is not directly in a standard Python path location.
    # This assumes 'module_logic' is a sibling directory to 'UI'.
    import sys
    import os
    # Get the parent directory of the current file's directory (UI)
    # This should be the project root if UI and module_logic are siblings
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from module_logic.optimization import gradient_descent


class OptimizationUI(tk.Toplevel):
    """
    A Toplevel window for configuring and running the Gradient Descent optimization.

    This UI allows users to define an objective function, its gradient,
    an initial starting point, learning rate, and the number of iterations.
    It then calls the core gradient_descent function and displays the
    resulting optimal point and function value, or any errors encountered.
    """
    def __init__(self, master=None):
        """
        Initializes the OptimizationUI Toplevel window.

        Args:
            master (tk.Widget, optional): The parent widget. Defaults to None.
        """
        super().__init__(master)
        self.title("Gradient Descent Optimization")
        self.geometry("450x450") # Adjusted for potentially longer error messages

        # Frame for input fields
        input_frame = ttk.Frame(self, padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True)

        # --- Input Fields ---
        ttk.Label(input_frame, text="Objective Function (e.g., p[0]**2 or p[0]**2 + p[1]**2):").grid(row=0, column=0, sticky="w", pady=2)
        self.obj_func_str = tk.StringVar(value="p[0]**2") # Default for 1 var
        ttk.Entry(input_frame, textvariable=self.obj_func_str, width=40).grid(row=0, column=1, pady=2)

        ttk.Label(input_frame, text="Gradient Function (e.g., [2*p[0]] or [2*p[0], 2*p[1]]):").grid(row=1, column=0, sticky="w", pady=2)
        self.grad_func_str = tk.StringVar(value="[2*p[0]]") # Default for 1 var
        ttk.Entry(input_frame, textvariable=self.grad_func_str, width=40).grid(row=1, column=1, pady=2)

        ttk.Label(input_frame, text="Initial Point (comma-separated, e.g., 5.0 or 5.0,3.0):").grid(row=2, column=0, sticky="w", pady=2)
        self.initial_point_str = tk.StringVar(value="5.0") # Default for 1 var
        ttk.Entry(input_frame, textvariable=self.initial_point_str, width=40).grid(row=2, column=1, pady=2)

        ttk.Label(input_frame, text="Learning Rate:").grid(row=3, column=0, sticky="w", pady=2)
        self.learning_rate_str = tk.StringVar(value="0.1")
        ttk.Entry(input_frame, textvariable=self.learning_rate_str, width=40).grid(row=3, column=1, pady=2)

        ttk.Label(input_frame, text="Iterations:").grid(row=4, column=0, sticky="w", pady=2)
        self.iterations_str = tk.StringVar(value="100")
        ttk.Entry(input_frame, textvariable=self.iterations_str, width=40).grid(row=4, column=1, pady=2)

        # --- Calculate Button ---
        self.calculate_button = ttk.Button(input_frame, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

        # --- Results Display ---
        self.result_label = ttk.Label(input_frame, text="Result will be shown here.", wraplength=400)
        self.result_label.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Configure column weights for proper spacing
        input_frame.grid_columnconfigure(1, weight=1)


    def calculate(self):
        """
        Handles user input, calls the gradient descent algorithm, and displays results or errors.

        This method retrieves the objective function string, gradient function string,
        initial point, learning rate, and number of iterations from the UI input fields.
        It performs validation on these inputs, converts string functions to callable
        functions using `eval()` (with a restricted environment for safety),
        and then executes the `gradient_descent` algorithm from the `module_logic.optimization` module.
        
        The results (optimal point and minimum value) are displayed in a label.
        If any errors occur during input parsing, function evaluation, or the
        optimization process, an appropriate error message is shown to the user
        via a `messagebox`.
        """
        try:
            obj_func_str_val = self.obj_func_str.get()
            grad_func_str_val = self.grad_func_str.get()

            # Basic validation for empty fields
            if not all([obj_func_str_val, grad_func_str_val, self.initial_point_str.get(), 
                        self.learning_rate_str.get(), self.iterations_str.get()]):
                messagebox.showerror("Input Error", "All fields must be filled.")
                return

            # Using eval is risky. Ensure 'p' is the list/array of variables, and 'np' is numpy.
            # The restricted globals provide some mitigation but not full security.
            # For objective function, it expects p (a list/array) and returns a scalar
            # For gradient function, it expects p (a list/array) and returns a list/array
            # We pass 'np' to eval's globals. 'p' (representing p_vars) is passed in the lambda's local scope.
            safe_globals = {"np": np, "__builtins__": {}} # Disallow most builtins for safety
            
            objective_fn = lambda p_vars: eval(obj_func_str_val, safe_globals, {"p": p_vars})
            gradient_fn = lambda p_vars: eval(grad_func_str_val, safe_globals, {"p": p_vars})

            initial_point_str_val = self.initial_point_str.get()
            try:
                initial_point = [float(x.strip()) for x in initial_point_str_val.split(',')]
            except ValueError:
                messagebox.showerror("Input Error", "Initial point must be comma-separated numbers (e.g., 5.0 or 5.0,3.0).")
                return

            try:
                learning_rate = float(self.learning_rate_str.get())
                iterations = int(self.iterations_str.get())
                if learning_rate <= 0:
                    messagebox.showerror("Input Error", "Learning rate must be positive.")
                    return
                if iterations <= 0:
                    messagebox.showerror("Input Error", "Number of iterations must be positive.")
                    return
            except ValueError:
                messagebox.showerror("Input Error", "Learning rate and iterations must be valid numbers.")
                return

            # Test functions with a sample point of the correct dimension
            # This helps catch errors in function definitions early.
            try:
                test_p = np.array(initial_point) # Use a NumPy array for testing
                # print(f"Testing objective function with: {test_p}") # Debug print
                obj_test_val = objective_fn(test_p)
                # print(f"Objective function test output: {obj_test_val}") # Debug print
                # print(f"Testing gradient function with: {test_p}") # Debug print
                grad_test_val = np.array(gradient_fn(test_p)) # Ensure gradient is array for shape check
                # print(f"Gradient function test output: {grad_test_val}") # Debug print

                if not isinstance(obj_test_val, (int, float, np.number)):
                     messagebox.showerror("Function Error", "Objective function must return a single number (scalar).")
                     return
                # Check if gradient_fn returns a list or array-like structure
                if not isinstance(grad_test_val, np.ndarray) or grad_test_val.ndim == 0 : # grad_test_val.ndim == 0 if it's a scalar
                     messagebox.showerror("Function Error", "Gradient function must return a list or array of numbers (e.g., [2*p[0]] or np.array([2*p[0]])).")
                     return
                # Check if the dimensions of initial_point and gradient match
                if test_p.shape != grad_test_val.shape:
                    messagebox.showerror("Function Error", 
                                         f"Dimension mismatch: Initial point has {test_p.ndim} dimension(s) with shape {test_p.shape}, "
                                         f"but gradient function returns {grad_test_val.ndim} dimension(s) with shape {grad_test_val.shape}.\n"
                                         "Ensure gradient output matches point structure (e.g., if point is [1.0, 2.0], gradient should be like [0.5, -0.1]).")
                    return


            except Exception as e:
                messagebox.showerror("Function Definition Error", 
                                     f"Error evaluating user-defined functions: {e}\n"
                                     "Ensure functions use 'p[index]' for variables (e.g., p[0], p[1]) "
                                     "and 'np' for NumPy functions (e.g., np.exp).\n"
                                     "Example for 1 variable: Objective: p[0]**2, Gradient: [2*p[0]]\n"
                                     "Example for 2 variables: Objective: p[0]**2 + p[1]**2, Gradient: [2*p[0], 2*p[1]]")
                return

            optimal_point, min_value = gradient_descent(
                objective_fn, gradient_fn, initial_point, learning_rate, iterations
            )
            self.result_label.config(text=f"Optimal Point: {np.array2string(optimal_point, precision=4)}\nMinimum Value: {min_value:.4f}")

        except ValueError as ve: # Catches errors from gradient_descent itself (e.g. dimension mismatch)
            messagebox.showerror("Calculation Error", f"Error during gradient descent: {ve}")
        except Exception as e:
            # This will catch other unexpected errors, including certain types of eval errors not caught above
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    # This is for testing the UI independently
    # The main application would typically create and manage this window.
    root = tk.Tk()
    # If this UI is part of a larger app, you might not want to hide the root window
    # or you might want to handle the root window differently.
    # For standalone testing of this Toplevel window:
    if root.winfo_viewable(): # Check if root window is actually there and not already withdrawn
        root.withdraw() # Hide the main root window when testing this dialog.
    
    app = OptimizationUI(master=root) # Pass root so it behaves like a dialog
    
    # Protocol to show the root window again if the OptimizationUI is closed by 'x' button
    def on_closing():
        app.destroy()
        # if not root.winfo_viewable(): # Only deiconify if it was withdrawn
        # try:
        #     root.deiconify() # This can cause issues if root was destroyed elsewhere
        # except tk.TclError:
        #     pass # Root window might already be destroyed
        # For standalone test, just quit
        root.quit()


    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
```
