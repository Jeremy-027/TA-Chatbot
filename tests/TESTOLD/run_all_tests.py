# tests/run_all_tests.py

import unittest
import os
import sys
import time

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import all the test modules
from tests.test_clarification_module import TestClarificationModule
from tests.test_fashion_mapping import TestFashionMapping
from tests.test_response_generator import TestResponseGenerator
from tests.test_clothing_selector import TestClothingSelector
from tests.test_language_model import TestIndoBERTFashionProcessor
from tests.test_chatbot_azure import TestAzureFashionChatbot


def run_tests():
    """Run all test modules and generate a summary report"""
    # Create test suite
    test_suite = unittest.TestSuite()

    # Add all tests from test classes
    test_classes = [
        TestClarificationModule,
        TestFashionMapping,
        TestResponseGenerator,
        TestClothingSelector,
        TestIndoBERTFashionProcessor,
        TestAzureFashionChatbot,
    ]

    for test_class in test_classes:
        test_suite.addTest(unittest.makeSuite(test_class))

    # Create test runner
    test_runner = unittest.TextTestRunner(verbosity=2)

    # Start timing
    start_time = time.time()

    # Run the tests
    test_result = test_runner.run(test_suite)

    # End timing
    end_time = time.time()

    # Generate summary report
    print("\n" + "=" * 70)
    print("FASHION CHATBOT TEST SUMMARY")
    print("=" * 70)
    print(f"Total tests run: {test_result.testsRun}")
    print(
        f"Tests passed: {test_result.testsRun - len(test_result.failures) - len(test_result.errors)}"
    )
    print(f"Tests failed: {len(test_result.failures)}")
    print(f"Tests with errors: {len(test_result.errors)}")
    print(f"Total test time: {end_time - start_time:.2f} seconds")
    print("=" * 70)

    # Print failures and errors if any
    if test_result.failures:
        print("\nFAILURES:")
        for test, error in test_result.failures:
            print(f"\n- {test}")
            print(f"  {error}")

    if test_result.errors:
        print("\nERRORS:")
        for test, error in test_result.errors:
            print(f"\n- {test}")
            print(f"  {error}")

    # Return success status (True if all tests passed)
    return len(test_result.failures) == 0 and len(test_result.errors) == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
