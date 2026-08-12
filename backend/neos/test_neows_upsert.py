from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from .models import CloseApproach, NearEarthObject
from .services.neows_upsert import (
    upsert_normalized_feed,
    upsert_normalized_object,
)


class UpsertNormalizedObjectTests(TestCase):
    def test_upsert_normalized_object_creates_neo_and_close_approach(self):
        synced_at = timezone.now()
        normalized_object = {
            "neo": {
                "nasa_jpl_id": "3542519",
                "name": "(2010 PK9)",
                "absolute_magnitude_h": Decimal("21.5"),
                "estimated_diameter_min_km": Decimal("0.12"),
                "estimated_diameter_max_km": Decimal("0.27"),
                "is_potentially_hazardous": False,
            },
            "close_approaches": [
                {
                    "close_approach_date": date(2026, 6, 8),
                    "epoch_date_close_approach": 1780876800000,
                    "relative_velocity_kps": Decimal("15.250000"),
                    "miss_distance_km": Decimal("7500000.123"),
                    "orbiting_body": "Earth",
                }
            ],
        }

        result = upsert_normalized_object(
            normalized_object,
            synced_at=synced_at,
        )

        self.assertEqual(NearEarthObject.objects.count(), 1)
        self.assertEqual(CloseApproach.objects.count(), 1)

        neo = NearEarthObject.objects.get(nasa_jpl_id="3542519")
        self.assertEqual(neo.name, "(2010 PK9)")
        self.assertEqual(neo.absolute_magnitude_h, Decimal("21.5"))
        self.assertEqual(neo.last_synced_at, synced_at)

        approach = CloseApproach.objects.get()
        self.assertEqual(approach.near_earth_object, neo)
        self.assertEqual(approach.close_approach_date, date(2026, 6, 8))
        self.assertEqual(
            approach.epoch_date_close_approach,
            1780876800000,
        )

        self.assertEqual(result.objects_created, 1)
        self.assertEqual(result.objects_updated, 0)
        self.assertEqual(result.approaches_created, 1)
        self.assertEqual(result.approaches_updated, 0)

    def test_upsert_normalized_object_updates_existing_neo(self):
        existing_neo = NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="Old name",
            absolute_magnitude_h=Decimal("22.0"),
            estimated_diameter_min_km=Decimal("0.10"),
            estimated_diameter_max_km=Decimal("0.20"),
            is_potentially_hazardous=True,
        )
        synced_at = timezone.now()
        normalized_object = {
            "neo": {
                "nasa_jpl_id": "3542519",
                "name": "(2010 PK9)",
                "absolute_magnitude_h": Decimal("21.5"),
                "estimated_diameter_min_km": Decimal("0.12"),
                "estimated_diameter_max_km": Decimal("0.27"),
                "is_potentially_hazardous": False,
            },
            "close_approaches": [],
        }

        result = upsert_normalized_object(
            normalized_object,
            synced_at=synced_at,
        )

        self.assertEqual(NearEarthObject.objects.count(), 1)

        existing_neo.refresh_from_db()
        self.assertEqual(existing_neo.name, "(2010 PK9)")
        self.assertEqual(existing_neo.absolute_magnitude_h, Decimal("21.5"))
        self.assertEqual(existing_neo.estimated_diameter_min_km, Decimal("0.12"))
        self.assertEqual(existing_neo.estimated_diameter_max_km, Decimal("0.27"))
        self.assertFalse(existing_neo.is_potentially_hazardous)
        self.assertEqual(existing_neo.last_synced_at, synced_at)

        self.assertEqual(result.objects_created, 0)
        self.assertEqual(result.objects_updated, 1)
        self.assertEqual(result.approaches_created, 0)
        self.assertEqual(result.approaches_updated, 0)

    def test_upsert_normalized_object_updates_existing_close_approach(self):
        neo = NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="(2010 PK9)",
            is_potentially_hazardous=False,
        )
        existing_approach = CloseApproach.objects.create(
            near_earth_object=neo,
            close_approach_date=date(2026, 6, 8),
            epoch_date_close_approach=1780876800000,
            relative_velocity_kps=Decimal("10.000000"),
            miss_distance_km=Decimal("8000000.000"),
            orbiting_body="Earth",
        )
        normalized_object = {
            "neo": {
                "nasa_jpl_id": "3542519",
                "name": "(2010 PK9)",
                "absolute_magnitude_h": Decimal("21.5"),
                "estimated_diameter_min_km": Decimal("0.12"),
                "estimated_diameter_max_km": Decimal("0.27"),
                "is_potentially_hazardous": False,
            },
            "close_approaches": [
                {
                    "close_approach_date": date(2026, 6, 8),
                    "epoch_date_close_approach": 1780876800000,
                    "relative_velocity_kps": Decimal("15.250000"),
                    "miss_distance_km": Decimal("7500000.123"),
                    "orbiting_body": "Earth",
                }
            ],
        }

        result = upsert_normalized_object(normalized_object)

        self.assertEqual(CloseApproach.objects.count(), 1)

        existing_approach.refresh_from_db()
        self.assertEqual(
            existing_approach.relative_velocity_kps,
            Decimal("15.250000"),
        )
        self.assertEqual(
            existing_approach.miss_distance_km,
            Decimal("7500000.123"),
        )

        self.assertEqual(result.objects_created, 0)
        self.assertEqual(result.objects_updated, 1)
        self.assertEqual(result.approaches_created, 0)
        self.assertEqual(result.approaches_updated, 1)

    def test_upsert_normalized_object_allows_multiple_close_approaches_for_same_neo(self):
        normalized_object = {
            "neo": {
                "nasa_jpl_id": "3542519",
                "name": "(2010 PK9)",
                "absolute_magnitude_h": Decimal("21.5"),
                "estimated_diameter_min_km": Decimal("0.12"),
                "estimated_diameter_max_km": Decimal("0.27"),
                "is_potentially_hazardous": False,
            },
            "close_approaches": [
                {
                    "close_approach_date": date(2026, 6, 8),
                    "epoch_date_close_approach": 1780876800000,
                    "relative_velocity_kps": Decimal("15.250000"),
                    "miss_distance_km": Decimal("7500000.123"),
                    "orbiting_body": "Earth",
                },
                {
                    "close_approach_date": date(2026, 7, 1),
                    "epoch_date_close_approach": 1782864000000,
                    "relative_velocity_kps": Decimal("16.500000"),
                    "miss_distance_km": Decimal("6500000.456"),
                    "orbiting_body": "Earth",
                },
            ],
        }

        result = upsert_normalized_object(normalized_object)

        self.assertEqual(NearEarthObject.objects.count(), 1)
        self.assertEqual(CloseApproach.objects.count(), 2)

        neo = NearEarthObject.objects.get(nasa_jpl_id="3542519")
        approach_epochs = set(
            neo.close_approaches.values_list(
                "epoch_date_close_approach",
                flat=True,
            )
        )

        self.assertEqual(
            approach_epochs,
            {1780876800000, 1782864000000},
        )
        self.assertEqual(result.objects_created, 1)
        self.assertEqual(result.objects_updated, 0)
        self.assertEqual(result.approaches_created, 2)
        self.assertEqual(result.approaches_updated, 0)

    def test_upsert_normalized_object_requires_potentially_hazardous_flag(self):
        normalized_object = {
            "neo": {
                "nasa_jpl_id": "3542519",
                "name": "(2010 PK9)",
                "absolute_magnitude_h": Decimal("21.5"),
                "estimated_diameter_min_km": Decimal("0.12"),
                "estimated_diameter_max_km": Decimal("0.27"),
            },
            "close_approaches": [],
        }

        with self.assertRaises(KeyError) as context:
            upsert_normalized_object(normalized_object)

        self.assertEqual(
            context.exception.args[0],
            "is_potentially_hazardous",
        )


class UpsertNormalizedFeedTests(TestCase):

    def test_upsert_normalized_feed_combines_counts_for_multiple_objects(self):
        normalized_objects = [
            {
                "neo": {
                    "nasa_jpl_id": "3542519",
                    "name": "(2010 PK9)",
                    "absolute_magnitude_h": Decimal("21.5"),
                    "estimated_diameter_min_km": Decimal("0.12"),
                    "estimated_diameter_max_km": Decimal("0.27"),
                    "is_potentially_hazardous": False,
                },
                "close_approaches": [
                    {
                        "close_approach_date": date(2026, 6, 8),
                        "epoch_date_close_approach": 1780876800000,
                        "relative_velocity_kps": Decimal("15.250000"),
                        "miss_distance_km": Decimal("7500000.123"),
                        "orbiting_body": "Earth",
                    }
                ],
            },
            {
                "neo": {
                    "nasa_jpl_id": "3012398",
                    "name": "433 Eros",
                    "absolute_magnitude_h": Decimal("10.4"),
                    "estimated_diameter_min_km": Decimal("16.840000"),
                    "estimated_diameter_max_km": Decimal("37.660000"),
                    "is_potentially_hazardous": False,
                },
                "close_approaches": [
                    {
                        "close_approach_date": date(2026, 6, 9),
                        "epoch_date_close_approach": 1780963200000,
                        "relative_velocity_kps": Decimal("5.820000"),
                        "miss_distance_km": Decimal("22000000.000"),
                        "orbiting_body": "Earth",
                    }
                ],
            },
        ]

        result = upsert_normalized_feed(normalized_objects)

        self.assertEqual(NearEarthObject.objects.count(), 2)
        self.assertEqual(CloseApproach.objects.count(), 2)
        self.assertEqual(result.objects_created, 2)
        self.assertEqual(result.objects_updated, 0)
        self.assertEqual(result.approaches_created, 2)
        self.assertEqual(result.approaches_updated, 0)