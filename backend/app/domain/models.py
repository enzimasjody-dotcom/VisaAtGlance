from datetime import date, datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, HttpUrl, computed_field


class HealthStatus(BaseModel):
    status: str = Field(description="Service status")
    service: str = Field(description="Service name")


class CaseStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    UNKNOWN = "unknown"


class ContributionType(StrEnum):
    SPREADSHEET = "spreadsheet"
    ANONYMOUS_USER = "anonymous_user"
    SAVED_USER = "saved_user"
    OFFICIAL = "official"
    MANUAL = "manual"


class RecordVisibility(StrEnum):
    PRIVATE = "private"
    AGGREGATE_ONLY = "aggregate_only"
    PUBLIC_PREVIEW = "public_preview"


class SourceKind(StrEnum):
    GOOGLE_SHEET = "google_sheet"
    USER_CONTRIBUTION = "user_contribution"
    OFFICIAL = "official"
    MANUAL = "manual"


class TimelineRecord(BaseModel):
    """Normalized I-485 timeline row based on the Apr '26 spreadsheet tab."""

    id: str
    category: str = Field(description="Spreadsheet Category column, such as EB2 NIW or EB3")
    priority_date: date | None = None
    i485_mailed_date: date | None = None
    i485_received_date: date | None = None
    i485_receipt_date: date | None = None
    block_number: str | None = Field(default=None, description="Partial IOE block, not a full receipt number")
    lockbox: str | None = None
    biometric_date: date | None = None
    interview_status: str | None = None
    ead_approval_date: date | None = None
    advanced_parole_approval_date: date | None = None
    field_office_name: str | None = None
    field_office_transfer_date: date | None = None
    fta_updates: str | None = None
    silent_updates_after_biometrics: str | None = None
    gc_approved_date: date | None = None
    gc_received_date: date | None = None
    country_of_concern: str | None = None
    applicant_group: str | None = Field(default=None, description="Spreadsheet Single/Spouse status column")
    comments: str | None = Field(default=None, description="Free-text comments; never expose in public aggregate responses")
    source_id: str | None = None
    contribution_type: ContributionType = ContributionType.SPREADSHEET
    visibility: RecordVisibility = RecordVisibility.AGGREGATE_ONLY
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @computed_field
    @property
    def status(self) -> CaseStatus:
        if self.gc_approved_date is not None:
            return CaseStatus.APPROVED
        return CaseStatus.PENDING

    @property
    def processing_start_date(self) -> date | None:
        return self.i485_received_date or self.i485_receipt_date or self.i485_mailed_date

    @property
    def processing_days(self) -> int | None:
        if self.gc_approved_date is None or self.processing_start_date is None:
            return None
        days = (self.gc_approved_date - self.processing_start_date).days
        return days if days >= 0 else None


class SourceRecord(BaseModel):
    id: str
    source_kind: SourceKind
    title: str
    url: HttpUrl | None = None
    checked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    limitation: str | None = None
    is_official: bool = False


class PrivacyRule(BaseModel):
    id: str = "default-public-aggregate-rule"
    name: str = "Default public aggregate rule"
    minimum_cohort_size: int = 10
    minimum_percentile_size: int = 20
    minimum_recent_trend_size: int = 10
    hide_percentile_for_small_cohort: bool = True
    hide_recent_trend_for_small_cohort: bool = True
    allow_row_level_public_preview: bool = False
    aggregate_only_default: bool = True


class CohortSummary(BaseModel):
    cohort_key: dict[str, str]
    sample_size: int
    average_processing_days: float | None = None
    median_processing_days: float | None = None
    user_percentile: float | None = None
    recent_approval_count: int | None = None
    suppressed_fields: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)
    computed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
