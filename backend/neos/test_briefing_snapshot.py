import json
from datetime import date
from decimal import Decimal

from django.test import TestCase

from .models import AstralScore, CloseApproach, NearEarthObject
from .services.briefing_snapshot import (
    build_briefing_snapshot,
    build_data_caveats,
)


class BriefingSnapshotTests(TestCase):
    def setUp(self):
        self.neo = NearEarthObject.objects.create(
            nasa_jpl_id="3542519",
            name="(2010 PK9)",
            is_potentially_hazardous=False,
            absolute_magnitude_h=Decimal("21.500"),
            estimated_diameter_min_km=Decimal("0.200000"),
            estimated_diameter_max_km=Decimal("0.400000"),
        )
        self.approach = CloseApproach.objects.create(
            near_earth_object=self.neo,
            close_approach_date=date(2026, 5, 29),
            epoch_date_close_approach=1780012800000,
            relative_velocity_kps=Decimal("15.250000"),
            miss_distance_km=Decimal("7500000.123"),
            orbiting_body="Earth",
        )
        self.astral_score = AstralScore.objects.create(
            close_approach=self.approach,
            score=81,
            category=AstralScore.Category.CRITICAL_REVIEW,
            model_version="APS-v1",
            diameter_factor=21,
            distance_factor=21,
            velocity_factor=12,
            timing_factor=12,
            hazard_flag_factor=15,
            explanation="This is a test explanation.",
        )

    def test_build_briefing_snapshot(self):
        briefing_snapshot = build_briefing_snapshot(self.astral_score)

        self.assertEqual(briefing_snapshot["snapshot_version"], "briefing-source-v1")
        self.assertEqual(
            briefing_snapshot["near_earth_object"]["nasa_jpl_id"], "3542519"
        )
        self.assertEqual(
            briefing_snapshot["close_approach"]["close_approach_date"], "2026-05-29"
        )
        self.assertEqual(briefing_snapshot["astral_score"]["score"], 81)
        json.dumps(briefing_snapshot)

    def test_build_briefing_snapshot_preserves_missing_optional_values(self):
        self.neo.absolute_magnitude_h = None
        self.neo.save(update_fields=["absolute_magnitude_h"])

        briefing_snapshot = build_briefing_snapshot(self.astral_score)

        self.assertIsNone(
            briefing_snapshot["near_earth_object"]["absolute_magnitude_h"]
        )

        json.dumps(briefing_snapshot)

    def test_build_data_caveats_includes_standard_limitations(self):
        snapshot = build_briefing_snapshot(self.astral_score)

        caveats = build_data_caveats(snapshot)

        self.assertIn(
            "Estimated diameter values represent a range, not an exact diameter.",
            caveats,
        )
        self.assertIn(
            (
                "The Astral score is a project-specific review-priority metric,"
                " not an official NASA collision probability."
            ),
            caveats,
        )
        self.assertEqual(len(caveats), 2)

    def test_build_data_caveats_reports_missing_absolute_magnitude(self):
        self.neo.absolute_magnitude_h = None

        snapshot = build_briefing_snapshot(self.astral_score)

        caveats = build_data_caveats(snapshot)

        self.assertIn("The absolute magnitude was unavailable.", caveats)
        self.assertEqual(len(caveats), 3)
