from datetime import date, datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, HttpUrl, computed_field


class HealthStatus(BaseModel):
    status: str = Field(description="Service status")
    service: str = Field(description="Service name")


class CaseStatus(StrEnum):
    FILED = "filed"
    PENDING_BIO = "pending_bio"
    BIOMETRICS_DONE = "biometrics_done"
    EAD_APPROVED = "ead_approved"
    INTERVIEW = "interview"
    APPROVED = "approved"
    RECEIVED = "received"
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
    """Normalized I-485 timeline record inspired by the i485tracker case shape."""

    id: str
    pd: date | None = Field(default=None, description="I-140 priority date")
    cat: str = Field(description="Visa category, such as EB2 NIW or EB3")
    filed: date | None = Field(default=None, description="I-485 filed or received date")
    receipt: date | None = Field(default=None, description="I-485 receipt notice date")
    receipt_block: str | None = Field(default=None, description="Partial receipt block only; never store full receipt number")
    bio: date | None = Field(default=None, description="Biometrics date")
    ead: date | None = Field(default=None, description="EAD approval date")
    ap: date | None = Field(default=None, description="Advance Parole approval date")
    field_office: str | None = None
    fo_transfer_date: date | None = None
    silent: list[date] = Field(default_factory=list)
    gc_approved: date | None = None
    gc_received: date | None = None
    interview: date | None = None
    coc: str | None = Field(default="None", description="Country of concern marker, if voluntarily provided")
    rfe: str | None = Field(default="None", description="RFE status")
    region: str | None = Field(default=None, description="ROW or NROW when derivable")
    applicant_group: str | None = Field(default=None, description="Single, spouse, kids grouping when derivable")
    notes: str | None = Field(default=None, description="Free-text notes; never expose in public aggregate responses")
    last_updated: date | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    has_password: bool = False
    source_id: str | None = None
    contribution_type: ContributionType = ContributionType.SPREADSHEET
    visibility: RecordVisibility = RecordVisibility.AGGREGATE_ONLY

    @computed_field
    @property
    def status(self) -> CaseStatus:
        if self.gc_received is not None:
            return CaseStatus.RECEIVED
        if self.gc_approved is not None:
            return CaseStatus.APPROVED
        if self.interview is not None:
            return CaseStatus.INTERVIEW
        if self.ead is not None:
            return CaseStatus.EAD_APPROVED
        if self.bio is not None:
            return CaseStatus.BIOMETRICS_DONE
        if self.receipt is not None:
            return CaseStatus.PENDING_BIO
        if self.filed is not None:
            return CaseStatus.FILED
        return CaseStatus.UNKNOWN

    @property
    def processing_start_date(self) -> date | None:
        return self.filed or self.receipt

    @property
    def processing_days(self) -> int | None:
        if self.gc_approved is None or self.processing_start_date is None:
            return None
        days = (self.gc_approved - self.processing_start_date).days
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
