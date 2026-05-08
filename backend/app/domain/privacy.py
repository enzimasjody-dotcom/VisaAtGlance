from app.domain.models import PrivacyRule, RecordVisibility, TimelineRecord

PERCENTILE_FIELD = "user_percentile"
RECENT_TREND_FIELD = "recent_approval_count"
ROW_LEVEL_FIELD = "row_level_public_preview"


def should_show_percentile(sample_size: int, rule: PrivacyRule) -> bool:
    if not rule.hide_percentile_for_small_cohort:
        return True
    return sample_size >= rule.minimum_percentile_size


def should_show_recent_trend(sample_size: int, rule: PrivacyRule) -> bool:
    if not rule.hide_recent_trend_for_small_cohort:
        return True
    return sample_size >= rule.minimum_recent_trend_size


def can_expose_row_preview(record: TimelineRecord, rule: PrivacyRule) -> bool:
    return rule.allow_row_level_public_preview and record.visibility == RecordVisibility.PUBLIC_PREVIEW


def suppressed_fields_for(sample_size: int, rule: PrivacyRule) -> list[str]:
    fields: list[str] = []
    if not should_show_percentile(sample_size, rule):
        fields.append(PERCENTILE_FIELD)
    if not should_show_recent_trend(sample_size, rule):
        fields.append(RECENT_TREND_FIELD)
    if not rule.allow_row_level_public_preview:
        fields.append(ROW_LEVEL_FIELD)
    return fields
