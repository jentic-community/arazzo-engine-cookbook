# Contributing to Arazzo Engine Cookbook

Thank you for your interest in contributing to the Arazzo Engine Cookbook! This document provides guidelines and instructions for contributing recipes, improvements, and fixes.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Recipe Contributions](#recipe-contributions)
- [Development Workflow](#development-workflow)
- [Recipe Standards](#recipe-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.11 or higher
- uv package manager
- Git
- GitHub account

### Setup Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/arazzo-engine-cookbook.git
cd arazzo-engine-cookbook

# Setup environment
make setup

# Activate virtual environment
source .venv/bin/activate

# Verify setup
make check-env
```

## Recipe Contributions

### Types of Contributions

We welcome:

1. **New Recipes**: Practical examples demonstrating Arazzo workflows
2. **Recipe Improvements**: Enhancements to existing recipes
3. **Bug Fixes**: Corrections to errors in recipes
4. **Documentation**: Improvements to READMEs, guides, and comments
5. **Tests**: Additional test coverage for recipes

### Choosing a Recipe Topic

Good recipe topics are:

- **Practical**: Solve real-world API orchestration problems
- **Clear**: Have well-defined learning objectives
- **Complete**: Include all necessary files and documentation
- **Tested**: Can be verified to work correctly
- **Documented**: Easy for others to understand and use

### Recipe Levels

- **Level 1 (Basic)**: Fundamental concepts, single API calls, basic flows
- **Level 2 (Intermediate)**: Multi-API orchestration, authentication, error handling
- **Level 3 (Advanced)**: Complex workflows, production patterns, optimizations

## Development Workflow

### 1. Create an Issue

Before starting work, create an issue describing:
- What the recipe will demonstrate
- Why it's useful
- Which level it belongs to
- Any special requirements or dependencies

### 2. Fork and Branch

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/arazzo-engine-cookbook.git
cd arazzo-engine-cookbook

# Create a feature branch
git checkout -b recipe/your-recipe-name
```

### 3. Create Recipe Structure

```bash
# Use the Makefile to create the skeleton
make new-recipe \
  RECIPE_TARGET=your-recipe-name \
  RECIPE_LEVEL=level-1-basic \
  RECIPE_TYPE=runner
```

### 4. Implement the Recipe

Follow the [Recipe Standards](#recipe-standards) below.

### 5. Test Your Recipe

```bash
cd recipes/runner/level-1-basic/your-recipe-name

# Run tests
make test

# Validate structure
make validate

# Try the example
make run
```

### 6. Document Your Recipe

Ensure your README includes:
- Clear description and objectives
- Prerequisites
- Step-by-step instructions
- Example usage
- Troubleshooting section

### 7. Submit Pull Request

```bash
git add .
git commit -m "Add recipe: your-recipe-name"
git push origin recipe/your-recipe-name
```

Then create a pull request on GitHub.

## Recipe Standards

### Required Files

Every runner recipe must include:

```
recipe-name/
├── README.md                       # Complete documentation
├── Makefile                        # Convenient commands
├── pyproject.toml                  # Dependencies
├── .env.example                    # Environment template (if needed)
├── arazzo/
│   └── workflow.arazzo.yaml        # Arazzo workflow
├── openapi/
│   └── api.openapi.yaml           # OpenAPI spec(s)
├── examples/
│   ├── basic_example.py           # Python example
│   └── cli_example.sh             # CLI example
└── tests/
    └── test_workflow.py           # Tests
```

### Arazzo Workflow Standards

Workflows must:

- Follow Arazzo 1.0.0 specification
- Include clear descriptions for all steps
- Define success criteria
- Document all inputs and outputs
- Use meaningful IDs for workflows and steps
- Include error handling where appropriate

Example:

```yaml
arazzo: "1.0.0"
info:
  title: Clear Descriptive Title
  version: 1.0.0
  description: |
    Detailed description of what this workflow does
    and when to use it.

sourceDescriptions:
  - name: descriptiveName
    url: ./openapi/api.openapi.yaml
    type: openapi

workflows:
  - workflowId: descriptiveWorkflowId
    description: What this workflow accomplishes
    inputs:
      type: object
      properties:
        paramName:
          type: string
          description: What this parameter is for
    steps:
      - stepId: descriptiveStepId
        description: What this step does
        operationId: apiOperationId
        successCriteria:
          - condition: $statusCode == 200
        outputs:
          outputName: $response.body.field
    outputs:
      resultName: $steps.stepId.outputs.outputName
```

### Python Code Standards

Follow PEP 8 and project conventions:

- Use type hints
- Include docstrings
- Handle errors gracefully
- Use meaningful variable names
- Keep functions focused and small
- Add comments for complex logic

```python
def execute_workflow(workflow_id: str, inputs: dict) -> WorkflowResult:
    """
    Execute an Arazzo workflow with provided inputs.
    
    Args:
        workflow_id: Identifier of the workflow to execute
        inputs: Dictionary of input parameters
        
    Returns:
        WorkflowResult containing outputs and status
        
    Raises:
        WorkflowExecutionError: If workflow execution fails
    """
    # Implementation
```

### Makefile Standards

Include these standard targets:

```makefile
install:    # Install dependencies
check:      # Verify setup
validate:   # Validate workflow
run:        # Execute workflow
test:       # Run tests
clean:      # Clean artifacts
help:       # Show help (default)
```

## Testing Guidelines

### Test Coverage

Every recipe must include tests for:

1. **Workflow Validation**: Spec is valid Arazzo
2. **Successful Execution**: Workflow completes successfully
3. **Output Verification**: Outputs match expected structure
4. **Error Handling**: Failures are handled gracefully
5. **Edge Cases**: Boundary conditions work correctly

### Test Structure

```python
import pytest
from pathlib import Path
from arazzo_runner import ArazzoRunner

@pytest.fixture
def workflow_file():
    """Path to workflow file."""
    return Path(__file__).parent.parent / "arazzo" / "workflow.arazzo.yaml"

@pytest.fixture
def runner(workflow_file):
    """Create runner instance."""
    return ArazzoRunner.from_file(str(workflow_file))

def test_workflow_loads(runner):
    """Test workflow loads successfully."""
    assert runner is not None

def test_successful_execution(runner):
    """Test workflow executes successfully."""
    result = runner.execute_workflow(
        workflow_id="testWorkflow",
        inputs={"param": "value"}
    )
    assert result.status == "workflow_complete"
    assert "output" in result.outputs

def test_output_structure(runner):
    """Test outputs have correct structure."""
    result = runner.execute_workflow(
        workflow_id="testWorkflow",
        inputs={"param": "value"}
    )
    output = result.outputs["output"]
    assert isinstance(output, dict)
    assert "field" in output
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific test
pytest tests/test_workflow.py::test_name -v
```

## Documentation Standards

### README Structure

Every recipe README must include:

```markdown
# Recipe Title

**Level**: Basic/Intermediate/Advanced
**Type**: Runner/Generator
**Estimated Time**: X minutes

## Overview
Brief description and learning objectives

## Use Case
Real-world scenario this recipe addresses

## Prerequisites
- Required knowledge
- Required tools
- API keys needed

## Quick Start
Steps to run in < 5 minutes

## Understanding the Workflow
Detailed explanation of components

## Running from Python
Python API examples

## Running from CLI
Command-line examples

## Expected Output
What successful execution looks like

## Testing
How to test the recipe

## Troubleshooting
Common issues and solutions

## Next Steps
Related recipes to explore

## Resources
Links to relevant documentation
```

### Code Comments

- Comment complex logic
- Explain non-obvious decisions
- Document API-specific quirks
- Include TODO notes for improvements

### Examples

Include both Python and CLI examples that:
- Are complete and runnable
- Include error handling
- Show common variations
- Are well-commented

## Pull Request Process

### Before Submitting

- [ ] Recipe follows all standards
- [ ] All tests pass
- [ ] Documentation is complete
- [ ] Code is formatted (run `make format`)
- [ ] No linting errors (run `make lint`)
- [ ] Recipe validated (run `make validate-recipe`)

### PR Description Template

```markdown
## Description
Brief description of the recipe

## Type of Change
- [ ] New recipe
- [ ] Recipe improvement
- [ ] Bug fix
- [ ] Documentation update

## Recipe Details
- **Name**: recipe-name
- **Level**: Basic/Intermediate/Advanced
- **Type**: Runner/Generator

## Learning Objectives
What users will learn from this recipe

## Checklist
- [ ] Recipe follows structure standards
- [ ] All required files included
- [ ] Tests pass
- [ ] Documentation complete
- [ ] Examples work
- [ ] Validated with `make validate-recipe`

## Additional Notes
Any special considerations or requirements
```

### Review Process

1. Automated checks run (tests, linting, validation)
2. Maintainer reviews code and documentation
3. Community feedback collected
4. Changes requested if needed
5. Once approved, PR is merged

### After Merge

- Your recipe appears in the cookbook
- You're added to CONTRIBUTORS.md
- Recipe is announced in release notes

## Style Guide

### Naming Conventions

- **Recipes**: lowercase with hyphens (e.g., `multi-api-orchestration`)
- **Files**: lowercase with underscores (e.g., `test_workflow.py`)
- **IDs**: camelCase (e.g., `getUserInfo`, `fetchData`)
- **Variables**: snake_case (e.g., `user_id`, `api_key`)

### Writing Style

- Use clear, simple language
- Write in present tense
- Use active voice
- Be concise but complete
- Include examples

### Code Style

- Run `make format` before committing
- Follow PEP 8 for Python
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable names

## Getting Help

### Resources

- [Arazzo Specification](https://github.com/OAI/Arazzo-Specification)
- [Arazzo Engine Docs](https://github.com/jentic/arazzo-engine)
- [Cookbook README](README.md)

### Community

- **Discord**: [Join chat](https://discord.gg/TdbWXZsUSm)
- **Discussions**: [GitHub Discussions](https://github.com/jentic/arazzo-engine-cookbook/discussions)
- **Issues**: [Report problems](https://github.com/jentic/arazzo-engine-cookbook/issues)

### Questions

For contribution questions:
1. Check existing issues and discussions
2. Ask in Discord
3. Open a discussion on GitHub

## Recognition

Contributors are recognized:
- In CONTRIBUTORS.md
- In release notes
- On the project website
- In social media announcements

Thank you for contributing to the Arazzo Engine Cookbook!

---

**Questions about contributing?** Open a discussion or ask in Discord!