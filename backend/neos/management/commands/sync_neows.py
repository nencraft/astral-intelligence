from datetime import date

from django.core.management.base import BaseCommand, CommandError

from neos.services.neows_client import fetch_neows_feed
from neos.services.neows_normalizer import normalize_feed
from neos.services.neows_upsert import upsert_normalized_feed
from neos.services.sync_logger import (
    mark_sync_failed,
    mark_sync_success,
    start_sync_run,
)


class Command(BaseCommand):
    help = "Sync near-Earth object data from NASA NeoWs Feed."

    def add_arguments(self, parser):
        parser.add_argument("--start-date", required=True)
        parser.add_argument("--end-date", required=True)

    def handle(self, *args, **options):
        start_date = self.parse_date(options["start_date"], "--start-date")
        end_date = self.parse_date(options["end_date"], "--end-date")

        if end_date < start_date:
            raise CommandError("--end-date must be on or after --start-date")

        sync_run = start_sync_run(
            source="NASA NeoWs Feed",
            start_date=start_date,
            end_date=end_date,
        )

        try:
            raw_payload = fetch_neows_feed(start_date, end_date)
            normalized_objects = normalize_feed(raw_payload)
            upsert_result = upsert_normalized_feed(normalized_objects)

            mark_sync_success(
                sync_run,
                upsert_result,
                records_requested=len(normalized_objects),
            )

        except Exception as exc:
            mark_sync_failed(sync_run, str(exc))
            raise CommandError(f"NeoWs sync failed: {exc}") from exc

        self.stdout.write(
            self.style.SUCCESS("NeoWs sync completed successfully")
        )
        
    def parse_date(self, value, option_name):
        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise CommandError(
                f"{option_name} must use YYYY-MM-DD format"
            ) from exc
        
    