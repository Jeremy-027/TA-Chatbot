# Run this to fix import issues
with open("tests/test_language_model.py", "r") as f:
    content = f.read()

# Fix imports to use src prefix
modified_content = content.replace(
    "from response_generator import ResponseGenerator",
    "from src.response_generator import ResponseGenerator",
)

with open("tests/test_language_model.py", "w") as f:
    f.write(modified_content)

print("Fixed import in test_language_model.py")

# Do the same for other files as needed
files_to_fix = [
    "src/language_model.py",
    "src/chatbot_azure.py",
    "src/chatbot_interface.py",
]

for file_path in files_to_fix:
    try:
        with open(file_path, "r") as f:
            content = f.read()

        # Replace imports
        modified_content = content.replace(
            "from response_generator import", "from src.response_generator import"
        )
        modified_content = modified_content.replace(
            "from fashion_mapping import", "from src.fashion_mapping import"
        )
        modified_content = modified_content.replace(
            "from clothing_selector import", "from src.clothing_selector import"
        )
        modified_content = modified_content.replace(
            "from clarification_module import", "from src.clarification_module import"
        )
        modified_content = modified_content.replace(
            "from language_model import", "from src.language_model import"
        )

        with open(file_path, "w") as f:
            f.write(modified_content)

        print(f"Fixed imports in {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
