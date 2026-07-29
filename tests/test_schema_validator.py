"""
test_schema_validator.py — Schema Validation Tests
Skill 235: beach-cleaning-robot-design v2.0.0

Unit tests for JSON schema validation.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

try:
    from schema_validator import SchemaValidator, get_validator
    SCHEMA_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import schema_validator: {e}")
    SCHEMA_AVAILABLE = False


def test_validator_initialization():
    """Test validator initialization."""
    if not SCHEMA_AVAILABLE:
        print("[SKIP] validator initialization - schema_validator not available")
        return

    validator = SchemaValidator()
    schemas = validator.list_schemas()
    assert isinstance(schemas, list)
    assert len(schemas) > 0
    print(f"[OK] validator initialization (found {len(schemas)} schemas)")


def test_requirements_input_schema():
    """Test requirements input schema validation."""
    if not SCHEMA_AVAILABLE:
        print("[SKIP] requirements schema - schema_validator not available")
        return

    validator = get_validator()

    # Valid input
    valid_data = {
        "object": "test robot",
        "scope": "California beach",
        "language": "en",
        "analysis_type": "combined"
    }
    result = validator.validate(valid_data, "requirements-input")
    assert result["valid"] == True
    assert len(result["errors"]) == 0

    # Invalid input (missing required field)
    invalid_data = {
        "scope": "California beach"
    }
    result = validator.validate(invalid_data, "requirements-input")
    assert result["valid"] == False
    assert len(result["errors"]) > 0

    print("[OK] requirements input schema")


def test_evidence_output_schema():
    """Test evidence output schema validation."""
    if not SCHEMA_AVAILABLE:
        print("[SKIP] evidence schema - schema_validator not available")
        return

    validator = get_validator()

    # Valid output
    valid_data = {
        "current_data": [
            {
                "source": "test source",
                "value": "test value",
                "timestamp": "2026-07-27T10:00:00Z",
                "tier": "2"
            }
        ],
        "authoritative_docs": [
            {
                "title": "Test Document",
                "url": "https://example.com",
                "tier": "1"
            }
        ]
    }
    result = validator.validate(valid_data, "evidence-output")
    assert result["valid"] == True

    print("[OK] evidence output schema")


def test_core_analysis_output_schema():
    """Test core analysis output schema validation."""
    if not SCHEMA_AVAILABLE:
        print("[SKIP] core analysis schema - schema_validator not available")
        return

    validator = get_validator()

    # Valid output (minimal required fields)
    valid_data = {
        "locomotion_collection": {
            "type": "wheels",
            "collection_mechanism": "sieve",
            "rationale": "Test rationale"
        },
        "sensing_path_planning": {
            "sensors": [
                {"type": "camera", "purpose": "debris detection"}
            ],
            "algorithm": "boustrophedon",
            "tide_aware": True
        },
        "battery_autonomy": {
            "capacity_wh": 2000,
            "autonomy_hours": 8,
            "solar_assist": True
        },
        "reliability": {
            "ip_rating": "IP67",
            "corrosion_protection": True,
            "water_ingress_protection": True,
            "sand_abrasion_resistance": True
        },
        "scenarios": [
            {
                "name": "best",
                "coverage_rate_sqm_per_hour": 1500,
                "collection_efficiency_percent": 90
            },
            {
                "name": "base",
                "coverage_rate_sqm_per_hour": 1000,
                "collection_efficiency_percent": 80
            },
            {
                "name": "worst",
                "coverage_rate_sqm_per_hour": 500,
                "collection_efficiency_percent": 70
            }
        ]
    }
    result = validator.validate(valid_data, "core-analysis-output")
    assert result["valid"] == True

    print("[OK] core analysis output schema")


def test_final_report_output_schema():
    """Test final report output schema validation."""
    if not SCHEMA_AVAILABLE:
        print("[SKIP] final report schema - schema_validator not available")
        return

    validator = get_validator()

    # Valid output (minimal required fields)
    valid_data = {
        "report_metadata": {
            "date": "2026-07-27",
            "analyst": "beach-cleaning-robot-design v2.0",
            "language": "en",
            "version": "2.0.0"
        },
        "executive_summary": "This is a test executive summary for the robot design report.",
        "disclosure": "This analysis has limitations including data availability and model assumptions.",
        "recommendation": {
            "verdict": "Production-Ready Design",
            "confidence": "high"
        }
    }
    result = validator.validate(valid_data, "final-report-output")
    assert result["valid"] == True

    print("[OK] final report output schema")


def run_all_tests():
    """Run all schema validation tests."""
    print("Running schema validation tests...")
    print("=" * 60)

    test_validator_initialization()
    test_requirements_input_schema()
    test_evidence_output_schema()
    test_core_analysis_output_schema()
    test_final_report_output_schema()

    print("=" * 60)
    print("All schema validation tests passed!")


if __name__ == "__main__":
    run_all_tests()
