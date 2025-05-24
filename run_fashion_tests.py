
import unittest
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.abspath('.'))

print("===== Fashion Chatbot Testing =====")

# Make sure the tests directory is a package
if not os.path.exists('tests/__init__.py'):
    with open('tests/__init__.py', 'w') as init_file:
        init_file.write('# Makes tests a Python package')
    print("Created tests/__init__.py")

# Discover and run tests
loader = unittest.TestLoader()
tests = loader.discover('tests', pattern='test_*.py')
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(tests)

# Print summary
print("\nTest Summary:")
print(f"Ran {result.testsRun} tests")
print(f"Failures: {len(result.failures)}")
print(f"Errors: {len(result.errors)}")

# Exit with proper code
sys.exit(len(result.failures) + len(result.errors))
