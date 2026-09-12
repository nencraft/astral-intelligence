from django.test import SimpleTestCase

from .services.briefing_response import (
    BriefingResponseError,
    normalize_briefing_response,
)


class BriefingResponseTests(SimpleTestCase):
    def setUp(self):
        self.response = {
            "plain_english_summary": "General summary.",
            "technical_summary": "Technical summary.",
            "risk_context": "Risk context.",
        }

    def assert_response_error(self, expected_message, response=None):
        response = self.response if response is None else response

        with self.assertRaises(BriefingResponseError) as context:
            normalize_briefing_response(response)

        self.assertIn(expected_message, str(context.exception))

    def test_normalize_briefing_response_returns_clean_data(self):
        self.response["plain_english_summary"] = "  General summary.  "

        result = normalize_briefing_response(self.response)

        self.assertEqual(
            result,
            {
                "plain_english_summary": "General summary.",
                "technical_summary": "Technical summary.",
                "risk_context": "Risk context.",
            },
        )

    def test_rejects_non_object_response(self):
        self.assert_response_error("JSON object", response=[])

    def test_rejects_missing_required_field(self):
        del self.response["technical_summary"]

        self.assert_response_error("technical_summary")

    def test_rejects_unexpected_field(self):
        self.response["extra_field"] = "Unexpected."

        self.assert_response_error("extra_field")

    def test_rejects_invalid_text_values(self):
        invalid_values = (None, 123, "", "   ")

        for invalid_value in invalid_values:
            with self.subTest(value=invalid_value):
                self.response["risk_context"] = invalid_value

                self.assert_response_error("risk_context")
