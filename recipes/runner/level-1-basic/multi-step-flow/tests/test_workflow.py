"""
Tests for the multi-step workflow.

These tests verify:
1. Workflow structure and loading
2. Multi-step execution
3. Data passing between steps
4. Array handling and data extraction
"""

import pytest
import yaml
from pathlib import Path
from arazzo_runner import ArazzoRunner


@pytest.fixture
def workflow_dir():
    """Get the workflow directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def arazzo_doc(workflow_dir):
    """Load the Arazzo workflow document."""
    arazzo_path = workflow_dir / "arazzo" / "workflow.arazzo.yaml"
    with open(arazzo_path) as f:
        return yaml.safe_load(f)


@pytest.fixture
def openapi_spec(workflow_dir):
    """Load the OpenAPI specification."""
    openapi_path = workflow_dir / "openapi" / "jsonplaceholder.openapi.yaml"
    with open(openapi_path) as f:
        return yaml.safe_load(f)


@pytest.fixture
def runner(arazzo_doc, openapi_spec):
    """Create an ArazzoRunner instance."""
    source_descriptions = {
        "jsonPlaceholderAPI": openapi_spec
    }
    return ArazzoRunner(arazzo_doc, source_descriptions)


def test_workflow_file_exists(workflow_dir):
    """Test that the workflow file exists."""
    arazzo_path = workflow_dir / "arazzo" / "workflow.arazzo.yaml"
    assert arazzo_path.exists(), "Workflow file should exist"


def test_openapi_file_exists(workflow_dir):
    """Test that the OpenAPI spec file exists."""
    openapi_path = workflow_dir / "openapi" / "jsonplaceholder.openapi.yaml"
    assert openapi_path.exists(), "OpenAPI spec file should exist"


def test_workflow_loads_successfully(arazzo_doc):
    """Test that the workflow document loads correctly."""
    assert arazzo_doc.get("arazzo") == "1.0.0"
    assert "workflows" in arazzo_doc
    assert len(arazzo_doc["workflows"]) > 0


def test_multi_step_execution(runner):
    """Test that the workflow executes all steps successfully."""
    execution_id = runner.start_workflow("getUserContent", {"userId": 1})
    
    # Execute all steps
    result = None
    for _ in range(10):  # Max 10 iterations to prevent infinite loop
        result = runner.execute_next_step(execution_id)
        if result["status"] == "workflow_complete":
            break
    
    assert result is not None
    assert result["status"] == "workflow_complete"
    assert "outputs" in result


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
    assert "posts" in posts_data
    posts = posts_data.get("posts", [])
    assert isinstance(posts, list), "Posts should be a list"
    assert len(posts) > 0, "Should have at least one post"
    
    # Step 3: Comments (should use first post ID from Step 2)
    comments_data = state.step_outputs["fetchComments"]
    assert "comments" in comments_data
    comments = comments_data.get("comments", [])
    assert isinstance(comments, list), "Comments should be a list"
    assert len(comments) > 0, "Should have at least one comment"


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
    assert isinstance(posts_data["posts"], list)
    
    # Verify Step 3 outputs
    comments_data = state.step_outputs["fetchComments"]
    assert "comments" in comments_data
    assert isinstance(comments_data["comments"], list)


def test_workflow_with_different_users(runner):
    """Test workflow with different user IDs."""
    for user_id in [1, 2, 3]:
        execution_id = runner.start_workflow("getUserContent", {"userId": user_id})
        
        result = None
        for _ in range(10):
            result = runner.execute_next_step(execution_id)
            if result["status"] == "workflow_complete":
                break
        
        assert result["status"] == "workflow_complete"
        state = runner.execution_states[execution_id]
        assert state.step_outputs["fetchUser"].get("userId") == user_id


def test_sequential_execution(runner):
    """Test that steps execute in the correct order."""
    execution_id = runner.start_workflow("getUserContent", {"userId": 1})
    
    step_order = []
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result.get("step_id"):
            step_order.append(result["step_id"])
        if result["status"] == "workflow_complete":
            break
    
    # Verify steps executed in order
    assert "fetchUser" in step_order
    assert "fetchPosts" in step_order
    assert "fetchComments" in step_order
    
    # Verify order
    user_idx = step_order.index("fetchUser")
    posts_idx = step_order.index("fetchPosts")
    comments_idx = step_order.index("fetchComments")
    
    assert user_idx < posts_idx < comments_idx


def test_array_access_in_workflow(runner):
    """Test that the workflow can access array elements correctly."""
    execution_id = runner.start_workflow("getUserContent", {"userId": 1})
    
    result = None
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result["status"] == "workflow_complete":
            break
    
    state = runner.execution_states[execution_id]
    
    # Step 2 should have posts
    posts_data = state.step_outputs["fetchPosts"]
    posts = posts_data.get("posts", [])
    assert len(posts) > 0
    
    # First post should have an ID
    first_post = posts[0]
    assert "id" in first_post
    first_post_id = first_post["id"]
    
    # Step 3 should have fetched comments for that post
    # Verify this by checking comments exist
    comments_data = state.step_outputs["fetchComments"]
    comments = comments_data.get("comments", [])
    assert len(comments) > 0
    
    # All comments should have the same postId
    for comment in comments:
        assert comment.get("postId") == first_post_id


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
    
    # Verify posts were fetched
    posts = state.step_outputs["fetchPosts"].get("posts", [])
    assert len(posts) > 0
    
    # Verify comments were fetched
    comments = state.step_outputs["fetchComments"].get("comments", [])
    assert len(comments) > 0


def test_post_count_accuracy(runner):
    """Test that we can calculate post count from the posts array."""
    execution_id = runner.start_workflow("getUserContent", {"userId": 1})
    
    result = None
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result["status"] == "workflow_complete":
            break
    
    state = runner.execution_states[execution_id]
    posts_data = state.step_outputs["fetchPosts"]
    
    # Get posts array
    posts = posts_data.get("posts", [])
    
    # Verify we have posts
    assert len(posts) > 0
    
    # User 1 should have exactly 10 posts in JSONPlaceholder
    assert len(posts) == 10


def test_workflow_outputs(runner):
    """Test that the workflow produces the expected final outputs."""
    execution_id = runner.start_workflow("getUserContent", {"userId": 1})
    
    result = None
    for _ in range(10):
        result = runner.execute_next_step(execution_id)
        if result["status"] == "workflow_complete":
            break
    
    # Check final workflow outputs
    assert "outputs" in result
    outputs = result["outputs"]
    
    # Should have user, posts, and comments in outputs
    assert "user" in outputs, "Should have user in outputs"
    assert "posts" in outputs, "Should have posts in outputs"
    assert "comments" in outputs, "Should have comments in outputs"
    
    # Verify user output structure
    user_output = outputs["user"]
    assert isinstance(user_output, dict), "User output should be a dict"
    assert "userId" in user_output, f"User output should have userId, got: {user_output.keys()}"
    assert "username" in user_output, "User output should have username"
    
    # Verify posts output
    posts_output = outputs["posts"]
    assert isinstance(posts_output, list), "Posts output should be a list"
    assert len(posts_output) > 0, "Should have at least one post"
    
    # Verify comments output
    comments_output = outputs["comments"]
    assert isinstance(comments_output, list), "Comments output should be a list"
    assert len(comments_output) > 0, "Should have at least one comment"