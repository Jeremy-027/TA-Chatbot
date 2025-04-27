# src/chatbot_interface.py

from language_model import IndoBERTFashionProcessor
from response_generator import FashionResponseGenerator
from clarification_module import ClarificationModule
from color_selector import ColorSelector


class FashionChatbot:
    def __init__(self, model_path="./fine-tuned-model"):
        self.processor = IndoBERTFashionProcessor(model_path)
        self.response_generator = FashionResponseGenerator()
        self.clarification = ClarificationModule()
        self.color_selector = ColorSelector()

        # For maintaining conversation context
        self.conversation_state = {
            "awaiting_clarification": False,
            "pending_params": {},
            "clarification_type": None,
        }

    def process_query(self, text: str) -> str:
        """Process user query and generate appropriate response"""
        # Check if we're waiting for clarification
        if self.conversation_state["awaiting_clarification"]:
            return self._handle_clarification(text)

        # Classify intent
        intent = self.processor.classify_intent(text)

        # Extract parameters
        params = self.clarification.extract_parameters(text)

        # Check if we need clarification
        missing_param = self.clarification.get_clarification_question(params)
        if missing_param:
            self.conversation_state["awaiting_clarification"] = True
            self.conversation_state["pending_params"] = params
            self.conversation_state["clarification_type"] = next(
                key for key, value in params.items() if value is None
            )
            return missing_param

        # Generate response with complete parameters
        response = self.response_generator.generate_response(
            params["gender"], params["skin_tone"], params["occasion"]
        )

        return response

    def _handle_clarification(self, text: str) -> str:
        """Handle user's response to clarification question"""
        clarification_type = self.conversation_state["clarification_type"]
        params = self.conversation_state["pending_params"]

        if clarification_type == "gender":
            if any(
                keyword in text.lower()
                for keyword in self.clarification.gender_keywords["pria"]
            ):
                params["gender"] = "pria"
            elif any(
                keyword in text.lower()
                for keyword in self.clarification.gender_keywords["wanita"]
            ):
                params["gender"] = "wanita"

        elif clarification_type == "skin_tone":
            for tone, keywords in self.clarification.skin_tone_keywords.items():
                if any(keyword in text.lower() for keyword in keywords):
                    params["skin_tone"] = tone
                    break

        elif clarification_type == "occasion":
            for occasion, keywords in self.clarification.occasion_keywords.items():
                if any(keyword in text.lower() for keyword in keywords):
                    params["occasion"] = occasion
                    break

        # Check if we still need clarification
        missing_param = self.clarification.get_clarification_question(params)
        if missing_param:
            self.conversation_state["clarification_type"] = next(
                key for key, value in params.items() if value is None
            )
            return missing_param

        # Reset state
        self.conversation_state["awaiting_clarification"] = False

        # Generate response
        response = self.response_generator.generate_response(
            params["gender"], params["skin_tone"], params["occasion"]
        )

        return response
