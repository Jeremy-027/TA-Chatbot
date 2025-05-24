# src/run_tests.py
import unittest
import os
import sys
import json
import time
from datetime import datetime

# Set up test directories
TEST_DIR = "tests"
RESULTS_DIR = "test_results"
os.makedirs(RESULTS_DIR, exist_ok=True)


def run_tests():
    """Run all automated tests and generate report."""
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Discover and run tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(TEST_DIR)

    # Run tests with XML reports for CI integration
    import xmlrunner

    result_file = os.path.join(RESULTS_DIR, f"test_results_{timestamp}.xml")
    with open(os.path.join(RESULTS_DIR, f"test_output_{timestamp}.txt"), "w") as f:
        runner = xmlrunner.XMLTestRunner(output=RESULTS_DIR, stream=f, verbosity=2)
        test_results = runner.run(test_suite)

    # Generate summary report
    total_tests = test_results.testsRun
    failed_tests = len(test_results.failures) + len(test_results.errors)
    passed_tests = total_tests - failed_tests

    execution_time = time.time() - start_time

    summary = {
        "timestamp": timestamp,
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "success_rate": passed_tests / total_tests if total_tests > 0 else 0,
        "execution_time": execution_time,
    }

    with open(os.path.join(RESULTS_DIR, f"summary_{timestamp}.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print("\n" + "=" * 60)
    print(f"Test Summary ({timestamp}):")
    print("-" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {summary['success_rate']*100:.2f}%")
    print(f"Execution Time: {execution_time:.2f} seconds")
    print("=" * 60)

    return test_results.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
