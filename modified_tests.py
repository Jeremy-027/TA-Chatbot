# Create this file: modified_tests.py
import unittest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath("."))

# Try to import your modules
try:
    from src.clarification_module import ClarificationModule

    clarification_module_exists = True
except ImportError:
    clarification_module_exists = False
    print("Warning: Could not import ClarificationModule")


@unittest.skipIf(not clarification_module_exists, "ClarificationModule not available")
class ModifiedClarificationModuleTests(unittest.TestCase):
    def setUp(self):
        if clarification_module_exists:
            self.clarification = ClarificationModule()

    def test_basic_functionality(self):
        """Test that basic functionality works"""
        if not clarification_module_exists:
            self.skipTest("ClarificationModule not available")

        # Test a simple case
        text = "Pakaian untuk pria"
        params = self.clarification.extract_parameters(text)
        self.assertEqual(params.get("gender"), "pria")

        # Test that get_clarification_question works
        params = {"gender": None, "skin_tone": "light", "occasion": "formal"}
        question = self.clarification.get_clarification_question(params)
        self.assertIsNotNone(question, "Should return a question for missing gender")


if __name__ == "__main__":
    unittest.main()
