from django.core.management.base import BaseCommand, CommandError

from ...models import CloseApproach
from ...services.scoring_client import ScoringClientError
from ...services.scoring_payload import ScoringPayloadError
from ...services.scoring_response import ScoringResponseError
from ...services.scoring_service import score_close_approach


class Command(BaseCommand):
    help = "Score one stored close approach."
    
    def add_arguments(self, parser):
        parser.add_argument(
            "--approach-id",
            required=True,
            type=int,
        )
        
    def handle(self, *args, **options):
        approach_id = options["approach_id"]
        
        try:
            approach = (
                CloseApproach.objects
                .select_related("near_earth_object")
                .get(pk=approach_id)
            )
        except CloseApproach.DoesNotExist as exc:
            raise CommandError(
                f"Close approach {approach_id} does not exist."
            ) from exc
            
        try:
            score, created = score_close_approach(approach)
        except (
            ScoringClientError,
            ScoringPayloadError,
            ScoringResponseError,
        ) as exc:
            raise CommandError(f"Scoring failed: {exc}") from exc

        action = "created" if created else "updated"

        self.stdout.write(
            self.style.SUCCESS(
                f"Astral score {action}: {score.score} | "
                f"{score.category} | {score.model_version}"
            )
        )