from django.utils import timezone

from neos.models import ApiSyncRun


def start_sync_run(source, start_date, end_date):
    return ApiSyncRun.objects.create(
        source=source,
        status=ApiSyncRun.Status.STARTED,
        start_date=start_date,
        end_date=end_date,
    )


def mark_sync_success(sync_run, upsert_result, records_requested=0):
    sync_run.status = ApiSyncRun.Status.SUCCESS
    sync_run.finished_at = timezone.now()
    sync_run.records_requested = records_requested
    sync_run.records_created = (
        upsert_result.objects_created + upsert_result.approaches_created
    )
    sync_run.records_updated = (
        upsert_result.objects_updated + upsert_result.approaches_updated
    )
    sync_run.records_skipped = 0
    sync_run.error_message = ""
    sync_run.save()

    return sync_run


def mark_sync_failed(sync_run, error_message):
    sync_run.status = ApiSyncRun.Status.FAILED
    sync_run.finished_at = timezone.now()
    sync_run.error_message = error_message
    sync_run.save()

    return sync_run