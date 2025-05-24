# Run this in your Python environment
import os

# Verify the file structure
if os.path.exists("tests/__init__.py"):
    print("tests/__init__.py exists ✓")
else:
    print("tests/__init__.py is missing ✗")

# List all files in the tests directory
print("\nFiles in tests directory:")
if os.path.exists("tests"):
    for file in os.listdir("tests"):
        print(f"  - {file}")
else:
    print("tests directory not found")
