"""Provide API for user models enumeration."""
import enum


class RoleType(enum.Enum):
    """Represents role type enumeration."""

    ADMIN = 'admin'
    APPROVER = 'approver'
    COMPLAINER = 'complainer'


class State(enum.Enum):
    """Represents status state enumeration."""

    APPROVED = 'Approved'
    PENDING = 'Pending'
    REJECTED = 'Rejected'
