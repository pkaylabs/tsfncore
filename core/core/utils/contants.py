from enum import Enum

class MealType(Enum):
    BREAKFAST = "BREAKFAST"
    BRUNCH = "BRUNCH"
    LUNCH = "LUNCH"
    SUPPER = "SUPPER"
    BEDTIME = "BEDTIME"

class UserType(Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    REPORTER = "REPORTER"

class ReportStatus(Enum):
    PENDING_REVIEW = "PENDING REVIEW"
    UNDER_REVIEW = "UNDER REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"