from datetime import date
from decimal import Decimal

from django.test import TestCase

from .models import CloseApproach, NearEarthObject
from .services.scoring_payload import (
    ScoringPayloadError, 
    build_score_payload,
)


class ScoringPayloadTests(TestCase):
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
        
    def test_build_score_payload_maps_close_approach_data(self):
        result = build_score_payload(self.approach)
        
        self.assertEqual(
            result,
            {
                "estimatedDiameterMinKm": 0.2,
                "estimatedDiameterMaxKm": 0.4,
                "missDistanceKm": 10_000_000.0,
                "relativeVelocityKps": 15.0,
                "isPotentiallyHazardous": True,
                "closeApproachDate": "2026-08-10",
            },
        )
        
    def test_build_score_payload_rejects_missing_minimum_diameter(self):
        self.neo.estimated_diameter_min_km = None
          
        with self.assertRaises(ScoringPayloadError) as context:
            build_score_payload(self.approach)
            
        self.assertIn(
            "estimated_diameter_min_km",
            str(context.exception),
        )
        
    def test_build_score_payload_rejects_missing_maximum_diameter(self):
        self.neo.estimated_diameter_max_km = None
          
        with self.assertRaises(ScoringPayloadError) as context:
            build_score_payload(self.approach)
            
        self.assertIn(
            "estimated_diameter_max_km",
            str(context.exception),
        )
        
    def test_build_score_payload_rejects_missing_miss_distance(self):
        self.approach.miss_distance_km = None
          
        with self.assertRaises(ScoringPayloadError) as context:
            build_score_payload(self.approach)
            
        self.assertIn(
            "miss_distance_km",
            str(context.exception),
        )
        
    def test_build_score_payload_rejects_missing_relative_velocity(self):
        self.approach.relative_velocity_kps = None
          
        with self.assertRaises(ScoringPayloadError) as context:
            build_score_payload(self.approach)
            
        self.assertIn(
            "relative_velocity_kps",
            str(context.exception),
        )
        
    def test_build_score_payload_allows_zero_miss_distance(self):
        self.approach.miss_distance_km = Decimal("0")
          
        payload = build_score_payload(self.approach)
            
        self.assertEqual(
            payload["missDistanceKm"],
            0.0,
        )