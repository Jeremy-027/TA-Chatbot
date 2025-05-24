# run_tests.py - Python script to run tests for the Indonesian Fashion Chatbot
import os
import sys
import unittest
import importlib
import subprocess

print("Indonesian Fashion Chatbot - Testing Suite")
print("--------------------------------------------")


def run_test_module(module_name):
    """Run a specific test module"""
    print(f"\nRunning {module_name}...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", f"tests.{module_name}"],
            capture_output=True,
            text=True,
        )
        print(result.stdout)

        if result.returncode == 0:
            print(f"{module_name} completed successfully.")
        else:
            print(f"{module_name} failed.")
            print(result.stderr)
    except Exception as e:
        print(f"Error running {module_name}: {str(e)}")


def run_all_tests():
    """Run all test modules"""
    # Unit tests
    print("\nRUNNING UNIT TESTS")
    unit_tests = [
        "test_clarification_module",
        "test_fashion_mapping",
        "test_response_generator",
        "test_clothing_selector",
        "test_language_model",
        "test_chatbot_azure",
    ]

    for test in unit_tests:
        run_test_module(test)

    # Performance tests
    print("\nRUNNING PERFORMANCE TESTS")
    perf_tests = [
        "test_performance_latency",
        "test_resource_usage",
        "test_throughput",
        "test_speech_performance",
    ]

    for test in perf_tests:
        run_test_module(test)

    print("\nAll tests completed!")


def run_unit_tests():
    """Run only unit tests"""
    print("\nRUNNING UNIT TESTS")
    unit_tests = [
        "test_clarification_module",
        "test_fashion_mapping",
        "test_response_generator",
        "test_clothing_selector",
        "test_language_model",
        "test_chatbot_azure",
    ]

    for test in unit_tests:
        run_test_module(test)


def run_performance_tests():
    """Run only performance tests"""
    print("\nRUNNING PERFORMANCE TESTS")
    perf_tests = [
        "test_performance_latency",
        "test_resource_usage",
        "test_throughput",
        "test_speech_performance",
    ]

    for test in perf_tests:
        run_test_module(test)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python run_tests.py all          Run all tests")
        print("  python run_tests.py unit         Run unit tests")
        print("  python run_tests.py performance  Run performance tests")
    elif sys.argv[1] == "all":
        run_all_tests()
    elif sys.argv[1] == "unit":
        run_unit_tests()
    elif sys.argv[1] == "performance":
        run_performance_tests()
    else:
        print(f"Unknown option: {sys.argv[1]}")
        print("Usage:")
        print("  python run_tests.py all          Run all tests")
        print("  python run_tests.py unit         Run unit tests")
        print("  python run_tests.py performance  Run performance tests")
