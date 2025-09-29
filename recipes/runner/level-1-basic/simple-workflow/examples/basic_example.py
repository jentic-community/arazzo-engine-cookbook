#!/usr/bin/env python3
"""
Basic example demonstrating Arazzo workflow execution using the Python API.

This script shows how to:
1. Load an Arazzo workflow from a file
2. Execute the workflow with inputs
3. Access and process the outputs
4. Handle different user IDs
"""

import json
import sys
from pathlib import Path

from arazzo_runner import ArazzoRunner


def print_separator(title: str = "") -> None:
    """Print a formatted separator line."""
    width = 60
    if title:
        padding = (width - len(title) - 2) // 2
        print("=" * padding + f" {title} " + "=" * padding)
    else:
        print("=" * width)


def print_user_info(user: dict) -> None:
    """Print user information in a formatted way."""
    print("User Information:")
    print("-" * 40)
    print(f"  ID:       {user.get('userId', 'N/A')}")
    print(f"  Name:     {user.get('name', 'N/A')}")
    print(f"  Username: {user.get('username', 'N/A')}")
    print(f"  Email:    {user.get('email', 'N/A')}")
    print(f"  Phone:    {user.get('phone', 'N/A')}")
    print(f"  Website:  {user.get('website', 'N/A')}")


def main() -> int:
    """Execute the simple workflow example."""
    # Define paths
    workflow_file = Path(__file__).parent.parent / "arazzo" / "workflow.arazzo.yaml"
    
    print_separator("Arazzo Simple Workflow Example")
    print()
    
    # Check if workflow file exists
    if not workflow_file.exists():
        print(f"❌ Error: Workflow file not found at {workflow_file}")
        return 1
    
    # Load the workflow
    print(f"📂 Loading workflow from: {workflow_file}")
    try:
        runner = ArazzoRunner.from_file(str(workflow_file))
        print("✅ Workflow loaded successfully")
        print()
    except Exception as e:
        print(f"❌ Failed to load workflow: {e}")
        return 1
    
    # Execute the workflow with default input (user ID 1)
    print("🚀 Executing workflow with userId=1...")
    try:
        result = runner.execute_workflow(
            workflow_id="getUserInfo",
            inputs={"userId": 1}
        )
        
        # Check execution status
        if result.status == "workflow_complete":
            print("✅ Workflow completed successfully")
            print()
            
            # Extract and display user information
            user = result.outputs.get("user", {})
            print_user_info(user)
            print()
            
        else:
            print(f"❌ Workflow failed with status: {result.status}")
            if result.error:
                print(f"   Error: {result.error}")
            return 1
            
    except Exception as e:
        print(f"❌ Workflow execution failed: {e}")
        return 1
    
    # Execute workflow with different user IDs
    print("📋 Fetching additional users...")
    print("-" * 40)
    
    user_ids = [2, 3, 5]
    for user_id in user_ids:
        try:
            result = runner.execute_workflow(
                workflow_id="getUserInfo",
                inputs={"userId": user_id}
            )
            
            if result.status == "workflow_complete":
                user = result.outputs.get("user", {})
                username = user.get('username', 'N/A')
                name = user.get('name', 'N/A')
                print(f"✅ User {user_id}: {name} (@{username})")
            else:
                print(f"❌ User {user_id}: Failed to fetch")
                
        except Exception as e:
            print(f"❌ User {user_id}: Error - {e}")
    
    print()
    print_separator()
    print("🎉 Example completed successfully!")
    print_separator()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())