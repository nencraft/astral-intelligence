from datetime import date
from decimal import Decimal

from django.test import SimpleTestCase

from .services.neows_normalizer import (
      NeoWsNormalizationError,
      normalize_feed,
  )

class NormalizeFeedTests(SimpleTestCase):
    def test_normalize_feed_maps_neo_and_close_approach_fields(self):
        payload = {
            "element_count": 1,
            "near_earth_objects": {
                "2026-06-08": [
                    {
                        "id": "3542519",
                        "name": "(2010 PK9)",
                        "absolute_magnitude_h": 21.5,
                        "estimated_diameter": {
                            "kilometers": {
                                "estimated_diameter_min": 0.12,
                                "estimated_diameter_max": 0.27,
                            }
                        },
                        "is_potentially_hazardous_asteroid": False,
                        "close_approach_data": [
                            {
                                "close_approach_date": "2026-06-08",
                                "epoch_date_close_approach": 1780876800000,
                                "relative_velocity": {
                                    "kilometers_per_second": "15.250000"
                                },
                                "miss_distance": {
                                    "kilometers": "7500000.123"
                                },
                                "orbiting_body": "Earth",
                            }
                        ],
                    }
                ]
            },
        }

        result = normalize_feed(payload)

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0]["neo"],
            {
                "nasa_jpl_id": "3542519",
                "name": "(2010 PK9)",
                "absolute_magnitude_h": Decimal("21.5"),
                "estimated_diameter_min_km": Decimal("0.12"),
                "estimated_diameter_max_km": Decimal("0.27"),
                "is_potentially_hazardous": False,
            },
        )
        self.assertEqual(
            result[0]["close_approaches"],
            [
                {
                    "close_approach_date": date(2026, 6, 8),
                    "epoch_date_close_approach": 1780876800000,
                    "relative_velocity_kps": Decimal("15.250000"),
                    "miss_distance_km": Decimal("7500000.123"),
                    "orbiting_body": "Earth",
                }
            ],
        )


    def test_normalize_feed_uses_none_for_missing_optional_measurements(self):
        payload = {
            "element_count": 1,
            "near_earth_objects": {
                "2026-06-08": [
                    {
                        "id": "3542519",
                        "name": "(2010 PK9)",
                        "is_potentially_hazardous_asteroid": False,
                        "close_approach_data": [
                            {
                                "close_approach_date": "2026-06-08",
                                "epoch_date_close_approach": 1780876800000,
                                "orbiting_body": "Earth",
                            }
                        ],
                    }
                ]
            },
        }

        result = normalize_feed(payload)

        self.assertIsNone(result[0]["neo"]["absolute_magnitude_h"])
        self.assertIsNone(result[0]["neo"]["estimated_diameter_min_km"])
        self.assertIsNone(result[0]["neo"]["estimated_diameter_max_km"])
        self.assertIsNone(
            result[0]["close_approaches"][0]["relative_velocity_kps"]
        )
        self.assertIsNone(
            result[0]["close_approaches"][0]["miss_distance_km"]
        )

    def test_normalize_feed_requires_nasa_id(self):
        payload = {
            "near_earth_objects": {
                "2026-06-08": [
                    {
                        "name": "(2010 PK9)",
                        "close_approach_data": [],
                    }
                ]
            },
        }

        with self.assertRaises(NeoWsNormalizationError):
            normalize_feed(payload)

    def test_normalize_feed_requires_name(self):
        payload = {
            "near_earth_objects": {
                "2026-06-08": [
                    {
                        "id": "3542519",
                        "close_approach_data": [],
                    }
                ]
            },
        }

        with self.assertRaises(NeoWsNormalizationError):
            normalize_feed(payload)

    def test_normalize_feed_requires_close_approach_identity_fields(self):
        payload = {
            "near_earth_objects": {
                "2026-06-08": [
                    {
                        "id": "3542519",
                        "name": "(2010 PK9)",
                        "close_approach_data": [
                            {
                                "close_approach_date": "2026-06-08",
                                "orbiting_body": "Earth",
                            }
                        ],
                    }
                ]
            },
        }

        with self.assertRaises(NeoWsNormalizationError):
            normalize_feed(payload)

    def test_normalize_feed_requires_potentially_hazardous_flag(self):
        payload = {
            "near_earth_objects": {
                "2026-06-08": [
                    {
                        "id": "3542519",
                        "name": "(2010 PK9)",
                        "close_approach_data": [],
                    }
                ]
            },
        }

        with self.assertRaisesRegex(
            NeoWsNormalizationError,
            "is_potentially_hazardous_asteroid",
        ):
            normalize_feed(payload)
