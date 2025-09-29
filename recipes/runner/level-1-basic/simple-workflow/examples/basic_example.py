#!/usr/bin/env python3
"""
Basic example demonstrating Arazzo workflow execution using the Python API.
"""

import yaml
import sys
from pathlib import Path

from arazzo_runner import ArazzoRunner


def main() -> int:
    """Execute the simple workflow example."""
    # Define paths
    workflow_file = Path(__file__).parent.parent / "arazzo" / "workflow.arazzo.yaml"
    openapi_file = Path(__file__).parent.parent / "openapi" / "jsonplaceholder.openapi.yaml"
    
    print("=" * 60)
    print("Arazzo Simple Workflow Example")
    print("=" * 60)
    print()
    
    # Check files exist
    if not workflow_file.exists():
        print(f"❌ Error: Workflow file not found at {workflow_file}")
        return 1
    
    if not openapi_file.exists():
        print(f"❌ Error: OpenAPI file not found at {openapi_file}")
        return 1
    
    # Load files
    print(f"📂 Loading workflow from: {workflow_file}")
    try:
        with open(workflow_file) as f:
            arazzo_doc = yaml.safe_load(f)
        
        with open(openapi_file) as f:
            openapi_spec = yaml.safe_load(f)
        
        source_descriptions = {
            "jsonPlaceholderAPI": openapi_spec
        }
        
        runner = ArazzoRunner(arazzo_doc, source_descriptions)
        print("✅ Workflow loaded successfully")
        print()
    except Exception as e:
        print(f"❌ Failed to load workflow: {e}")
        return 1
    
    # Execute workflow
    print("🚀 Executing workflow with userId=1...")
    try:
        execution_id = runner.start_workflow("getUserInfo", {"userId": 1})
        
        # Execute steps
        result = None
        for _ in range(10):
            result = runner.execute_next_step(execution_id)
            if result["status"] == "workflow_complete":
                break
        
        if result["status"] == "workflow_complete":
            print("✅ Workflow completed successfully")
            print()
            
            state = runner.execution_states[execution_id]
            user = state.step_outputs["fetchUser"]
            
            print("User Information:")
            print("-" * 40)
            print(f"  ID:       {user.get('userId')}")
            print(f"  Name:     {user.get('name')}")
            print(f"  Username: {user.get('username')}")
            print(f"  Email:    {user.get('email')}")
            print(f"  Phone:    {user.get('phone')}")
            print(f"  Website:  {user.get('website')}")
            print()
        else:
            print(f"❌ Workflow failed: {result.get('error')}")
            return 1
            
    except Exception as e:
        print(f"❌ Workflow execution failed: {e}")
        return 1
    
    print("=" * 60)
    print("🎉 Example completed successfully!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())