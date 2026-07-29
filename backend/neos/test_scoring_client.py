import json

import httpx

from django.test import SimpleTestCase, override_settings

from .services.scoring_client import ScoringClientError, request_score


class RequestScoreTests(SimpleTestCase):
    @override_settings(
        SCORING_SERVICE_URL="http://scoring.test",
        SCORING_SERVICE_TIMEOUT_SECONDS=5.0,
    )
    def test_request_score_posts_payload_and_returns_decoded_response(self):
        request_payload = {
            "estimatedDiameterMinKm": "0.200000",
            "estimatedDiameterMaxKm": "0.400000",
            "missDistanceKm": "10000000.000",
            "relativeVelocityKps": "15.000000",
            "isPotentiallyHazardous": True,
            "closeApproachDate": "2026-08-10",
        }

        expected_response = {
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

        def handler(request):
            self.assertEqual(request.method, "POST")
            self.assertEqual(str(request.url), "http://scoring.test/api/score")
            self.assertEqual(json.loads(request.content), request_payload)

            return httpx.Response(
                200,
                json=expected_response,
                request=request,
            )

        client = httpx.Client(transport=httpx.MockTransport(handler))

        result = request_score(
            request_payload,
            client=client,
        )

        self.assertEqual(result, expected_response)

    def test_request_score_raises_client_error_for_timeout(self):
        request_payload = {}

        def handler(request):
            raise httpx.TimeoutException(
                "Request timed out",
                request=request,
            )

        client = httpx.Client(transport=httpx.MockTransport(handler))

        with self.assertRaises(ScoringClientError):
            request_score(
                request_payload, 
                client=client,
            )

    def test_request_score_raises_client_error_for_non_success_response(self):
        payload = {}

        def handler(request):
            return httpx.Response(
                500,
                json={"error": "Scoring service unavailable"},
                request=request,
            )

        client = httpx.Client(transport=httpx.MockTransport(handler))

        with self.assertRaises(ScoringClientError) as context:
            request_score(
                payload,
                client=client
            )

        self.assertIn("500", str(context.exception))

    def test_request_score_raises_client_error_for_invalid_json(self):
      payload = {}

      def handler(request):
          return httpx.Response(
              200,
              content=b"not-json",
              request=request,
          )

      client = httpx.Client(transport=httpx.MockTransport(handler))

      with self.assertRaises(ScoringClientError) as context:
          request_score(
              payload,
              client=client,
          )

      self.assertIn("invalid JSON", str(context.exception))
