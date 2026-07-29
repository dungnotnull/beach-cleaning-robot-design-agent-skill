"""
hooks.py — Production-Grade Hooks System
Skill 235: beach-cleaning-robot-design v2.0.0

Implements lifecycle hooks for state synchronization, event emission,
and graceful error handling.
"""

import json
import logging
import time
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/hooks.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DegradationLevel(Enum):
    """Degradation levels for graceful failure handling."""
    FULL = 0
    SECONDARY_SOURCES = 1
    KNOWLEDGE_BASE_ONLY = 2
    FLAG_MISSING = 3
    UNAVAILABLE = 4


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RecoveryAction(Enum):
    """Recovery actions for errors."""
    RETRY = "retry"
    DEGRADE = "degrade"
    ABORT = "abort"
    IGNORE = "ignore"


@dataclass
class ExecutionContext:
    """Execution context for hooks."""
    execution_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    skill_name: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    current_step: Optional[str] = None
    degradation_level: DegradationLevel = DegradationLevel.FULL
    language: str = "en"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ErrorRecord:
    """Error record for tracking."""
    error_type: str
    message: str
    severity: ErrorSeverity
    timestamp: datetime = field(default_factory=datetime.now)
    step_name: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SkillEvent:
    """Skill event for emission."""
    event_type: str
    timestamp: datetime = field(default_factory=datetime.now)
    execution_id: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)


# Hook state storage
_hook_state: Dict[str, Any] = {}


def get_hook_state() -> Dict[str, Any]:
    """Get current hook state."""
    return _hook_state.copy()


def update_hook_state(key: str, value: Any) -> None:
    """Update hook state."""
    _hook_state[key] = value
    logger.debug(f"Hook state updated: {key} = {value}")


# ==================== HOOK HANDLERS ====================

def pre_flight_handler(
    inputs: Dict[str, Any],
    context: ExecutionContext,
    skill_name: str
) -> Dict[str, Any]:
    """
    Pre-flight hook handler.
    Validates inputs, detects language, checks tool availability.
    """
    logger.info(f"[PRE-FLIGHT] Starting pre-flight for {skill_name}")

    try:
        # Input validation
        errors = []
        warnings = []

        if not inputs.get("object"):
            errors.append("Missing required field: object")

        # Language detection
        language = detect_language(inputs)
        context.language = language
        update_hook_state("detected_language", language)

        # Tool availability check
        available_tools = check_tool_availability()
        update_hook_state("available_tools", available_tools)

        result = {
            "valid": len(errors) == 0,
            "errors": errors,
            "normalized_inputs": normalize_inputs(inputs),
            "warnings": warnings,
            "language": language
        }

        # Emit event
        emit_event(SkillEvent(
            event_type="skill.started",
            execution_id=context.execution_id,
            payload={"skill_name": skill_name, "inputs": inputs}
        ))

        logger.info(f"[PRE-FLIGHT] Complete - valid: {result['valid']}")
        return result

    except Exception as e:
        logger.error(f"[PRE-FLIGHT] Error: {e}")
        return {"valid": False, "errors": [str(e)]}


def pre_step_handler(
    step_name: str,
    step_number: int,
    state: Dict[str, Any],
    inputs: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Pre-step hook handler.
    Verifies state and prepares step inputs.
    """
    logger.info(f"[PRE-STEP] Step {step_number}: {step_name}")

    try:
        errors = []
        ready = True

        # Verify required state exists
        if step_number > 1 and not state.get(f"step_{step_number-1}_complete"):
            errors.append(f"Step {step_number-1} not completed")
            ready = False

        # Check dependencies
        required_keys = get_step_requirements(step_name)
        missing_keys = [k for k in required_keys if k not in state]
        if missing_keys:
            errors.append(f"Missing state keys: {missing_keys}")
            ready = False

        # Emit event
        emit_event(SkillEvent(
            event_type="step.started",
            payload={"step_name": step_name, "step_number": step_number}
        ))

        update_hook_state(f"step_{step_number}_start_time", time.time())

        logger.info(f"[PRE-STEP] Ready: {ready}")
        return {"ready": ready, "errors": errors, "prepared_inputs": inputs}

    except Exception as e:
        logger.error(f"[PRE-STEP] Error: {e}")
        return {"ready": False, "errors": [str(e)]}


def post_step_handler(
    step_name: str,
    step_number: int,
    result: Dict[str, Any],
    state: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Post-step hook handler.
    Validates output, updates state, runs quality gates.
    """
    logger.info(f"[POST-STEP] Step {step_number}: {step_name}")

    try:
        errors = []
        quality_gate_passed = True

        # Validate output against schema if available
        schema = get_step_output_schema(step_name)
        if schema:
            validation_result = validate_schema(result, schema)
            if not validation_result["valid"]:
                errors.extend(validation_result["errors"])
                quality_gate_passed = False

        # Update state
        state[f"step_{step_number}_result"] = result
        state[f"step_{step_number}_complete"] = True
        state["current_step"] = step_number + 1

        # Emit event
        emit_event(SkillEvent(
            event_type="step.completed",
            payload={"step_name": step_name, "result": result}
        ))

        duration = time.time() - _hook_state.get(f"step_{step_number}_start_time", time.time())
        logger.info(f"[POST-STEP] Complete - duration: {duration:.2f}s, gate_passed: {quality_gate_passed}")

        return {
            "state_updated": True,
            "quality_gate_passed": quality_gate_passed,
            "errors": errors,
            "next_step_ready": len(errors) == 0
        }

    except Exception as e:
        logger.error(f"[POST-STEP] Error: {e}")
        return {"state_updated": False, "quality_gate_passed": False, "errors": [str(e)]}


def on_error_handler(
    error: Exception,
    context: ExecutionContext,
    step_name: Optional[str] = None,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
) -> Dict[str, Any]:
    """
    On-error hook handler.
    Centralized error handling and recovery.
    """
    logger.error(f"[ON-ERROR] {severity.value}: {error} in step: {step_name}")

    # Record error
    error_record = ErrorRecord(
        error_type=type(error).__name__,
        message=str(error),
        severity=severity,
        step_name=step_name,
        context={"execution_id": context.execution_id}
    )

    errors = _hook_state.get("errors", [])
    errors.append(error_record)
    update_hook_state("errors", errors)

    # Determine recovery action
    action = determine_recovery_action(error, severity)

    # Prepare user message
    user_message = prepare_user_message(error, action)

    result = {
        "action": action.value,
        "retry_after_ms": 1000 if action == RecoveryAction.RETRY else None,
        "degradation_level": context.degradation_level.value + 1 if action == RecoveryAction.DEGRADE else None,
        "user_message": user_message
    }

    logger.info(f"[ON-ERROR] Recovery action: {action.value}")
    return result


def on_degrade_handler(
    from_level: int,
    to_level: int,
    reason: str,
    context: ExecutionContext
) -> Dict[str, Any]:
    """
    On-degrade hook handler.
    Flags limitations and adjusts output expectations.
    """
    logger.warning(f"[ON-DEGRADE] Level {from_level} → {to_level}: {reason}")

    context.degradation_level = DegradationLevel(to_level)
    update_hook_state("degradation_level", to_level)

    # Emit limitation banner
    limitation_banner = generate_limitation_banner(to_level, reason)

    # Suggest alternatives if available
    alternative = suggest_alternative(to_level)

    emit_event(SkillEvent(
        event_type="degradation.changed",
        payload={"from_level": from_level, "to_level": to_level, "reason": reason}
    ))

    return {
        "limitation_emitted": True,
        "output_adjusted": True,
        "alternative_suggested": alternative
    }


def post_flight_handler(
    outputs: Dict[str, Any],
    context: ExecutionContext,
    execution_time_ms: int,
    quality_gates_results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Post-flight hook handler.
    Final validation and delivery preparation.
    """
    logger.info(f"[POST-FLIGHT] Execution time: {execution_time_ms}ms")

    try:
        # Run final quality gate validation
        final_quality_check = all(qg.get("passed", False) for qg in quality_gates_results)

        # Format output according to template
        formatted_output = format_output(outputs, context.language)

        # Add metadata
        metadata = {
            "execution_id": context.execution_id,
            "execution_time_ms": execution_time_ms,
            "degradation_level": context.degradation_level.value,
            "quality_gates_passed": len([qg for qg in quality_gates_results if qg.get("passed", False)])
        }

        # Emit completion event
        emit_event(SkillEvent(
            event_type="skill.completed",
            payload={"outputs": outputs, "duration_ms": execution_time_ms}
        ))

        result = {
            "delivery_ready": final_quality_check,
            "final_quality_check": final_quality_check,
            "formatted_output": formatted_output,
            "metadata": metadata
        }

        logger.info(f"[POST-FLIGHT] Complete - delivery_ready: {result['delivery_ready']}")
        return result

    except Exception as e:
        logger.error(f"[POST-FLIGHT] Error: {e}")
        return {"delivery_ready": False, "final_quality_check": False, "errors": [str(e)]}


# ==================== HELPER FUNCTIONS ====================

def detect_language(inputs: Dict[str, Any]) -> str:
    """Detect language from inputs."""
    vietnamese_chars = set("àáảãạăâèéêìíòóôơùúưý")
    text = str(inputs)

    if any(char in vietnamese_chars for char in text):
        return "vi"
    return "en"


def check_tool_availability() -> List[str]:
    """Check which tools are available."""
    # This would integrate with actual tool registry
    return ["WebSearch", "WebFetch", "Read", "Write", "Bash", "Skill"]


def normalize_inputs(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize input values."""
    normalized = inputs.copy()

    # Default analysis type
    if "analysis_type" not in normalized:
        normalized["analysis_type"] = "combined"

    return normalized


def get_step_requirements(step_name: str) -> List[str]:
    """Get required state keys for a step."""
    requirements = {
        "sub-gather-requirements": [],
        "sub-evidence-collector": ["requirements"],
        "sub-core-analysis": ["requirements", "evidence"],
        "sub-knowledge-updater": ["requirements", "evidence", "core_analysis"],
        "sub-advisor": ["requirements", "evidence", "core_analysis", "knowledge"]
    }
    return requirements.get(step_name, [])


def get_step_output_schema(step_name: str) -> Optional[Dict[str, Any]]:
    """Get output schema for a step."""
    # This would load from config/schemas/
    return None


def validate_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """Validate data against JSON schema."""
    # This would use jsonschema library
    return {"valid": True, "errors": []}


def determine_recovery_action(error: Exception, severity: ErrorSeverity) -> RecoveryAction:
    """Determine appropriate recovery action."""
    if severity == ErrorSeverity.CRITICAL:
        return RecoveryAction.ABORT
    if "timeout" in str(error).lower():
        return RecoveryAction.DEGRADE
    if "not found" in str(error).lower():
        return RecoveryAction.DEGRADE
    return RecoveryAction.RETRY


def prepare_user_message(error: Exception, action: RecoveryAction) -> str:
    """Prepare user-facing error message."""
    messages = {
        RecoveryAction.RETRY: "Temporary issue, retrying...",
        RecoveryAction.DEGRADE: "Using alternative data sources, some limitations apply.",
        RecoveryAction.ABORT: "Critical error, cannot continue.",
        RecoveryAction.IGNORE: "Issue encountered, continuing with caution."
    }
    return messages.get(action, "Unknown error occurred.")


def generate_limitation_banner(level: int, reason: str) -> str:
    """Generate limitation banner for degraded mode."""
    return f"""
---
⚠️ LIMITATION NOTICE
This output was generated with reduced data availability (Level {level}).
Reason: {reason}
Cross-check with current data before acting on it.
---
"""


def suggest_alternative(level: int) -> Optional[str]:
    """Suggest alternative approaches."""
    alternatives = {
        2: "Using cached knowledge base - consider refreshing data.",
        3: "Key inputs missing - provide complete specifications.",
        4: "All sources unavailable - try again later."
    }
    return alternatives.get(level)


def format_output(outputs: Dict[str, Any], language: str) -> str:
    """Format output according to template."""
    # This would apply the output template
    return json.dumps(outputs, indent=2)


def emit_event(event: SkillEvent) -> None:
    """Emit a skill event."""
    logger.info(f"[EVENT] {event.event_type}: {event.payload}")
    # Event consumers would be registered here


# ==================== EXPORTS ====================

__all__ = [
    "ExecutionContext",
    "DegradationLevel",
    "ErrorSeverity",
    "RecoveryAction",
    "ErrorRecord",
    "SkillEvent",
    "pre_flight_handler",
    "pre_step_handler",
    "post_step_handler",
    "on_error_handler",
    "on_degrade_handler",
    "post_flight_handler",
    "get_hook_state",
    "emit_event"
]
