from datetime import date
from decimal import Decimal
from io import StringIO
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from .models import CloseApproach, NearEarthObject
from .services.scoring_client import ScoringClientError


class ScoreApproachCommandTests(TestCase):
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

    def test_score_approach_requires_approach_id(self):
        with self.assertRaises(CommandError):
            call_command("score_approach")

    def test_score_approach_rejects_missing_approach(self):
        with self.assertRaises(CommandError):
            call_command(
                "score_approach",
                approach_id=999999,
            )

    @patch("neos.management.commands.score_approach.score_close_approach")
    def test_score_approach_calls_service_and_reports_created_score(
        self,
        mock_score_close_approach,
    ):
        mock_score = Mock(
            score=81,
            category="Critical Review",
            model_version="APS-v1",
        )
        mock_score_close_approach.return_value = (
            mock_score,
            True,
        )
        stdout = StringIO()

        call_command(
            "score_approach",
            approach_id=self.approach.id,
            stdout=stdout,
        )

        mock_score_close_approach.assert_called_once()

        called_approach = mock_score_close_approach.call_args.args[0]

        self.assertEqual(
            called_approach.id,
            self.approach.id,
        )

        output = stdout.getvalue()

        self.assertIn("created", output)
        self.assertIn("81", output)
        self.assertIn("Critical Review", output)
        self.assertIn("APS-v1", output)

    @patch("neos.management.commands.score_approach.score_close_approach")
    def test_score_approach_translates_scoring_failure_to_command_error(
        self,
        mock_score_close_approach,
    ):
        mock_score_close_approach.side_effect = ScoringClientError(
            "Scoring service request failed"
        )

        with self.assertRaises(CommandError) as context:
            call_command(
                "score_approach",
                approach_id=self.approach.id,
            )

        self.assertIn(
            "Scoring failed",
            str(context.exception),
        )
        mock_score_close_approach.assert_called_once()