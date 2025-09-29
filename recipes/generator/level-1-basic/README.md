# Arazzo Generator Recipes (Coming Soon)

This directory will contain recipes for using the Arazzo Generator to create workflow definitions from OpenAPI specifications using AI-powered analysis.

## Current Status

Generator recipes are under development. This placeholder structure has been created to guide future development.

## Planned Recipe Structure

```
recipes/generator/
├── level-1-basic/
│   ├── simple-generation/       # Generate basic workflow from OpenAPI
│   ├── multi-endpoint/          # Generate multi-step workflows
│   └── custom-prompts/          # Customize generation with prompts
├── level-2-intermediate/
│   ├── workflow-optimization/   # Optimize generated workflows
│   ├── pattern-recognition/     # Identify common patterns
│   └── batch-generation/        # Generate multiple workflows
└── level-3-advanced/
    ├── custom-models/           # Use fine-tuned models
    ├── workflow-templates/      # Generate from templates
    └── ci-cd-integration/       # Integrate into pipelines
```

## Planned Recipes

### Level 1 - Basic

#### simple-generation
Generate a basic Arazzo workflow from a single OpenAPI specification.

**Learning Objectives:**
- Install and configure arazzo-generator
- Generate workflow from OpenAPI spec
- Review and validate generated workflow
- Execute generated workflow

**Prerequisites:**
- OpenAI API key or alternative LLM provider
- Basic understanding of OpenAPI specifications

#### multi-endpoint
Generate workflows that orchestrate multiple API endpoints.

**Learning Objectives:**
- Generate multi-step workflows
- Understand parameter mapping
- Handle data flow between steps

#### custom-prompts
Customize workflow generation with custom prompts and instructions.

**Learning Objectives:**
- Write effective prompts for generation
- Guide workflow structure
- Incorporate business logic

### Level 2 - Intermediate

#### workflow-optimization
Optimize generated workflows for performance and reliability.

**Learning Objectives:**
- Analyze generated workflows
- Apply optimization patterns
- Implement error handling
- Add retry logic

#### pattern-recognition
Identify and apply common API orchestration patterns.

**Learning Objectives:**
- Recognize API design patterns
- Apply appropriate workflow patterns
- Handle common scenarios
- Reuse patterns across projects

#### batch-generation
Generate multiple workflows from a single OpenAPI specification.

**Learning Objectives:**
- Batch process multiple workflows
- Manage generated artifacts
- Version control workflows
- Validate in bulk

### Level 3 - Advanced

#### custom-models
Use fine-tuned models for specialized workflow generation.

**Learning Objectives:**
- Fine-tune LLMs for workflow generation
- Train on domain-specific patterns
- Deploy custom models
- Evaluate generation quality

#### workflow-templates
Create and use templates for consistent workflow generation.

**Learning Objectives:**
- Design workflow templates
- Parameterize templates
- Generate from templates
- Maintain template library

#### ci-cd-integration
Integrate workflow generation into CI/CD pipelines.

**Learning Objectives:**
- Automate workflow generation
- Version control workflows
- Test generated workflows
- Deploy automatically

## Development Guidelines for Contributors

When adding generator recipes, follow these guidelines:

### Recipe Structure

Each recipe should include:

```
recipe-name/
├── README.md                     # Detailed instructions
├── Makefile                      # Convenient commands
├── pyproject.toml               # Recipe dependencies
├── .env.example                 # Environment template
├── input/
│   └── api.openapi.yaml         # Input OpenAPI spec
├── output/
│   └── workflow.arazzo.yaml     # Generated workflow
├── examples/
│   ├── generate.py              # Python generation example
│   └── generate.sh              # CLI generation example
├── prompts/
│   └── custom_prompt.txt        # Custom generation prompts
└── tests/
    └── test_generation.py       # Generation tests
```

### Dependencies

Generator recipes require:
- `arazzo-generator>=0.2.0`
- `openai>=1.0.0` (or alternative LLM provider)
- Standard development dependencies

### Testing

Generator recipe tests should verify:
1. Workflow generation succeeds
2. Generated workflow is valid Arazzo 1.0
3. Generated workflow executes successfully
4. Generated workflow matches expected patterns

Example test structure:

```python
def test_workflow_generation(openapi_spec, generator):
    """Test that workflow is generated successfully."""
    workflow = generator.generate(openapi_spec)
    assert workflow is not None
    assert "arazzo" in workflow
    assert workflow["arazzo"] == "1.0.0"

def test_generated_workflow_validates(generated_workflow):
    """Test that generated workflow is valid."""
    validator = ArazzoValidator()
    assert validator.validate(generated_workflow)

def test_generated_workflow_executes(generated_workflow):
    """Test that generated workflow can be executed."""
    runner = ArazzoRunner(generated_workflow)
    result = runner.execute_workflow("mainWorkflow", inputs={})
    assert result.status == "workflow_complete"
```

### Documentation

Each recipe README should include:
1. **Overview**: What the recipe demonstrates
2. **Prerequisites**: Required knowledge and tools
3. **Quick Start**: Get running in 5 minutes
4. **Step-by-Step Guide**: Detailed instructions
5. **Understanding the Generation**: Explain how it works
6. **Customization**: How to adapt for different use cases
7. **Troubleshooting**: Common issues and solutions
8. **Next Steps**: Related recipes

### Best Practices

1. **Use Real-World Examples**: Base recipes on practical use cases
2. **Start Simple**: Basic recipes should be easy to understand
3. **Document Decisions**: Explain why certain approaches are used
4. **Test Thoroughly**: Include both unit and integration tests
5. **Follow Standards**: Adhere to Arazzo 1.0 specification
6. **Consider Performance**: Generation should be reasonably fast
7. **Handle Errors**: Gracefully handle generation failures
8. **Provide Alternatives**: Show different generation approaches

## Dependencies

Generator recipes will require:

```toml
[project.optional-dependencies]
generator = [
    "arazzo-generator>=0.2.0",
    "openai>=1.0.0",
]
```

## Environment Variables

Generator recipes will need:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Alternative: Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_key_here
AZURE_OPENAI_DEPLOYMENT=your-deployment-name

# Generation Settings
ARAZZO_GENERATION_TEMPERATURE=0.7
ARAZZO_GENERATION_MAX_TOKENS=2000
```

## Contributing

To contribute a generator recipe:

1. Create a new branch from `main`
2. Add your recipe following the structure above
3. Include comprehensive tests
4. Update this README with your recipe
5. Submit a pull request

## Timeline

- **Q1 2024**: Basic generator recipes (simple-generation, multi-endpoint)
- **Q2 2024**: Intermediate recipes (optimization, patterns)
- **Q3 2024**: Advanced recipes (custom models, templates)
- **Q4 2024**: CI/CD integration recipes

## Resources

- [Arazzo Generator Documentation](https://github.com/jentic/arazzo-engine/tree/main/generator)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Arazzo Specification](https://github.com/OAI/Arazzo-Specification)

## Questions?

For questions about generator recipes:
- Open an issue: [GitHub Issues](https://github.com/jentic/arazzo-engine-cookbook/issues)
- Join the discussion: [GitHub Discussions](https://github.com/jentic/arazzo-engine-cookbook/discussions)
- Chat with us: [Discord](https://discord.gg/TdbWXZsUSm)

---

*This is a living document. As generator recipes are developed, this README will be updated with actual implementations and learnings.*