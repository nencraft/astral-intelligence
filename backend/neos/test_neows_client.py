from datetime import date
from unittest.mock import patch

import httpx
from django.test import SimpleTestCase

from .services.neows_client import NeoWsClientError, fetch_neows_feed


class FetchNeoWsFeedTests(SimpleTestCase):
    def test_fetch_neows_feed_returns_decoded_json_response(self):
        expected_payload = {
            "element_count": 0,
            "near_earth_objects": {},
        }

        def handler(request):
            self.assertEqual(
                str(request.url),
                "https://api.nasa.gov/neo/rest/v1/feed"
                "?start_date=2026-06-01"
                "&end_date=2026-06-07"
                "&api_key=test-key",
            )
            return httpx.Response(200, json=expected_payload)

        transport = httpx.MockTransport(handler)
        client = httpx.Client(transport=transport)

        result = fetch_neows_feed(
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 7),
            api_key="test-key",
            client=client,
        )

        self.assertEqual(result, expected_payload)


    def test_fetch_neows_feed_requires_api_key(self):
        with self.assertRaises(NeoWsClientError):
            fetch_neows_feed(
                start_date=date(2026, 6, 1),
                end_date=date(2026, 6, 7),
                api_key=None,
                client=httpx.Client(
                    transport=httpx.MockTransport(
                        lambda request: httpx.Response(200, json={})
                    )
                ),
            )


    def test_fetch_neows_feed_raises_client_error_for_non_success_response(self):
        def handler(request):
            return httpx.Response(
                500,
                json={"error": "NASA service unavailable"},
                request=request,
            )

        client = httpx.Client(transport=httpx.MockTransport(handler))

        with self.assertRaises(NeoWsClientError):
            fetch_neows_feed(
                start_date=date(2026, 6, 1),
                end_date=date(2026, 6, 7),
                api_key="test-key",
                client=client,
            )


    def test_fetch_neows_feed_raises_client_error_for_request_failure(self):
        def handler(request):
            raise httpx.TimeoutException(
                "Request timed out",
                request=request,
            )

        client = httpx.Client(transport=httpx.MockTransport(handler))

        with self.assertRaises(NeoWsClientError):
            fetch_neows_feed(
                start_date=date(2026, 6, 1),
                end_date=date(2026, 6, 7),
                api_key="test-key",
                client=client,
            )


    @patch.dict("os.environ", {"NASA_API_KEY": "env-test-key"})
    def test_fetch_neows_feed_uses_api_key_from_environment(self):
        expected_payload = {
            "element_count": 0,
            "near_earth_objects": {},
        }

        def handler(request):
            self.assertIn("api_key=env-test-key", str(request.url))
            return httpx.Response(200, json=expected_payload)

        client = httpx.Client(transport=httpx.MockTransport(handler))

        result = fetch_neows_feed(
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 7),
            client=client,
        )

        self.assertEqual(result, expected_payload)

