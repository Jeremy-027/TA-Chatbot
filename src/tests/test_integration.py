# src/tests/test_integration.py
import unittest
import time
import threading
import queue
import numpy as np
from chatbot_azure import AzureFashionChatbot


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.chatbot = AzureFashionChatbot()
        self.test_queries = [
            "saya mencari pakaian formal untuk pria berkulit cerah",
            "rekomendasi pakaian casual untuk wanita berkulit sawo matang",
            "baju apa yang cocok untuk interview kerja?",
            "pakaian untuk cuaca panas",
            "outfit untuk musim dingin",
            # Add more varied queries
        ]

    def test_end_to_end_pipeline(self):
        """Test the full pipeline from text input to response generation."""
        response_times = []
        success_count = 0

        for query in self.test_queries:
            start_time = time.time()
            response, is_error, json_data = self.chatbot.process_input(query)
            end_time = time.time()

            response_time = end_time - start_time
            response_times.append(response_time)

            if not is_error and response and json_data:
                success_count += 1
                print(f"Query: '{query}'")
                print(f"Response: '{response}'")
                print(f"Response time: {response_time:.4f} seconds")
                print("-" * 50)

        success_rate = success_count / len(self.test_queries)
        avg_response_time = sum(response_times) / len(response_times)
        p95_response_time = np.percentile(response_times, 95)

        print(f"Success Rate: {success_rate:.4f}")
        print(f"Average Response Time: {avg_response_time:.4f} seconds")
        print(f"P95 Response Time: {p95_response_time:.4f} seconds")

        self.assertGreater(
            success_rate, 0.95, "End-to-end success rate below threshold"
        )
        self.assertLess(avg_response_time, 2.0, "Average response time above threshold")
