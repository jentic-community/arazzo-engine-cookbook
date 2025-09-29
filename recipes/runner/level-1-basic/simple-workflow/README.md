# Simple Workflow Recipe

**Level**: Basic  
**Type**: Runner  
**Estimated Time**: 15 minutes

## Overview

This recipe demonstrates the fundamentals of executing an Arazzo workflow. You'll learn how to:

- Define a simple workflow with one API call
- Execute the workflow using arazzo-runner
- Pass inputs to the workflow
- Extract outputs from API responses
- Validate workflow execution

## Use Case

Execute a simple API call to fetch information about a user from the JSONPlaceholder API (a free fake REST API for testing).

## Prerequisites

- Python 3.11+
- `uv` package manager installed
- Internet connection (for accessing the test API)

## Project Structure

```
simple-workflow/
├── README.md                       # This file
├── Makefile                        # Convenient commands
├── pyproject.toml                  # Recipe dependencies
├── .env.example                    # Environment template
├── arazzo/
│   └── workflow.arazzo.yaml        # Workflow definition
├── openapi/
│   └── jsonplaceholder.openapi.yaml # API specification
├── examples/
│   ├── basic_example.py            # Python example
│   └── cli_example.sh              # CLI example
└── tests/
    └── test_workflow.py            # Workflow tests
```

## Quick Start

### 1. Setup

From the recipe directory:

```bash
# Install dependencies
make install

# Verify setup
make check
```

### 2. Run the Workflow

```bash
# Execute with default inputs
make run

# Execute with custom input
make run INPUT='{"userId": 2}'
```

### 3. Explore

```bash
# View the workflow definition
cat arazzo/workflow.arazzo.yaml

# View the OpenAPI spec
cat openapi/jsonplaceholder.openapi.yaml

# Run tests
make test
```

## Understanding the Workflow

### Arazzo Workflow Definition

The workflow is defined in `arazzo/workflow.arazzo.yaml`:

```yaml
arazzo: "1.0.0"
info:
  title: Simple User Fetch Workflow
  version: 1.0.0
  description: Fetch user information from JSONPlaceholder API

sourceDescriptions:
  - name: jsonPlaceholderAPI
    url: ./openapi/jsonplaceholder.openapi.yaml
    type: openapi

workflows:
  - workflowId: getUserInfo
    description: Fetch information about a specific user
    inputs:
      type: object
      properties:
        userId:
          type: integer
          description: The ID of the user to fetch
          default: 1
    steps:
      - stepId: fetchUser
        operationId: getUser
        parameters:
          - name: id
            in: path
            value: $inputs.userId
        successCriteria:
          - condition: $statusCode == 200
        outputs:
          userId: $response.body.id
          username: $response.body.username
          email: $response.body.email
    outputs:
      user: $steps.fetchUser.outputs
```

### Key Concepts

1. **Source Descriptions**: References to OpenAPI specifications
2. **Workflows**: Named sequences of steps
3. **Inputs**: Parameters that can be passed to the workflow
4. **Steps**: Individual API operations to execute
5. **Success Criteria**: Conditions that determine if a step succeeded
6. **Outputs**: Data to extract from responses

## Running from Python

```python
from arazzo_runner import ArazzoRunner

# Load the workflow
runner = ArazzoRunner.from_file("arazzo/workflow.arazzo.yaml")

# Execute with inputs
result = runner.execute_workflow(
    workflow_id="getUserInfo",
    inputs={"userId": 1}
)

# Access outputs
print(f"User: {result.outputs['user']['username']}")
print(f"Email: {result.outputs['user']['email']}")
```

## Running from CLI

```bash
# Basic execution
arazzo-runner execute-workflow arazzo/workflow.arazzo.yaml \
  --workflow-id getUserInfo \
  --inputs '{"userId": 1}'

# With output file
arazzo-runner execute-workflow arazzo/workflow.arazzo.yaml \
  --workflow-id getUserInfo \
  --inputs '{"userId": 2}' \
  --output result.json
```

## Expected Output

When successful, you should see output similar to:

```json
{
  "status": "workflow_complete",
  "workflow_id": "getUserInfo",
  "outputs": {
    "user": {
      "userId": 1,
      "username": "Bret",
      "email": "Sincere@april.biz"
    }
  }
}
```

## Testing

The recipe includes tests to verify workflow execution:

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific test
pytest tests/test_workflow.py::test_successful_execution -v
```

## Troubleshooting

### Common Issues

1. **API not responding**
   - Check internet connection
   - Verify the JSONPlaceholder API is accessible

2. **Workflow validation errors**
   - Ensure YAML syntax is correct
   - Verify all referenced files exist

3. **Module not found errors**
   - Run `make install` to install dependencies
   - Activate virtual environment

## Next Steps

After completing this recipe, explore:

- **multi-step-flow**: Chain multiple API calls together
- **error-handling**: Handle API failures gracefully
- **authentication**: Work with authenticated APIs

## Learning Resources

- [Arazzo Specification](https://github.com/OAI/Arazzo-Specification)
- [Arazzo Runner Documentation](https://github.com/jentic/arazzo-engine/tree/main/runner)
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com/)

## Contributing

Found an issue or have a suggestion? Please open an issue or submit a pull request!

## License

Apache 2.0 - See LICENSE file for details