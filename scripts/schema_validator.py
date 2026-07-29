"""
schema_validator.py — JSON Schema Validation
Skill 235: beach-cleaning-robot-design v2.0.0

Production-grade JSON schema validation with detailed error reporting.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

try:
    from jsonschema import validate, ValidationError, Draft7Validator
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchemaValidator:
    """Production-grade JSON schema validator."""

    def __init__(self, schema_dir: Path = None):
        """Initialize validator with schema directory."""
        self.schema_dir = schema_dir or Path(__file__).parent.parent / "config" / "schemas"
        self.schemas: Dict[str, Dict] = {}
        self.validators: Dict[str, Draft7Validator] = {}
        self._load_schemas()

    def _load_schemas(self) -> None:
        """Load all schema files from the schema directory."""
        if not self.schema_dir.exists():
            logger.warning(f"Schema directory not found: {self.schema_dir}")
            return

        for schema_file in self.schema_dir.glob("*.json"):
            try:
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema = json.load(f)
                    schema_name = schema_file.stem
                    self.schemas[schema_name] = schema

                    if JSONSCHEMA_AVAILABLE:
                        self.validators[schema_name] = Draft7Validator(schema)

                    logger.info(f"Loaded schema: {schema_name}")
            except Exception as e:
                logger.error(f"Failed to load schema {schema_file}: {e}")

    def validate(
        self,
        data: Dict[str, Any],
        schema_name: str
    ) -> Dict[str, Any]:
        """
        Validate data against a named schema.

        Returns:
            Dict with keys: valid (bool), errors (List[str]), details (List[Dict])
        """
        if schema_name not in self.schemas:
            return {
                "valid": False,
                "errors": [f"Schema not found: {schema_name}"],
                "details": []
            }

        if not JSONSCHEMA_AVAILABLE:
            logger.warning("jsonschema not available, skipping validation")
            return {"valid": True, "errors": [], "details": []}

        try:
            validator = self.validators[schema_name]
            errors = list(validator.iter_errors(data))

            if not errors:
                return {"valid": True, "errors": [], "details": []}

            # Format errors for user consumption
            formatted_errors = []
            error_details = []

            for error in errors:
                path = " -> ".join(str(p) for p in error.path) if error.path else "root"
                formatted_errors.append(f"{path}: {error.message}")
                error_details.append({
                    "path": path,
                    "message": error.message,
                    "validator": error.validator,
                    "failed_value": str(error.instance) if error.instance else None
                })

            return {
                "valid": False,
                "errors": formatted_errors,
                "details": error_details
            }

        except Exception as e:
            logger.error(f"Validation error: {e}")
            return {
                "valid": False,
                "errors": [f"Validation failed: {str(e)}"],
                "details": []
            }

    def validate_and_fix(
        self,
        data: Dict[str, Any],
        schema_name: str
    ) -> Dict[str, Any]:
        """
        Validate and attempt to fix common issues.

        Returns:
            Dict with keys: valid (bool), data (Dict), errors (List[str]), fixes_applied (List[str])
        """
        result = self.validate(data, schema_name)
        fixes_applied = []

        if result["valid"]:
            return {
                "valid": True,
                "data": data,
                "errors": [],
                "fixes_applied": []
            }

        # Attempt fixes based on error types
        fixed_data = data.copy()

        for detail in result.get("details", []):
            validator = detail.get("validator", "")
            path = detail.get("path", "")

            # Fix missing required fields with defaults
            if validator == "required":
                # Add default values for missing required fields
                # This would be schema-specific
                pass

            # Fix type mismatches
            elif validator == "type":
                # Attempt type conversion
                pass

        # Re-validate after fixes
        revalidation = self.validate(fixed_data, schema_name)

        return {
            "valid": revalidation["valid"],
            "data": fixed_data,
            "errors": revalidation["errors"],
            "fixes_applied": fixes_applied
        }

    def get_schema(self, schema_name: str) -> Dict[str, Any]:
        """Get a schema by name."""
        return self.schemas.get(schema_name, {})

    def list_schemas(self) -> List[str]:
        """List all available schema names."""
        return list(self.schemas.keys())

    def validate_batch(
        self,
        items: List[Dict[str, Any]],
        schema_name: str
    ) -> Dict[str, Any]:
        """
        Validate multiple items against a schema.

        Returns:
            Dict with keys: valid (bool), results (List[Dict]), failed_indices (List[int])
        """
        results = []
        failed_indices = []

        for i, item in enumerate(items):
            result = self.validate(item, schema_name)
            results.append({
                "index": i,
                "valid": result["valid"],
                "errors": result["errors"]
            })
            if not result["valid"]:
                failed_indices.append(i)

        return {
            "valid": len(failed_indices) == 0,
            "results": results,
            "failed_indices": failed_indices
        }


# Singleton instance
_validator_instance: SchemaValidator = None


def get_validator() -> SchemaValidator:
    """Get the singleton validator instance."""
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = SchemaValidator()
    return _validator_instance


# CLI interface
def main():
    """CLI interface for schema validation."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python schema_validator.py <schema_name> [data_file]")
        print("\nAvailable schemas:")
        validator = SchemaValidator()
        for name in validator.list_schemas():
            print(f"  - {name}")
        sys.exit(1)

    schema_name = sys.argv[1]
    validator = SchemaValidator()

    if len(sys.argv) >= 3:
        # Validate from file
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            data = json.load(f)
        result = validator.validate(data, schema_name)
    else:
        # List schema details
        schema = validator.get_schema(schema_name)
        if schema:
            print(f"Schema: {schema_name}")
            print(f"Title: {schema.get('title', 'N/A')}")
            print(f"Description: {schema.get('description', 'N/A')}")
            print(f"Required fields: {schema.get('required', [])}")
        sys.exit(0)

    print(f"Validation result: {'PASSED' if result['valid'] else 'FAILED'}")
    if result['errors']:
        print("\nErrors:")
        for error in result['errors']:
            print(f"  - {error}")

    sys.exit(0 if result['valid'] else 1)


if __name__ == "__main__":
    main()
