# Create this file: robust_test_runner.py
import unittest
import sys
import os
import importlib

# Add the project root to the path
sys.path.insert(0, os.path.abspath("."))

# Make sure src and tests are recognized as packages
for directory in ["src", "tests"]:
    if os.path.exists(directory) and not os.path.exists(f"{directory}/__init__.py"):
        with open(f"{directory}/__init__.py", "w") as f:
            f.write("# Makes this directory a Python package")


def run_specific_test(test_class, test_method=None):
    """Run a specific test class or method"""
    suite = unittest.TestSuite()

    if test_method:
        suite.addTest(test_class(test_method))
    else:
        suite.addTest(unittest.makeSuite(test_class))

    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    print("Fashion Chatbot Robust Test Runner")
    print("=================================")

    if len(sys.argv) < 2:
        print(
            "Usage: python robust_test_runner.py [module_name] [class_name] [method_name]"
        )
        print("Examples:")
        print("  python robust_test_runner.py clarification_module")
        print(
            "  python robust_test_runner.py clarification_module TestClarificationModule"
        )
        print(
            "  python robust_test_runner.py clarification_module TestClarificationModule test_empty_input"
        )
        sys.exit(1)

    module_name = sys.argv[1]
    class_name = sys.argv[2] if len(sys.argv) > 2 else None
    method_name = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        # Try to import the test module
        test_module_name = f"tests.test_{module_name}"
        try:
            test_module = importlib.import_module(test_module_name)
            print(f"Successfully imported {test_module_name}")
        except ImportError as e:
            print(f"Error importing {test_module_name}: {e}")
            sys.exit(1)

        # Get the test class
        if class_name:
            test_class = getattr(test_module, class_name)

            # Run the specific test method or all methods in the class
            if method_name:
                print(f"Running {class_name}.{method_name}")
                result = run_specific_test(test_class, method_name)
            else:
                print(f"Running all tests in {class_name}")
                result = run_specific_test(test_class)
        else:
            # Run all tests in the module
            print(f"Running all tests in {test_module_name}")
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(test_module)
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)

        # Print summary
        print("\nTest Summary:")
        print(f"Ran {result.testsRun} tests")
        print(
            f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}"
        )
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")

        sys.exit(0 if result.wasSuccessful() else 1)

    except Exception as e:
        print(f"Error running tests: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
