# Multi-Step Flow Recipe

**Level**: Basic  
**Type**: Runner  
**Estimated Time**: 20 minutes

## Overview

This recipe demonstrates how to chain multiple API calls together, passing data between steps. You'll learn how to:

- Create workflows with multiple sequential steps
- Pass outputs from one step as inputs to another
- Use Arazzo expression syntax for data references
- Handle dependencies between workflow steps
- Extract and transform data between operations

## Use Case

Fetch a user's information, then retrieve all posts by that user, and finally get comments for the first post. This demonstrates a common pattern in API orchestration where subsequent calls depend on data from previous responses.

**Workflow Flow**:
1. Get user information by ID
2. Use the user's ID to fetch all their posts
3. Use the first post's ID to fetch its comments

## Prerequisites

- Python 3.11+
- `uv` package manager installed
- Internet connection (for accessing the test API)
- Completion of simple-workflow recipe (recommended)

## Project Structure

```
multi-step-flow/
├── README.md                       # This file
├── Makefile                        # Convenient commands
├── pyproject.toml                  # Recipe dependencies
├── .env.example                    # Environment template
├── arazzo/
│   └── workflow.arazzo.yaml        # Multi-step workflow definition
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

```bash
# Install dependencies
make install

# Verify setup
make check
```

### 2. Run the Workflow

```bash
# Execute with default user (ID 1)
make run

# Execute with specific user
make run INPUT='{"userId": 2}'
```

### 3. Explore

```bash
# View the workflow definition
cat arazzo/workflow.arazzo.yaml

# Run tests
make test
```

## Understanding the Workflow

### Step-by-Step Breakdown

#### Step 1: Fetch User
```yaml
- stepId: fetchUser
  operationId: getUser
  parameters:
    - name: id
      in: path
      value: $inputs.userId
  outputs:
    userId: $response.body.id
    username: $response.body.username
```

Fetches user information and extracts the user ID for subsequent steps.

#### Step 2: Fetch User's Posts
```yaml
- stepId: fetchPosts
  operationId: getUserPosts
  parameters:
    - name: userId
      in: query
      value: $steps.fetchUser.outputs.userId  # Reference Step 1 output
  outputs:
    posts: $response.body
    firstPostId: $response.body[0].id
```

Uses the user ID from Step 1 to fetch all posts, then extracts the first post's ID.

#### Step 3: Fetch Post Comments
```yaml
- stepId: fetchComments
  operationId: getPostComments
  parameters:
    - name: postId
      in: query
      value: $steps.fetchPosts.outputs.firstPostId  # Reference Step 2 output
  outputs:
    comments: $response.body
    commentCount: $response.body.length
```

Uses the first post ID from Step 2 to fetch comments for that post.

### Key Concepts

**1. Step Dependencies**
Steps execute in order, and later steps can reference outputs from earlier steps:
```yaml
value: $steps.previousStepId.outputs.outputName
```

**2. Data Extraction**
Use JSONPath-like expressions to extract data from responses:
```yaml
outputs:
  firstItem: $response.body[0]        # First array element
  nestedValue: $response.body.user.id # Nested object property
  arrayLength: $response.body.length  # Array length
```

**3. Output Composition**
Final workflow outputs can combine data from multiple steps:
```yaml
outputs:
  user: $steps.fetchUser.outputs
  postCount: $steps.fetchPosts.outputs.posts.length
  commentCount: $steps.fetchComments.outputs.commentCount
```

## Running from Python

```python
import yaml
from arazzo_runner import ArazzoRunner

# Load workflow and API spec
with open("arazzo/workflow.arazzo.yaml") as f:
    arazzo_doc = yaml.safe_load(f)

with open("openapi/jsonplaceholder.openapi.yaml") as f:
    openapi_spec = yaml.safe_load(f)

source_descriptions = {
    "jsonPlaceholderAPI": openapi_spec
}

# Create runner
runner = ArazzoRunner(arazzo_doc, source_descriptions)

# Execute workflow
execution_id = runner.start_workflow("getUserContent", {"userId": 1})

# Execute all steps
result = None
for _ in range(10):
    result = runner.execute_next_step(execution_id)
    if result["status"] == "workflow_complete":
        break

# Access results
state = runner.execution_states[execution_id]
print(f"User: {state.step_outputs['fetchUser']['username']}")
print(f"Posts: {len(state.step_outputs['fetchPosts']['posts'])}")
print(f"Comments on first post: {state.step_outputs['fetchComments']['commentCount']}")
```

## Running from CLI

```bash
# Basic execution
arazzo-runner execute-workflow arazzo/workflow.arazzo.yaml \
  --workflow-id getUserContent \
  --inputs '{"userId": 1}'

# With output file
arazzo-runner execute-workflow arazzo/workflow.arazzo.yaml \
  --workflow-id getUserContent \
  --inputs '{"userId": 2}' \
  --output result.json
```

## Expected Output

When successful, the workflow returns:

```json
{
  "status": "workflow_complete",
  "workflow_id": "getUserContent",
  "outputs": {
    "summary": {
      "username": "Bret",
      "postCount": 10,
      "firstPostCommentCount": 5
    }
  }
}
```

## Testing

```bash
# Run all tests
make test

# Run specific test
pytest tests/test_workflow.py::test_data_passing -v

# Run with coverage
make test-coverage
```

## Common Patterns

### Pattern 1: Sequential Dependencies
Each step depends on the previous:
```
Step 1 → Step 2 → Step 3
```

### Pattern 2: Parallel with Merge
Multiple steps use data from one source:
```
      → Step 2 →
Step 1            → Step 4
      → Step 3 →
```

### Pattern 3: Conditional Branching
Steps execute based on previous results (covered in conditional-logic recipe).

## Troubleshooting

### Issue: "Cannot read property of undefined"
**Cause**: Referenced output doesn't exist or step failed  
**Solution**: Check that previous step completed successfully and output name is correct

### Issue: "Array index out of bounds"
**Cause**: Trying to access array element that doesn't exist  
**Solution**: Add validation or use success criteria to check array length

### Issue: Steps executing out of order
**Cause**: Arazzo runner executes steps sequentially by definition  
**Note**: This shouldn't happen; if it does, there's a bug in the runner

## Next Steps

After completing this recipe, explore:

- **error-handling**: Handle failures gracefully with retry logic
- **conditional-logic**: Branch execution based on step results
- **parameter-mapping**: Complex data transformations between steps

## Learning Resources

- [Arazzo Specification - Steps](https://github.com/OAI/Arazzo-Specification#step-object)
- [Arazzo Expression Syntax](https://github.com/OAI/Arazzo-Specification#runtime-expressions)
- [JSONPlaceholder Guide](https://jsonplaceholder.typicode.com/guide/)

## Contributing

Found an issue or have a suggestion? Please open an issue or submit a pull request!

## License

Apache 2.0 - See LICENSE file for details