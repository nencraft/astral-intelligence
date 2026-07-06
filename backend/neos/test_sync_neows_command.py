from unittest.mock import Mock, patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase

from .services.neows_upsert import UpsertResult


class SyncNeoWsCommandTests(SimpleTestCase):
    def test_sync_neows_requires_start_date(self):
        with self.assertRaises(CommandError):
            call_command("sync_neows", end_date="2026-06-07")

    def test_sync_neows_requires_end_date(self):
        with self.assertRaises(CommandError):
            call_command("sync_neows", start_date="2026-06-01")

    def test_sync_neows_rejects_invalid_start_date(self):
        with self.assertRaises(CommandError):
            call_command(
                "sync_neows",
                start_date="not-a-date",
                end_date="2026-06-07",
            )

    def test_sync_neows_rejects_invalid_end_date(self):
        with self.assertRaises(CommandError):
            call_command(
                "sync_neows",
                start_date="2026-06-01",
                end_date="not-a-date",
            )

    def test_sync_neows_rejects_end_date_before_start_date(self):
        with self.assertRaises(CommandError):
            call_command(
                "sync_neows",
                start_date="2026-06-07",
                end_date="2026-06-01",
            )

    @patch("neos.management.commands.sync_neows.mark_sync_success")
    @patch("neos.management.commands.sync_neows.upsert_normalized_feed")
    @patch("neos.management.commands.sync_neows.normalize_feed")
    @patch("neos.management.commands.sync_neows.fetch_neows_feed")
    @patch("neos.management.commands.sync_neows.start_sync_run")
    def test_sync_neows_orchestrates_successful_sync(
        self,
        mock_start_sync_run,
        mock_fetch_neows_feed,
        mock_normalize_feed,
        mock_upsert_normalized_feed,
        mock_mark_sync_success,
    ):
        sync_run = Mock()
        raw_payload = {"near_earth_objects": {}}
        normalized_objects = [{"neo": {}, "close_approaches": []}]
        upsert_result = UpsertResult(
            objects_created=1,
            approaches_created=1,
        )

        mock_start_sync_run.return_value = sync_run
        mock_fetch_neows_feed.return_value = raw_payload
        mock_normalize_feed.return_value = normalized_objects
        mock_upsert_normalized_feed.return_value = upsert_result

        call_command(
            "sync_neows",
            start_date="2026-06-01",
            end_date="2026-06-07",
        )

        mock_start_sync_run.assert_called_once()
        mock_fetch_neows_feed.assert_called_once()
        mock_normalize_feed.assert_called_once_with(raw_payload)
        mock_upsert_normalized_feed.assert_called_once_with(
            normalized_objects
        )
        mock_mark_sync_success.assert_called_once_with(
            sync_run,
            upsert_result,
            records_requested=1,
        )
        
    @patch("neos.management.commands.sync_neows.mark_sync_failed")
    @patch("neos.management.commands.sync_neows.fetch_neows_feed")
    @patch("neos.management.commands.sync_neows.start_sync_run")
    def test_sync_neows_marks_sync_failed_when_service_fails(
        self,
        mock_start_sync_run,
        mock_fetch_neows_feed,
        mock_mark_sync_failed,
    ):
        sync_run = Mock()
        mock_start_sync_run.return_value = sync_run
        mock_fetch_neows_feed.side_effect = RuntimeError(
            "NASA request failed"
        )

        with self.assertRaises(CommandError):
            call_command(
                "sync_neows",
                start_date="2026-06-01",
                end_date="2026-06-07",
            )

        mock_mark_sync_failed.assert_called_once_with(
            sync_run,
            "NASA request failed",
        )