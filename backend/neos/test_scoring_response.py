from django.test import SimpleTestCase

from .services.scoring_response import (
    ScoringResponseError,
    normalize_score_response,
)


class ScoringResponseTests(SimpleTestCase):
    def setUp(self):
        self.response = {
            "score": 81,
            "category": "Critical Review",
            "modelVersion": "APS-v1",
            "factors": {
                "diameter": 21,
                "distance": 21,
                "velocity": 12,
                "timing": 12,
                "hazardFlag": 15,
            },
            "explanation": "Critical Review based on APS-v1 factors.",
        }

        self.expected_response = {
            "score": 81,
            "category": "Critical Review",
            "model_version": "APS-v1",
            "diameter_factor": 21,
            "distance_factor": 21,
            "velocity_factor": 12,
            "timing_factor": 12,
            "hazard_flag_factor": 15,
            "explanation": "Critical Review based on APS-v1 factors.",
        }

    def assert_response_error(self, expected_message, response=None):
        response = self.response if response is None else response

        with self.assertRaises(ScoringResponseError) as context:
            normalize_score_response(response)

        self.assertIn(
            expected_message,
            str(context.exception),
        )

    def test_normalize_score_response_returns_internal_data(self):
        result = normalize_score_response(self.response)

        self.assertEqual(result, self.expected_response)

    def test_normalize_score_response_rejects_missing_model_version(self):
        del self.response["modelVersion"]

        self.assert_response_error("modelVersion")

    def test_normalize_score_response_rejects_missing_factor(self):
        del self.response["factors"]["velocity"]

        self.assert_response_error("velocity")

    def test_normalize_score_response_rejects_non_object_response(self):
        self.assert_response_error(
            "response",
            response=[],
        )

    def test_normalize_score_response_rejects_non_object_factors(self):
        self.response["factors"] = []

        self.assert_response_error("factors")

    def test_normalize_score_response_rejects_non_integer_score(self):
        self.response["score"] = "81"

        self.assert_response_error("score")

    def test_normalize_score_response_rejects_score_outside_range(self):
        for invalid_score in (-1, 101):
            with self.subTest(score=invalid_score):
                self.response["score"] = invalid_score

                self.assert_response_error("score")

    def test_normalize_score_response_rejects_non_integer_factor(self):
        self.response["factors"]["diameter"] = "21"

        self.assert_response_error("diameter")

    def test_normalize_score_response_rejects_factor_outside_range(self):
        cases = (
            ("diameter", 26),
            ("distance", 26),
            ("velocity", 21),
            ("timing", 16),
            ("hazardFlag", 16),
            ("diameter", -1),
        )

        for factor_name, invalid_value in cases:
            with self.subTest(
                factor=factor_name,
                value=invalid_value,
            ):
                original_value = self.response["factors"][factor_name]
                self.response["factors"][factor_name] = invalid_value

                self.assert_response_error(factor_name)

                self.response["factors"][factor_name] = original_value

    def test_normalize_score_response_rejects_incorrect_factor_total(self):
        self.response["score"] = 80

        self.assert_response_error("factor total")

    def test_normalize_score_response_rejects_incorrect_category(self):
        self.response["category"] = "Moderate Interest"

        self.assert_response_error("category")

    def test_normalize_score_response_rejects_empty_model_version(self):
        self.response["modelVersion"] = "   "

        self.assert_response_error("modelVersion")

    def test_normalize_score_response_rejects_empty_explanation(self):
        self.response["explanation"] = ""

        self.assert_response_error("explanation")