"""Tests for the simple workflow recipe."""

import yaml
import pytest
from pathlib import Path

from arazzo_runner import ArazzoRunner


@pytest.fixture
def workflow_file():
    """Path to the workflow file."""
    return Path(__file__).parent.parent / "arazzo" / "workflow.arazzo.yaml"


@pytest.fixture
def openapi_file():
    """Path to the OpenAPI file."""
    return Path(__file__).parent.parent / "openapi" / "jsonplaceholder.openapi.yaml"


@pytest.fixture
def runner(workflow_file, openapi_file):
    """Create an ArazzoRunner instance."""
    # Load the Arazzo document
    with open(workflow_file) as f:
        arazzo_doc = yaml.safe_load(f)
    
    # Load the OpenAPI specification
    with open(openapi_file) as f:
        openapi_spec = yaml.safe_load(f)
    
    # Create source descriptions dict
    source_descriptions = {
        "jsonPlaceholderAPI": openapi_spec
    }
    
    return ArazzoRunner(arazzo_doc, source_descriptions)


def test_workflow_file_exists(workflow_file):
    """Test that the workflow file exists."""
    assert workflow_file.exists(), f"Workflow file not found at {workflow_file}"


def test_openapi_file_exists(openapi_file):
    """Test that the OpenAPI file exists."""
    assert openapi_file.exists(), f"OpenAPI file not found at {openapi_file}"


def test_workflow_loads_successfully(runner):
    """Test that the workflow loads without errors."""
    assert runner is not None
    assert hasattr(runner, 'start_workflow')


def test_successful_execution(runner):
    """Test successful workflow execution with valid input."""
    execution_id = runner.start_workflow("getUserInfo", {"userId": 1})
    
    # Execute all steps
    result = None
    for _ in range(10):  # Max 10 steps
        result = runner.execute_next_step(execution_id)
        if result["status"] == "workflow_complete":
            break
    
    assert result["status"] == "workflow_complete"
    
    # Get the execution state
    state = runner.execution_states[execution_id]
    assert "fetchUser" in state.step_outputs
    
    user = state.step_outputs["fetchUser"]
    assert user.get("userId") == 1
    assert user.get("username") is not None
    assert user.get("email") is not None


def test_execution_with_different_users(runner):
    """Test execution with multiple user IDs."""
    user_ids = [1, 2, 3, 5, 10]
    
    for user_id in user_ids:
        execution_id = runner.start_workflow("getUserInfo", {"userId": user_id})
        
        result = None
        for _ in range(10):
            result = runner.execute_next_step(execution_id)
            if result["status"] == "workflow_complete":
                break
        
        assert result["status"] == "workflow_complete"
        state = runner.execution_states[execution_id]
        user = state.step_outputs["fetchUser"]
        assert user.get("userId") == user_id


def test_output_structure(runner):
    """Test that outputs have the expected structure."""
    execution_id = runner.start_workflow("getUserInfo", {"userId": 1})
    
    result = None
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result["status"] == "workflow_complete":
            break
    
    state = runner.execution_states[execution_id]
    user = state.step_outputs["fetchUser"]
    
    # Check required fields
    required_fields = ["userId", "username", "email", "name"]
    for field in required_fields:
        assert field in user, f"Missing required field: {field}"
    
    # Check optional fields
    optional_fields = ["phone", "website"]
    for field in optional_fields:
        assert field in user, f"Missing optional field: {field}"


@pytest.mark.parametrize("user_id,expected_username", [
    (1, "Bret"),
    (2, "Antonette"),
    (3, "Samantha"),
])
def test_known_users(runner, user_id, expected_username):
    """Test execution with known user IDs and verify usernames."""
    execution_id = runner.start_workflow("getUserInfo", {"userId": user_id})
    
    result = None
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result["status"] == "workflow_complete":
            break
    
    state = runner.execution_states[execution_id]
    user = state.step_outputs["fetchUser"]
    assert user.get("username") == expected_username


def test_default_user_id(runner):
    """Test execution with explicitly provided default user ID."""
    # Explicitly provide the default value instead of relying on workflow defaults
    execution_id = runner.start_workflow("getUserInfo", {"userId": 1})
    
    result = None
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result["status"] == "workflow_complete":
            break
    
    # Should successfully fetch user 1
    assert result["status"] == "workflow_complete"
    state = runner.execution_states[execution_id]
    user = state.step_outputs["fetchUser"]
    assert user.get("userId") == 1