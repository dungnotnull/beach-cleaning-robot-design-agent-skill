# Contributing to beach-cleaning-robot-design

Thank you for your interest in contributing! This is a professional-grade Claude Code harness for Beach-Cleaning Robotics & Coastal Engineering.

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python tools/test_knowledge_updater.py
python tools/run_test_scenarios.py

# Validate project structure
cd ..
python tools/validate_project.py 235-beach-cleaning-robot-design
```

## Project Structure

- `skills/` — Harness and sub-skill markdown files
- `tools/` — Python utilities for knowledge updates and testing
- `tests/` — Test scenarios and results
- `SECOND-KNOWLEDGE-BRAIN.md` — Living knowledge base

## Standards

All contributions must:
1. Pass the 8-File Contract validation
2. Include tests for new functionality
3. Follow the existing code style and documentation format
4. Preserve the evidence hierarchy and quality gate system

## Knowledge Updates

The knowledge base is updated automatically via cron. Manual updates:

```bash
python tools/knowledge_updater.py --dry-run  # Preview
python tools/knowledge_updater.py             # Live update
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
