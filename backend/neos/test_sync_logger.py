from datetime import date

from django.test import TestCase

from .models import ApiSyncRun
from .services.neows_upsert import UpsertResult
from .services.sync_logger import  (
    mark_sync_success,
    mark_sync_failed,
    start_sync_run,
)


class SyncLoggerTests(TestCase):
    def test_start_sync_run_creates_started_sync_record(self):
        sync_run = start_sync_run(
            source="NASA NeoWs Feed",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 7),
        )

        self.assertEqual(ApiSyncRun.objects.count(), 1)
        self.assertEqual(sync_run.source, "NASA NeoWs Feed")
        self.assertEqual(sync_run.status, ApiSyncRun.Status.STARTED)
        self.assertEqual(sync_run.start_date, date(2026, 6, 1))
        self.assertEqual(sync_run.end_date, date(2026, 6, 7))
        self.assertIsNone(sync_run.finished_at)


    def test_mark_sync_success_updates_sync_record_with_counts(self):
        sync_run = start_sync_run(
            source="NASA NeoWs Feed",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 7),
        )
        upsert_result = UpsertResult(
            objects_created=2,
            objects_updated=1,
            approaches_created=3,
            approaches_updated=4,
        )

        mark_sync_success(
            sync_run,
            upsert_result,
            records_requested=10,
        )

        sync_run.refresh_from_db()
        self.assertEqual(sync_run.status, ApiSyncRun.Status.SUCCESS)
        self.assertIsNotNone(sync_run.finished_at)
        self.assertEqual(sync_run.records_requested, 10)
        self.assertEqual(sync_run.records_created, 5)
        self.assertEqual(sync_run.records_updated, 5)
        self.assertEqual(sync_run.records_skipped, 0)


    def test_mark_sync_failed_updates_sync_record_with_error_message(self):
        sync_run = start_sync_run(
            source="NASA NeoWs Feed",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 7),
        )

        mark_sync_failed(sync_run, "NASA API request failed")

        sync_run.refresh_from_db()
        self.assertEqual(sync_run.status, ApiSyncRun.Status.FAILED)
        self.assertIsNotNone(sync_run.finished_at)
        self.assertEqual(sync_run.error_message, "NASA API request failed")