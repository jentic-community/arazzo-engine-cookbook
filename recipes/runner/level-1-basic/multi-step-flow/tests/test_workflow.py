"""Tests for the multi-step flow recipe."""

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
    with open(workflow_file) as f:
        arazzo_doc = yaml.safe_load(f)
    
    with open(openapi_file) as f:
        openapi_spec = yaml.safe_load(f)
    
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


def test_multi_step_execution(runner):
    """Test successful execution of all three steps."""
    execution_id = runner.start_workflow("getUserContent", {"userId": 1})
    
    # Execute all steps
    result = None
    step_count = 0
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result["status"] == "step_complete":
            step_count += 1
        if result["status"] == "workflow_complete":
            break
    
    assert result["status"] == "workflow_complete"
    assert step_count == 3, "Should have completed exactly 3 steps"


def test_data_passing_between_steps(runner):
    """Test that data is correctly passed between steps."""
    execution_id = runner.start_workflow("getUserContent", {"userId": 1})
    
    # Execute all steps
    result = None
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result["status"] == "workflow_complete":
            break
    
    state = runner.execution_states[execution_id]
    
    # Step 1: User data
    user_data = state.step_outputs["fetchUser"]
    assert user_data.get("userId") == 1
    assert user_data.get("username") is not None
    
    # Step 2: Posts (should use userId from Step 1)
    posts_data = state.step_outputs["fetchPosts"]
    assert posts_data.get("postCount") is not None
    assert posts_data.get("postCount") > 0
    assert posts_data.get("firstPostId") is not None
    
    # Step 3: Comments (should use firstPostId from Step 2)
    comments_data = state.step_outputs["fetchComments"]
    assert comments_data.get("commentCount") is not None
    assert comments_data.get("commentCount") > 0


def test_step_output_structure(runner):
    """Test that each step produces expected outputs."""
    execution_id = runner.start_workflow("getUserContent", {"userId": 1})
    
    result = None
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result["status"] == "workflow_complete":
            break
    
    state = runner.execution_states[execution_id]
    
    # Verify Step 1 outputs
    user_data = state.step_outputs["fetchUser"]
    assert "userId" in user_data
    assert "username" in user_data
    assert "name" in user_data
    assert "email" in user_data
    
    # Verify Step 2 outputs
    posts_data = state.step_outputs["fetchPosts"]
    assert "posts" in posts_data
    assert "postCount" in posts_data
    assert "firstPostId" in posts_data
    assert "firstPostTitle" in posts_data
    
    # Verify Step 3 outputs
    comments_data = state.step_outputs["fetchComments"]
    assert "comments" in comments_data
    assert "commentCount" in comments_data
    assert "firstCommentEmail" in comments_data


def test_workflow_with_different_users(runner):
    """Test workflow execution with different user IDs."""
    user_ids = [1, 2, 3]
    
    for user_id in user_ids:
        execution_id = runner.start_workflow("getUserContent", {"userId": user_id})
        
        result = None
        for _ in range(10):
            result = runner.execute_next_step(execution_id)
            if result["status"] == "workflow_complete":
                break
        
        assert result["status"] == "workflow_complete"
        state = runner.execution_states[execution_id]
        
        # Verify user ID matches input
        user_data = state.step_outputs["fetchUser"]
        assert user_data.get("userId") == user_id


def test_sequential_execution(runner):
    """Test that steps execute in the correct order."""
    execution_id = runner.start_workflow("getUserContent", {"userId": 1})
    
    executed_steps = []
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result["status"] == "step_complete":
            executed_steps.append(result.get("step_id"))
        if result["status"] == "workflow_complete":
            break
    
    # Verify steps executed in order
    assert executed_steps == ["fetchUser", "fetchPosts", "fetchComments"]


def test_array_access_in_outputs(runner):
    """Test that array access works in output expressions."""
    execution_id = runner.start_workflow("getUserContent", {"userId": 1})
    
    result = None
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result["status"] == "workflow_complete":
            break
    
    state = runner.execution_states[execution_id]
    
    # Step 2 should extract first post ID from array
    posts_data = state.step_outputs["fetchPosts"]
    first_post_id = posts_data.get("firstPostId")
    assert first_post_id is not None
    assert isinstance(first_post_id, int)
    
    # Step 3 should extract first comment email from array
    comments_data = state.step_outputs["fetchComments"]
    first_comment_email = comments_data.get("firstCommentEmail")
    assert first_comment_email is not None
    assert "@" in first_comment_email


@pytest.mark.parametrize("user_id", [1, 2, 3, 5, 10])
def test_workflow_with_various_users(runner, user_id):
    """Test workflow with various user IDs."""
    execution_id = runner.start_workflow("getUserContent", {"userId": user_id})
    
    result = None
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result["status"] == "workflow_complete":
            break
    
    assert result["status"] == "workflow_complete"
    
    state = runner.execution_states[execution_id]
    assert state.step_outputs["fetchUser"].get("userId") == user_id
    assert state.step_outputs["fetchPosts"].get("postCount") > 0
    assert state.step_outputs["fetchComments"].get("commentCount") >= 0


def test_post_count_accuracy(runner):
    """Test that post count matches actual posts array length."""
    execution_id = runner.start_workflow("getUserContent", {"userId": 1})
    
    result = None
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result["status"] == "workflow_complete":
            break
    
    state = runner.execution_states[execution_id]
    posts_data = state.step_outputs["fetchPosts"]
    
    # Verify count matches array length
    posts = posts_data.get("posts", [])
    post_count = posts_data.get("postCount", 0)
    assert len(posts) == post_count