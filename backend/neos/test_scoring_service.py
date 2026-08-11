from datetime import date
from decimal import Decimal

import httpx
from django.test import TestCase

from .models import AstralScore, CloseApproach, NearEarthObject
from .services.scoring_client import ScoringClientError
from .services.scoring_payload import ScoringPayloadError
from .services.scoring_response import ScoringResponseError
from .services.scoring_service import score_close_approach


class ScoreCloseApproachTests(TestCase):
    def setUp(self):
        self.neo = NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="(2010 PK9)",
            estimated_diameter_min_km=Decimal("0.200000"),
            estimated_diameter_max_km=Decimal("0.400000"),
            is_potentially_hazardous=True,
        )
        
        self.approach = CloseApproach.objects.create(
            near_earth_object=self.neo,
            close_approach_date=date(2026, 8, 10),
            epoch_date_close_approach=1780876800000,
            relative_velocity_kps=Decimal("15.000000"),
            miss_distance_km=Decimal("10000000.000"),
            orbiting_body="Earth",
        )
        
    def test_score_close_approach_creates_astral_score(self):
        response_payload = {
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
            return httpx.Response(
                200,
                json=response_payload,
                request=request,
            )
        
        client = httpx.Client(transport=httpx.MockTransport(handler))
        
        score, created = score_close_approach(
            self.approach,
            client=client,
        )
        
        self.assertTrue(created)
        self.assertEqual(score.close_approach, self.approach)
        self.assertEqual(score.score, 81)
        self.assertEqual(score.model_version, "APS-v1")
        self.assertEqual(AstralScore.objects.count(), 1)
        
    def test_score_close_approach_updates_existing_model_version(self):
        first_response_payload = {
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
        
        second_response_payload = {
            "score": 68,
            "category": "High Interest",
            "modelVersion": "APS-v1",
            "factors": {
                "diameter": 21,
                "distance": 15,
                "velocity": 12,
                "timing": 5,
                "hazardFlag": 15,
            },
            "explanation": "Updated APS-v1 scoring result."
        }
        
        def first_handler(request):
            return httpx.Response(
                200,
                json=first_response_payload,
                request=request,
            )
        
        first_client = httpx.Client(transport=httpx.MockTransport(first_handler))
        
        def second_handler(request):
            return httpx.Response(
                200,
                json=second_response_payload,
                request=request,
            )
        
        second_client = httpx.Client(transport=httpx.MockTransport(second_handler))
        
        first_score, first_created = score_close_approach(
            self.approach,
            client=first_client
        )
        
        second_score, second_created = score_close_approach (
            self.approach,
            client=second_client
            )
        
        
        self.assertTrue(first_created)
        
        self.assertFalse(second_created)
        
        self.assertEqual(
            first_score.id,
            second_score.id,
        )
        
        self.assertEqual(AstralScore.objects.count(), 1)
        
        self.assertEqual(
            second_score.score,
            68
        )
        
        self.assertEqual(
            second_score.category,
            "High Interest"
        )
        
    def test_score_close_approach_does_not_save_when_service_fails(self):
        def handler(request):
            return httpx.Response(
                500,
                request=request,
            )
        
        client = httpx.Client(transport=httpx.MockTransport(handler))
        
        with self.assertRaises(ScoringClientError):         
            score_close_approach(
                self.approach,
                client=client,
            )

        self.assertEqual(
            AstralScore.objects.count(),
            0
        )
        
    def test_score_close_approach_does_not_save_invalid_response(self):
      response_payload = {
          "score": 80,
          "category": "Critical Review",
          "modelVersion": "APS-v1",
          "factors": {
              "diameter": 21,
              "distance": 21,
              "velocity": 12,
              "timing": 12,
              "hazardFlag": 15,
          },
          "explanation": "Invalid response with mismatched total.",
      }

      def handler(request):
          return httpx.Response(
              200,
              json=response_payload,
              request=request,
          )

      client = httpx.Client(transport=httpx.MockTransport(handler))

      with self.assertRaises(ScoringResponseError):
          score_close_approach(
              self.approach,
              client=client,
          )

      self.assertEqual(
          AstralScore.objects.count(),
          0,
      )
      
    def test_score_close_approach_creates_new_row_for_new_model_version(self):
      first_response_payload = {
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
          "explanation": "APS-v1 scoring result.",
      }

      second_response_payload = {
          "score": 81,
          "category": "Critical Review",
          "modelVersion": "APS-v2",
          "factors": {
              "diameter": 21,
              "distance": 21,
              "velocity": 12,
              "timing": 12,
              "hazardFlag": 15,
          },
          "explanation": "APS-v2 scoring result.",
      }

      def first_handler(request):
          return httpx.Response(
              200,
              json=first_response_payload,
              request=request,
          )

      def second_handler(request):
          return httpx.Response(
              200,
              json=second_response_payload,
              request=request,
          )

      first_client = httpx.Client(
          transport=httpx.MockTransport(first_handler)
      )
      second_client = httpx.Client(
          transport=httpx.MockTransport(second_handler)
      )

      first_score, first_created = score_close_approach(
          self.approach,
          client=first_client,
      )
      second_score, second_created = score_close_approach(
          self.approach,
          client=second_client,
      )

      self.assertTrue(first_created)
      self.assertTrue(second_created)
      self.assertNotEqual(first_score.id, second_score.id)
      self.assertEqual(first_score.model_version, "APS-v1")
      self.assertEqual(second_score.model_version, "APS-v2")
      self.assertEqual(AstralScore.objects.count(), 2)

    def test_score_close_approach_does_not_request_or_save_missing_data(self):
      self.neo.estimated_diameter_min_km = None

      def handler(request):
          self.fail("Scoring service should not be called")

      client = httpx.Client(transport=httpx.MockTransport(handler))

      with self.assertRaises(ScoringPayloadError):
          score_close_approach(
              self.approach,
              client=client,
          )

      self.assertEqual(
          AstralScore.objects.count(),
          0,
      )