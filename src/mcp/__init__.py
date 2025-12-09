"""MCP-style tools for extending agent capabilities"""
from .tools import (
    get_document_metadata,
    calculate_days_between,
    estimate_coverage_payout,
    validate_claim_status,
    get_timeline_summary
)

__all__ = [
    'get_document_metadata',
    'calculate_days_between',
    'estimate_coverage_payout',
    'validate_claim_status',
    'get_timeline_summary'
]
