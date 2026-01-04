# Test Suite

## Purpose

Comprehensive test suite for unit tests, integration tests, and end-to-end tests.

## Structure

```
tests/
├── conftest.py          # Pytest configuration
├── unit/                # Unit tests
│   ├── agents/         # Agent unit tests
│   ├── tools/          # Tools unit tests
│   └── orchestrator/   # Orchestrator unit tests
├── integration/        # Integration tests
│   └── workflows/       # Workflow integration tests
└── e2e/                # End-to-end tests
    └── test_full_workflow.py
```

## Tech Stack

- **Framework**: pytest
- **Async**: pytest-asyncio
- **Coverage**: pytest-cov
- **HTTP Testing**: httpx

## Test Types

### Unit Tests
- Individual component testing
- Mocked dependencies
- Fast execution

### Integration Tests
- Service interaction testing
- Database integration
- Agent communication

### End-to-End Tests
- Full workflow testing
- Real services (or Docker)
- Complete ticket lifecycle

## Usage Examples

### Run All Tests

```bash
pytest
```

### Run Unit Tests Only

```bash
pytest tests/unit/
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html
```

### Run Specific Test

```bash
pytest tests/unit/agents/test_router_agent.py
```

## Configuration

Tests use pytest configuration in `conftest.py`:
- Test fixtures
- Mock setup
- Database test configuration



