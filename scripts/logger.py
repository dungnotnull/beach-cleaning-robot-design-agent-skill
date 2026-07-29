"""
logger.py — Structured Logging System
Skill 235: beach-cleaning-robot-design v2.0.0

Production-grade structured logging with context management.
"""

import json
import logging
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional
from contextlib import contextmanager


class LogLevel(Enum):
    """Log levels for structured logging."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class StructuredLogger:
    """Structured logger with context management."""

    def __init__(
        self,
        name: str,
        log_dir: Path = None,
        level: LogLevel = LogLevel.INFO
    ):
        """Initialize structured logger."""
        self.name = name
        self.log_dir = log_dir or Path(__file__).parent.parent / "logs"
        self.level = level

        # Create log directory
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Setup logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.value))

        # Clear existing handlers
        self.logger.handlers.clear()

        # Console handler with simple format
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler with JSON format for structured logs
        file_handler = logging.FileHandler(
            self.log_dir / f"{name}.log",
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, level.value))
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Structured log file (JSON lines)
        self.json_handler = logging.FileHandler(
            self.log_dir / f"{name}.jsonl",
            encoding='utf-8'
        )
        self.json_handler.setLevel(getattr(logging, level.value))
        self.json_handler.setFormatter(JsonFormatter())
        self.logger.addHandler(self.json_handler)

    def debug(self, message: str, **context) -> None:
        """Log debug message with context."""
        self._log(LogLevel.DEBUG, message, context)

    def info(self, message: str, **context) -> None:
        """Log info message with context."""
        self._log(LogLevel.INFO, message, context)

    def warning(self, message: str, **context) -> None:
        """Log warning message with context."""
        self._log(LogLevel.WARNING, message, context)

    def error(self, message: str, **context) -> None:
        """Log error message with context."""
        self._log(LogLevel.ERROR, message, context)

    def critical(self, message: str, **context) -> None:
        """Log critical message with context."""
        self._log(LogLevel.CRITICAL, message, context)

    def _log(self, level: LogLevel, message: str, context: Dict[str, Any]) -> None:
        """Internal log method."""
        log_entry = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "level": level.value,
            **context
        }
        log_method = getattr(self.logger, level.value.lower())
        log_method(json.dumps(log_entry), extra={"structured": log_entry})

    @contextmanager
    def context(self, **kwargs):
        """Context manager for adding context to all logs within scope."""
        original_context = kwargs.copy()
        try:
            self.info("Context entered", **original_context)
            yield
        finally:
            self.info("Context exited", **original_context)

    def log_hook_event(
        self,
        hook_name: str,
        event_type: str,
        **details
    ) -> None:
        """Log a hook event."""
        self.info(
            f"Hook event: {hook_name} - {event_type}",
            hook=hook_name,
            event_type=event_type,
            **details
        )

    def log_quality_gate(
        self,
        gate_name: str,
        passed: bool,
        **details
    ) -> None:
        """Log a quality gate check."""
        level = LogLevel.INFO if passed else LogLevel.WARNING
        self._log(
            level,
            f"Quality gate: {gate_name} - {'PASSED' if passed else 'FAILED'}",
            {"gate": gate_name, "passed": passed, **details}
        )

    def log_execution_start(
        self,
        skill_name: str,
        execution_id: str,
        **params
    ) -> None:
        """Log execution start."""
        self.info(
            f"Execution started: {skill_name}",
            skill=skill_name,
            execution_id=execution_id,
            event_type="execution.start",
            **params
        )

    def log_execution_complete(
        self,
        skill_name: str,
        execution_id: str,
        duration_ms: int,
        success: bool,
        **result
    ) -> None:
        """Log execution completion."""
        level = LogLevel.INFO if success else LogLevel.ERROR
        self._log(
            level,
            f"Execution completed: {skill_name} - {'SUCCESS' if success else 'FAILED'}",
            {
                "skill": skill_name,
                "execution_id": execution_id,
                "event_type": "execution.complete",
                "duration_ms": duration_ms,
                "success": success,
                **result
            }
        )


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        if hasattr(record, 'structured'):
            return json.dumps(record.structured)

        # Fallback to basic JSON
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        return json.dumps(log_entry)


# Singleton instances
_loggers: Dict[str, StructuredLogger] = {}


def get_logger(name: str = "beach-cleaning-robot-design") -> StructuredLogger:
    """Get or create a structured logger instance."""
    if name not in _loggers:
        _loggers[name] = StructuredLogger(name)
    return _loggers[name]


# Convenience functions
def log_hook_event(hook_name: str, event_type: str, **details) -> None:
    """Log a hook event using default logger."""
    get_logger().log_hook_event(hook_name, event_type, **details)


def log_quality_gate(gate_name: str, passed: bool, **details) -> None:
    """Log a quality gate check using default logger."""
    get_logger().log_quality_gate(gate_name, passed, **details)


def log_execution_start(skill_name: str, execution_id: str, **params) -> None:
    """Log execution start using default logger."""
    get_logger().log_execution_start(skill_name, execution_id, **params)


def log_execution_complete(
    skill_name: str,
    execution_id: str,
    duration_ms: int,
    success: bool,
    **result
) -> None:
    """Log execution completion using default logger."""
    get_logger().log_execution_complete(
        skill_name, execution_id, duration_ms, success, **result
    )


__all__ = [
    "LogLevel",
    "StructuredLogger",
    "get_logger",
    "log_hook_event",
    "log_quality_gate",
    "log_execution_start",
    "log_execution_complete"
]
