from datetime import date
from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from .models import CloseApproach, NearEarthObject

class NearEarthObjectModelTests(TestCase):
    def test_near_earth_object_can_be_created(self):
        neo = NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="(2010 PK9)",
            absolute_magnitude_h=Decimal("21.500"),
            estimated_diameter_min_km=Decimal("0.120000"),
            estimated_diameter_max_km=Decimal("0.270000"),
            is_potentially_hazardous=False,
        )

        self.assertEqual(neo.nasa_jpl_id, "3542519")
        self.assertEqual(neo.name, "(2010 PK9)")
        self.assertEqual(str(neo), "(2010 PK9)")
        self.assertFalse(neo.is_potentially_hazardous)

    def test_nasa_jpl_id_must_be_unique(self):
        NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="(2010 PK9)",
        )

        with self.assertRaises(IntegrityError):
            NearEarthObject.objects.create(
                nasa_jpl_id="3542519",
                name="Duplicate object",
            )

class CloseApproachModelTests(TestCase):
    def test_close_approach_can_be_created_for_neo(self):
        neo = NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="(2010 PK9)",
        )

        approach = CloseApproach.objects.create(
            near_earth_object=neo,
            close_approach_date=date(2026, 5, 27),
            epoch_date_close_approach=1780012800000,
            relative_velocity_kps=Decimal("15.250000"),
            miss_distance_km=Decimal("7500000.123"),
            orbiting_body="Earth",
        )

        self.assertEqual(approach.near_earth_object, neo)
        self.assertEqual(approach.close_approach_date, date(2026, 5, 27))
        self.assertEqual(str(approach), "(2010 PK9) - 2026-05-27")

    def test_neo_can_access_related_close_approaches(self):
        neo = NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="(2010 PK9)",
        )

        approach = CloseApproach.objects.create(
            near_earth_object=neo,
            close_approach_date=date(2026, 5, 27),
        )

        self.assertIn(approach, neo.close_approaches.all())