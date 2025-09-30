#!/usr/bin/env python3
"""
Multi-step workflow example demonstrating data passing between steps.

This script shows how to:
1. Execute a workflow with multiple sequential steps
2. Access outputs from each step
3. See how data flows between steps
"""

import argparse
import sys
import yaml
from pathlib import Path

from arazzo_runner import ArazzoRunner


def main() -> int:
    """Execute the multi-step workflow example."""
    parser = argparse.ArgumentParser(description="Multi-step workflow example")
    parser.add_argument("--user-id", type=int, default=1, help="User ID to fetch (1-10)")
    args = parser.parse_args()
    
    # Define paths
    workflow_file = Path(__file__).parent.parent / "arazzo" / "workflow.arazzo.yaml"
    openapi_file = Path(__file__).parent.parent / "openapi" / "jsonplaceholder.openapi.yaml"
    
    print("=" * 70)
    print("Arazzo Multi-Step Workflow Example")
    print("=" * 70)
    print()
    
    # Check files exist
    if not workflow_file.exists():
        print(f"Error: Workflow file not found at {workflow_file}")
        return 1
    
    if not openapi_file.exists():
        print(f"Error: OpenAPI file not found at {openapi_file}")
        return 1
    
    # Load files
    print(f"Loading workflow from: {workflow_file}")
    try:
        with open(workflow_file) as f:
            arazzo_doc = yaml.safe_load(f)
        
        with open(openapi_file) as f:
            openapi_spec = yaml.safe_load(f)
        
        source_descriptions = {
            "jsonPlaceholderAPI": openapi_spec
        }
        
        runner = ArazzoRunner(arazzo_doc, source_descriptions)
        print("✓ Workflow loaded successfully")
        print()
    except Exception as e:
        print(f"Failed to load workflow: {e}")
        return 1
    
    # Execute workflow
    print(f"Executing workflow for user ID: {args.user_id}")
    print("-" * 70)
    print()
    
    try:
        execution_id = runner.start_workflow("getUserContent", {"userId": args.user_id})
        
        # Execute steps and track progress
        step_count = 0
        result = None
        for _ in range(10):
            result = runner.execute_next_step(execution_id)
            
            if result["status"] == "step_complete":
                step_count += 1
                step_id = result.get("step_id", "unknown")
                print(f"✓ Step {step_count} completed: {step_id}")
            
            if result["status"] == "workflow_complete":
                break
        
        print()
        
        if result["status"] == "workflow_complete":
            print("✓ Workflow completed successfully")
            print()
            
            # Access step outputs
            state = runner.execution_states[execution_id]
            
            # Step 1: User info
            user_data = state.step_outputs["fetchUser"]
            print("Step 1 - User Information:")
            print(f"  User ID:  {user_data.get('userId')}")
            print(f"  Username: {user_data.get('username')}")
            print(f"  Name:     {user_data.get('name')}")
            print(f"  Email:    {user_data.get('email')}")
            print()
            
            # Step 2: Posts
            posts_data = state.step_outputs["fetchPosts"]
            print("Step 2 - User Posts:")
            print(f"  Total Posts:      {posts_data.get('postCount')}")
            print(f"  First Post ID:    {posts_data.get('firstPostId')}")
            print(f"  First Post Title: {posts_data.get('firstPostTitle')}")
            print()
            
            # Step 3: Comments
            comments_data = state.step_outputs["fetchComments"]
            print("Step 3 - Post Comments:")
            print(f"  Comment Count:      {comments_data.get('commentCount')}")
            print(f"  First Comment From: {comments_data.get('firstCommentEmail')}")
            print()
            
            # Show data flow
            print("Data Flow Summary:")
            print("-" * 70)
            print(f"  Input (userId: {args.user_id})")
            print(f"    ↓")
            print(f"  Step 1: Fetched user '{user_data.get('username')}'")
            print(f"    ↓ (passed userId: {user_data.get('userId')})")
            print(f"  Step 2: Found {posts_data.get('postCount')} posts")
            print(f"    ↓ (passed firstPostId: {posts_data.get('firstPostId')})")
            print(f"  Step 3: Found {comments_data.get('commentCount')} comments")
            print(f"    ↓")
            print(f"  Output: Summary generated")
            print()
            
        else:
            print(f"Workflow failed: {result.get('error')}")
            return 1
            
    except Exception as e:
        print(f"Workflow execution failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("=" * 70)
    print("Example completed successfully!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())