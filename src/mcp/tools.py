"""
MCP Tools for Insurance Claim System
These tools extend LLM capabilities beyond prompting
Implemented as LangChain-compatible tools
"""

from datetime import datetime, timedelta
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_document_metadata(claim_id: str) -> Dict[str, Any]:
    """
    MCP Tool: Retrieve document filing information and metadata

    Args:
        claim_id: The claim ID to look up (e.g., "CLM-2024-001")

    Returns:
        Dictionary with document metadata
    """
    logger.info(f"MCP Tool called: get_document_metadata({claim_id})")

    # In a real system, this would query a database
    # For demo purposes, we return mock data for our test claim
    metadata_db = {
        "CLM-2024-001": {
            "claim_id": "CLM-2024-001",
            "policy_number": "POL-2024-VEH-45782",
            "filed_date": "2024-01-15",
            "incident_date": "2024-01-12",
            "status": "Under Review",
            "last_updated": "2024-02-28",
            "policyholder": "Sarah Mitchell",
            "claim_type": "Auto - Multi-Vehicle Collision",
            "total_claim_amount": 23370.80,
            "deductible": 750.00,
            "adjuster": "Kevin Park",
            "adjuster_contact": "kevin.park@premierinsurance.com"
        }
    }

    result = metadata_db.get(claim_id, {
        "error": f"Claim {claim_id} not found",
        "available_claims": list(metadata_db.keys())
    })

    return result


def calculate_days_between(start_date: str, end_date: str) -> Dict[str, Any]:
    """
    MCP Tool: Calculate days between two dates

    Args:
        start_date: Start date in format "YYYY-MM-DD" or "Month DD, YYYY"
        end_date: End date in same format

    Returns:
        Dictionary with day calculations
    """
    logger.info(f"MCP Tool called: calculate_days_between({start_date}, {end_date})")

    try:
        # Try parsing YYYY-MM-DD format first
        try:
            d1 = datetime.strptime(start_date, "%Y-%m-%d")
            d2 = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            # Try "Month DD, YYYY" format
            d1 = datetime.strptime(start_date, "%B %d, %Y")
            d2 = datetime.strptime(end_date, "%B %d, %Y")

        delta = d2 - d1
        total_days = delta.days

        # Calculate business days (excluding weekends)
        business_days = 0
        current = d1
        while current <= d2:
            if current.weekday() < 5:  # Monday = 0, Sunday = 6
                business_days += 1
            current += timedelta(days=1)

        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_days": total_days,
            "business_days": business_days,
            "weeks": round(total_days / 7, 1),
            "calculation_date": datetime.now().strftime("%Y-%m-%d")
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": "Date format should be 'YYYY-MM-DD' or 'Month DD, YYYY'"
        }


def estimate_coverage_payout(
    damage_amount: float,
    deductible: float,
    policy_limit: float = None
) -> Dict[str, Any]:
    """
    MCP Tool: Calculate insurance payout based on policy terms

    Args:
        damage_amount: Total damage/claim amount
        deductible: Policy deductible amount
        policy_limit: Optional policy coverage limit

    Returns:
        Dictionary with payout calculations
    """
    logger.info(f"MCP Tool called: estimate_coverage_payout(damage={damage_amount}, deductible={deductible})")

    try:
        # Basic payout calculation
        payout_before_limit = max(0, damage_amount - deductible)

        # Apply policy limit if specified
        if policy_limit:
            payout = min(payout_before_limit, policy_limit)
            limited = payout < payout_before_limit
        else:
            payout = payout_before_limit
            limited = False

        # Calculate percentages
        coverage_percentage = (payout / damage_amount * 100) if damage_amount > 0 else 0
        out_of_pocket = damage_amount - payout

        return {
            "damage_amount": round(damage_amount, 2),
            "deductible": round(deductible, 2),
            "policy_limit": policy_limit,
            "estimated_payout": round(payout, 2),
            "out_of_pocket": round(out_of_pocket, 2),
            "coverage_percentage": round(coverage_percentage, 1),
            "payout_limited_by_policy": limited,
            "fully_covered": payout == payout_before_limit and payout > 0
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": "Invalid input values for payout calculation"
        }


def validate_claim_status(
    filed_date: str,
    claim_status: str,
    days_since_filing: int = None
) -> Dict[str, Any]:
    """
    MCP Tool: Validate if claim is within filing window and check status

    Args:
        filed_date: Date claim was filed (format: YYYY-MM-DD)
        claim_status: Current status of claim
        days_since_filing: Optional override for days calculation

    Returns:
        Dictionary with validation results
    """
    logger.info(f"MCP Tool called: validate_claim_status({filed_date}, {claim_status})")

    try:
        # Calculate days since filing
        if days_since_filing is None:
            filed = datetime.strptime(filed_date, "%Y-%m-%d")
            today = datetime.now()
            days_since_filing = (today - filed).days

        # Define status expectations based on elapsed time
        # These are typical insurance claim timelines
        expected_status = None
        within_normal_timeframe = True

        if days_since_filing <= 3:
            expected_status = "Initial Review"
        elif days_since_filing <= 14:
            expected_status = "Under Review"
        elif days_since_filing <= 30:
            expected_status = "Pending Settlement"
        elif days_since_filing <= 45:
            expected_status = "Settlement Processing"
        else:
            expected_status = "Should be Closed"
            within_normal_timeframe = False

        # Claim is typically closed within 30-45 days
        within_filing_window = days_since_filing <= 365  # Most policies require claim within 1 year

        return {
            "filed_date": filed_date,
            "days_since_filing": days_since_filing,
            "current_status": claim_status,
            "expected_status": expected_status,
            "within_filing_window": within_filing_window,
            "within_normal_timeframe": within_normal_timeframe,
            "status_appropriate": claim_status in [expected_status, "Closed", "Settled"],
            "message": f"Claim filed {days_since_filing} days ago. Status '{claim_status}' is {'normal' if within_normal_timeframe else 'taking longer than usual'}."
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": "Invalid date format. Use YYYY-MM-DD"
        }


def get_timeline_summary(claim_id: str) -> Dict[str, Any]:
    """
    MCP Tool: Get quick timeline summary for a claim

    Args:
        claim_id: The claim ID to summarize

    Returns:
        Dictionary with key timeline events
    """
    logger.info(f"MCP Tool called: get_timeline_summary({claim_id})")

    # Mock timeline data for our test claim
    timelines = {
        "CLM-2024-001": {
            "claim_id": "CLM-2024-001",
            "incident_date": "2024-01-12",
            "filed_date": "2024-01-15",
            "first_assessment_date": "2024-01-14",
            "repairs_started": "2024-01-29",
            "repairs_completed": "2024-02-15",
            "total_duration_days": 34,
            "key_milestones": [
                "2024-01-12: Incident occurred (7:42 AM)",
                "2024-01-15: Claim filed",
                "2024-01-26: Liability accepted by at-fault party",
                "2024-01-29: Repairs authorized",
                "2024-02-15: Repairs completed",
                "2024-02-16: Vehicle returned to policyholder"
            ],
            "current_phase": "Final Settlement",
            "estimated_closure": "2024-03-20"
        }
    }

    result = timelines.get(claim_id, {
        "error": f"Timeline for claim {claim_id} not found",
        "available_claims": list(timelines.keys())
    })

    return result


# Convenience function to get all tools as LangChain Tool objects
def get_all_mcp_tools():
    """
    Get all MCP tools as LangChain Tool objects

    Returns:
        List of LangChain Tool objects
    """
    from langchain_core.tools import Tool

    tools = [
        Tool(
            name="GetDocumentMetadata",
            func=lambda claim_id: str(get_document_metadata(claim_id)),
            description="Get document metadata including filing date, status, policyholder info, and adjuster details. Input: claim_id (e.g., 'CLM-2024-001')"
        ),
        Tool(
            name="CalculateDaysBetween",
            func=lambda dates: str(calculate_days_between(*dates.split(","))),
            description="Calculate days between two dates. Input: 'start_date,end_date' in format 'YYYY-MM-DD,YYYY-MM-DD' or 'Month DD YYYY,Month DD YYYY'"
        ),
        Tool(
            name="EstimateCoveragePayout",
            func=lambda params: str(estimate_coverage_payout(*[float(x) for x in params.split(",")])),
            description="Estimate insurance payout. Input: 'damage_amount,deductible' or 'damage_amount,deductible,policy_limit' (numbers only, comma-separated)"
        ),
        Tool(
            name="ValidateClaimStatus",
            func=lambda params: str(validate_claim_status(*params.split(",")[:2])),
            description="Validate claim status and check if within normal timeframes. Input: 'filed_date,claim_status' (date in YYYY-MM-DD format)"
        ),
        Tool(
            name="GetTimelineSummary",
            func=lambda claim_id: str(get_timeline_summary(claim_id)),
            description="Get timeline summary with key milestones for a claim. Input: claim_id (e.g., 'CLM-2024-001')"
        )
    ]

    return tools


if __name__ == "__main__":
    print("\n=== MCP Tools Test ===\n")

    # Test each tool
    print("1. Get Document Metadata:")
    print(get_document_metadata("CLM-2024-001"))

    print("\n2. Calculate Days Between:")
    print(calculate_days_between("2024-01-12", "2024-02-15"))

    print("\n3. Estimate Coverage Payout:")
    print(estimate_coverage_payout(17111.83, 750.00))

    print("\n4. Validate Claim Status:")
    print(validate_claim_status("2024-01-15", "Under Review"))

    print("\n5. Get Timeline Summary:")
    print(get_timeline_summary("CLM-2024-001"))
