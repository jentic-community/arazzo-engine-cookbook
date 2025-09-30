#!/bin/bash
# CLI examples for executing the multi-step workflow

set -e

echo "======================================"
echo "Arazzo Multi-Step Workflow CLI Examples"
echo "======================================"
echo ""

# Example 1: Basic execution with default input
echo "Example 1: Execute with default input (userId=1)"
echo "--------------------------------------------------"
arazzo-runner execute-workflow arazzo/workflow.arazzo.yaml \
  --workflow-id getUserContent \
  --inputs '{"userId": 1}'
echo ""
echo ""

# Example 2: Execute with custom user ID
echo "Example 2: Execute with custom user ID (userId=3)"
echo "--------------------------------------------------"
arazzo-runner execute-workflow arazzo/workflow.arazzo.yaml \
  --workflow-id getUserContent \
  --inputs '{"userId": 3}'
echo ""
echo ""

# Example 3: Save output to file
echo "Example 3: Save output to JSON file"
echo "------------------------------------"
arazzo-runner execute-workflow arazzo/workflow.arazzo.yaml \
  --workflow-id getUserContent \
  --inputs '{"userId": 2}' \
  --output user_2_content.json
echo "✓ Output saved to user_2_content.json"
cat user_2_content.json | python3 -m json.tool
rm -f user_2_content.json
echo ""
echo ""

# Example 4: Validate workflow before execution
echo "Example 4: Validate workflow specification"
echo "-------------------------------------------"
python3 -c "import yaml; yaml.safe_load(open('arazzo/workflow.arazzo.yaml'))" && \
  echo "✓ Workflow is valid YAML"
echo ""
echo ""

# Example 5: List workflows in the document
echo "Example 5: List available workflows"
echo "------------------------------------"
arazzo-runner list-workflows arazzo/workflow.arazzo.yaml
echo ""
echo ""

# Example 6: Describe the workflow
echo "Example 6: Describe workflow structure"
echo "---------------------------------------"
arazzo-runner describe-workflow arazzo/workflow.arazzo.yaml \
  --workflow-id getUserContent
echo ""
echo ""

# Example 7: Execute for multiple users
echo "Example 7: Execute for multiple users"
echo "--------------------------------------"
for user_id in 1 2 3; do
  echo ""
  echo "Fetching content for user $user_id..."
  arazzo-runner execute-workflow arazzo/workflow.arazzo.yaml \
    --workflow-id getUserContent \
    --inputs "{\"userId\": $user_id}" 2>&1 | \
    grep -E "(username|postCount|commentCount)" || true
done
echo ""
echo ""

echo "======================================"
echo "All examples completed successfully!"
echo "======================================"