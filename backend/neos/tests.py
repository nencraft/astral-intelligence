from datetime import date
from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from .models import ApiSyncRun, CloseApproach, NearEarthObject


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

    def test_near_earth_object_can_store_last_synced_at(self):
        synced_at = timezone.now()

        neo = NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="(2010 PK9)",
            last_synced_at=synced_at,
        )

        self.assertEqual(neo.last_synced_at, synced_at)

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
            epoch_date_close_approach=1780012800000,
            orbiting_body="Earth",
        )

        self.assertIn(approach, neo.close_approaches.all())

    def test_duplicate_close_approach_is_rejected(self):
        neo = NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="(2010 PK9)",
        )

        CloseApproach.objects.create(
            near_earth_object=neo,
            close_approach_date=date(2026, 5, 27),
            epoch_date_close_approach=1780012800000,
            orbiting_body="Earth",
        )

        with self.assertRaises(IntegrityError):
            CloseApproach.objects.create(
                near_earth_object=neo,
                close_approach_date=date(2026, 5, 27),
                epoch_date_close_approach=1780012800000,
                orbiting_body="Earth",
            )

    def test_same_neo_can_have_different_close_approach_epochs(self):
        neo = NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="(2010 PK9)",
        )

        first = CloseApproach.objects.create(
            near_earth_object=neo,
            close_approach_date=date(2026, 5, 27),
            epoch_date_close_approach=1780012800000,
            orbiting_body="Earth",
        )
        second = CloseApproach.objects.create(
            near_earth_object=neo,
            close_approach_date=date(2026, 6, 1),
            epoch_date_close_approach=1780444800000,
            orbiting_body="Earth",
        )

        self.assertNotEqual(first.id, second.id)

    def test_same_epoch_is_allowed_for_different_neos(self):
        first_neo = NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="(2010 PK9)",
        )
        second_neo = NearEarthObject.objects.create(
            nasa_jpl_id="3012398",
            name="433 Eros",
        )

        first = CloseApproach.objects.create(
            near_earth_object=first_neo,
            close_approach_date=date(2026, 5, 27),
            epoch_date_close_approach=1780012800000,
            orbiting_body="Earth",
        )
        second = CloseApproach.objects.create(
            near_earth_object=second_neo,
            close_approach_date=date(2026, 5, 27),
            epoch_date_close_approach=1780012800000,
            orbiting_body="Earth",
        )

        self.assertNotEqual(first.id, second.id)

class ApiSyncRunModelTests(TestCase):
    def test_api_sync_run_can_record_success(self):
        sync_run = ApiSyncRun.objects.create(
            source="NASA NeoWs Feed",
            status=ApiSyncRun.Status.SUCCESS,
            start_date=date(2026, 5, 27),
            end_date=date(2026, 5, 29),
            finished_at=timezone.now(),
            records_requested=5,
            records_created=3,
            records_updated=2,
            records_skipped=0,
        )

        self.assertEqual(sync_run.status, ApiSyncRun.Status.SUCCESS)
        self.assertEqual(sync_run.records_requested, 5)
        self.assertEqual(sync_run.records_created, 3)
        self.assertEqual(sync_run.records_updated, 2)

    def test_api_sync_run_can_record_failure_message(self):
        sync_run = ApiSyncRun.objects.create(
            source="NASA NeoWs Feed",
            status=ApiSyncRun.Status.FAILED,
            start_date=date(2026, 5, 27),
            end_date=date(2026, 5, 29),
            finished_at=timezone.now(),
            error_message="NASA API request failed",
        )

        self.assertEqual(sync_run.status, ApiSyncRun.Status.FAILED)
        self.assertEqual(sync_run.error_message, "NASA API request failed")

class NearEarthObjectApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.neo = NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="(2010 PK9)",
            absolute_magnitude_h=Decimal("21.500"),
            estimated_diameter_min_km=Decimal("0.120000"),
            estimated_diameter_max_km=Decimal("0.270000"),
            is_potentially_hazardous=False,
        )

    def test_neo_list_endpoint_returns_neos(self):
        response = self.client.get("/api/neos/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["nasa_jpl_id"], "3542519")
        self.assertEqual(response.data[0]["name"], "(2010 PK9)")

    def test_neo_detail_endpoint_returns_single_neo(self):
        response = self.client.get(f"/api/neos/{self.neo.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.neo.id)
        self.assertEqual(response.data["nasa_jpl_id"], "3542519")


class CloseApproachApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.neo = NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="(2010 PK9)",
        )
        self.approach = CloseApproach.objects.create(
            near_earth_object=self.neo,
            close_approach_date=date(2026, 5, 29),
            epoch_date_close_approach=1780012800000,
            relative_velocity_kps=Decimal("15.250000"),
            miss_distance_km=Decimal("7500000.123"),
            orbiting_body="Earth",
        )

    def test_close_approach_list_endpoint_returns_approaches(self):
        response = self.client.get("/api/approaches/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["near_earth_object"], self.neo.id)
        self.assertEqual(response.data[0]["orbiting_body"], "Earth")

    def test_close_approach_detail_endpoint_returns_single_approach(self):
        response = self.client.get(f"/api/approaches/{self.approach.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.approach.id)
        self.assertEqual(response.data["near_earth_object"], self.neo.id)