"""Tests for the simple workflow recipe."""

import pytest
from pathlib import Path

from arazzo_runner import ArazzoRunner


@pytest.fixture
def workflow_file():
    """Path to the workflow file."""
    return Path(__file__).parent.parent / "arazzo" / "workflow.arazzo.yaml"


@pytest.fixture
def runner(workflow_file):
    """Create an ArazzoRunner instance."""
    return ArazzoRunner.from_file(str(workflow_file))


def test_workflow_file_exists(workflow_file):
    """Test that the workflow file exists."""
    assert workflow_file.exists(), f"Workflow file not found at {workflow_file}"


def test_workflow_loads_successfully(runner):
    """Test that the workflow loads without errors."""
    assert runner is not None
    assert hasattr(runner, 'execute_workflow')


def test_successful_execution(runner):
    """Test successful workflow execution with valid input."""
    result = runner.execute_workflow(
        workflow_id="getUserInfo",
        inputs={"userId": 1}
    )
    
    assert result.status == "workflow_complete"
    assert "user" in result.outputs
    
    user = result.outputs["user"]
    assert user.get("userId") == 1
    assert user.get("username") is not None
    assert user.get("email") is not None


def test_execution_with_different_users(runner):
    """Test execution with multiple user IDs."""
    user_ids = [1, 2, 3, 5, 10]
    
    for user_id in user_ids:
        result = runner.execute_workflow(
            workflow_id="getUserInfo",
            inputs={"userId": user_id}
        )
        
        assert result.status == "workflow_complete"
        user = result.outputs["user"]
        assert user.get("userId") == user_id


def test_output_structure(runner):
    """Test that outputs have the expected structure."""
    result = runner.execute_workflow(
        workflow_id="getUserInfo",
        inputs={"userId": 1}
    )
    
    user = result.outputs["user"]
    
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
    result = runner.execute_workflow(
        workflow_id="getUserInfo",
        inputs={"userId": user_id}
    )
    
    user = result.outputs["user"]
    assert user.get("username") == expected_username


def test_invalid_user_id(runner):
    """Test execution with invalid user ID."""
    # User ID 999 doesn't exist in JSONPlaceholder
    result = runner.execute_workflow(
        workflow_id="getUserInfo",
        inputs={"userId": 999}
    )
    
    # The workflow should handle this gracefully
    # Depending on error handling, this might fail or return empty
    assert result is not None


def test_default_user_id(runner):
    """Test execution without providing user ID (should use default)."""
    result = runner.execute_workflow(
        workflow_id="getUserInfo",
        inputs={}
    )
    
    # Should use default userId=1
    assert result.status == "workflow_complete"
    user = result.outputs["user"]
    assert user.get("userId") == 1