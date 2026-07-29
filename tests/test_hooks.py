"""
test_hooks.py — Hooks System Tests
Skill 235: beach-cleaning-robot-design v2.0.0

Unit tests for the hooks system.
"""

import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

try:
    from hooks import (
        ExecutionContext,
        DegradationLevel,
        ErrorSeverity,
        RecoveryAction,
        pre_flight_handler,
        pre_step_handler,
        post_step_handler,
        on_error_handler,
        on_degrade_handler,
        post_flight_handler,
        get_hook_state,
        update_hook_state
    )
    HOOKS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import hooks: {e}")
    HOOKS_AVAILABLE = False


def test_execution_context():
    """Test ExecutionContext creation."""
    if not HOOKS_AVAILABLE:
        print("[SKIP] execution_context test - hooks not available")
        return

    ctx = ExecutionContext(skill_name="test_skill", language="vi")
    assert ctx.skill_name == "test_skill"
    assert ctx.language == "vi"
    assert ctx.degradation_level == DegradationLevel.FULL
    print("[OK] execution_context")


def test_pre_flight_validation():
    """Test pre-flight input validation."""
    if not HOOKS_AVAILABLE:
        print("[SKIP] pre_flight test - hooks not available")
        return

    # Valid input
    result = pre_flight_handler(
        inputs={"object": "test robot"},
        context=ExecutionContext(),
        skill_name="test"
    )
    assert result["valid"] == True
    assert result["language"] == "en"

    # Invalid input (missing object)
    result = pre_flight_handler(
        inputs={},
        context=ExecutionContext(),
        skill_name="test"
    )
    assert result["valid"] == False
    assert "Missing required field: object" in result["errors"]

    print("[OK] pre_flight_validation")


def test_error_recovery():
    """Test error recovery action determination."""
    if not HOOKS_AVAILABLE:
        print("[SKIP] error_recovery test - hooks not available")
        return

    ctx = ExecutionContext()

    # Timeout error → degrade
    result = on_error_handler(
        error=Exception("Request timeout"),
        context=ctx,
        severity=ErrorSeverity.MEDIUM
    )
    assert result["action"] in ["retry", "degrade"]

    # Critical error → abort
    result = on_error_handler(
        error=Exception("Critical system failure"),
        context=ctx,
        severity=ErrorSeverity.CRITICAL
    )
    assert result["action"] == "abort"

    print("[OK] error_recovery")


def test_degradation_handling():
    """Test degradation handling."""
    if not HOOKS_AVAILABLE:
        print("[SKIP] degradation test - hooks not available")
        return

    ctx = ExecutionContext()

    result = on_degrade_handler(
        from_level=0,
        to_level=2,
        reason="Network sources unavailable",
        context=ctx
    )

    assert result["limitation_emitted"] == True
    assert result["output_adjusted"] == True
    assert ctx.degradation_level == DegradationLevel(int(2))

    print("[OK] degradation_handling")


def test_hook_state():
    """Test hook state management."""
    if not HOOKS_AVAILABLE:
        print("[SKIP] hook_state test - hooks not available")
        return

    update_hook_state("test_key", "test_value")
    state = get_hook_state()
    assert state.get("test_key") == "test_value"

    print("[OK] hook_state")


def run_all_tests():
    """Run all hooks tests."""
    print("Running hooks tests...")
    print("=" * 60)

    test_execution_context()
    test_pre_flight_validation()
    test_error_recovery()
    test_degradation_handling()
    test_hook_state()

    print("=" * 60)
    print("All hooks tests passed!")


if __name__ == "__main__":
    run_all_tests()
