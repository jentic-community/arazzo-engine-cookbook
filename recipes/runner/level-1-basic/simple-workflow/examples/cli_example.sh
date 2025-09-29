#!/bin/bash
# CLI examples for executing the simple workflow

set -e

echo "=================================="
echo "Arazzo Simple Workflow CLI Examples"
echo "=================================="
echo ""

# Example 1: Basic execution with default input
echo "Example 1: Execute with default input (userId=1)"
echo "--------------------------------------------------"
arazzo-runner execute arazzo/workflow.arazzo.yaml \
  --workflow getUserInfo \
  --input '{"userId": 1}'
echo ""
echo ""

# Example 2: Execute with custom user ID
echo "Example 2: Execute with custom user ID (userId=3)"
echo "--------------------------------------------------"
arazzo-runner execute arazzo/workflow.arazzo.yaml \
  --workflow getUserInfo \
  --input '{"userId": 3}'
echo ""
echo ""

# Example 3: Save output to file
echo "Example 3: Save output to JSON file"
echo "------------------------------------"
arazzo-runner execute arazzo/workflow.arazzo.yaml \
  --workflow getUserInfo \
  --input '{"userId": 2}' \
  --output user_2_result.json
echo "✓ Output saved to user_2_result.json"
cat user_2_result.json | python3 -m json.tool
rm -f user_2_result.json
echo ""
echo ""

# Example 4: Validate workflow before execution
echo "Example 4: Validate workflow specification"
echo "-------------------------------------------"
arazzo-runner validate arazzo/workflow.arazzo.yaml
echo "✓ Workflow is valid"
echo ""
echo ""

# Example 5: Execute with verbose logging
echo "Example 5: Execute with verbose logging"
echo "----------------------------------------"
arazzo-runner execute arazzo/workflow.arazzo.yaml \
  --workflow getUserInfo \
  --input '{"userId": 1}' \
  --verbose
echo ""
echo ""

echo "=================================="
echo "All examples completed successfully!"
echo "=================================="