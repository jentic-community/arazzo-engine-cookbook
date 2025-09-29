# Arazzo Engine Cookbook

A comprehensive collection of recipes for building API workflow orchestrations using the Arazzo Specification with the Arazzo Engine (Runner & Generator).

## What is Arazzo?

Arazzo is the official specification from the OpenAPI Initiative for describing and executing complex API orchestrations. While OpenAPI describes individual APIs, **Arazzo defines workflows that orchestrate calls across one or more APIs**.

This cookbook provides practical, real-world recipes for:
- **Runner**: Executing Arazzo workflows with full specification compliance
- **Generator**: Creating Arazzo workflows from OpenAPI specifications (coming soon)

## Repository Structure

```
arazzo-engine-cookbook/
├── .env.example
├── .gitignore
├── Makefile
├── pyproject.toml
├── README.md
└── recipes/
    ├── runner/
    │   ├── level-1-basic/
    │   │   ├── simple-workflow/          # Single API, basic flow
    │   │   ├── multi-step-flow/          # Multiple steps, data passing
    │   │   └── error-handling/           # Success criteria, retries
    │   ├── level-2-intermediate/
    │   │   ├── authentication/           # OAuth2, API keys
    │   │   ├── multi-api-orchestration/  # Cross-API workflows
    │   │   ├── conditional-logic/        # Branching, criteria evaluation
    │   │   └── parameter-mapping/        # Complex data transformation
    │   └── level-3-advanced/
    │       ├── workflow-dependencies/    # Dependent workflows
    │       ├── real-time-streaming/      # Server variables, dynamic URLs
    │       ├── custom-extensions/        # Custom actions, integrations
    │       └── production-patterns/      # Error recovery, monitoring
    └── generator/
        ├── level-1-basic/
        │   └── README.md                 # Coming soon guide
        ├── level-2-intermediate/
        │   └── README.md
        └── level-3-advanced/
            └── README.md
```

## Quick Start

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jentic/arazzo-engine-cookbook.git
   cd arazzo-engine-cookbook
   ```

2. **Set up development environment**
   ```bash
   make setup
   source .venv/bin/activate
   ```

3. **Explore available recipes**
   ```bash
   make list-recipes
   ```

4. **Run your first recipe**
   ```bash
   cd recipes/runner/level-1-basic/simple-workflow
   make run
   ```

## Available Recipes

### Runner Recipes

#### Level 1 - Basic
- **simple-workflow**: Execute a single API workflow with basic parameters
- **multi-step-flow**: Chain multiple API calls with data passing between steps
- **error-handling**: Handle failures with success criteria and error responses

#### Level 2 - Intermediate
- **authentication**: Implement OAuth2, API keys, and bearer token authentication
- **multi-api-orchestration**: Orchestrate workflows across multiple APIs
- **conditional-logic**: Build workflows with branching and conditional execution
- **parameter-mapping**: Transform and map data between workflow steps

#### Level 3 - Advanced
- **workflow-dependencies**: Create workflows that depend on other workflows
- **real-time-streaming**: Handle server variables and dynamic base URLs
- **custom-extensions**: Build custom actions and integrate external systems
- **production-patterns**: Implement error recovery, monitoring, and best practices

### Generator Recipes (Coming Soon)

The generator recipes will cover AI-powered workflow generation from OpenAPI specs. See `recipes/generator/README.md` for the roadmap.

## Recipe Structure

Each recipe follows a consistent structure:

```
recipe-name/
├── README.md                    # Recipe overview and instructions
├── pyproject.toml              # Recipe-specific dependencies
├── Makefile                    # Convenient commands
├── .env.example                # Environment variable template
├── arazzo/
│   └── workflow.arazzo.yaml    # Arazzo workflow definition
├── openapi/
│   ├── api1.openapi.yaml       # OpenAPI specifications
│   └── api2.openapi.yaml
├── examples/
│   ├── basic_example.py        # Python usage examples
│   └── cli_example.sh          # CLI usage examples
└── tests/
    └── test_workflow.py        # Workflow tests
```

## Working with Recipes

### Using the Makefile

The root Makefile provides convenient commands:

```bash
# Setup
make setup                              # Complete environment setup
make check-env                          # Verify environment

# Recipe Management
make list-recipes                       # Show all recipes
make recipe RECIPE_TARGET=simple-workflow RECIPE_LEVEL=level-1-basic
make validate-recipe RECIPE_TARGET=simple-workflow

# Development
make format                             # Format code
make lint                               # Run linters
make test                               # Run all tests
make clean                              # Clean artifacts
```

### Running Individual Recipes

Each recipe has its own Makefile:

```bash
cd recipes/runner/level-1-basic/simple-workflow
make install                            # Install dependencies
make run                                # Execute workflow
make test                               # Test workflow
make clean                              # Clean up
```

## Development Guidelines

### Adding a New Recipe

1. **Create recipe structure**
   ```bash
   make new-recipe RECIPE_TARGET=my-workflow RECIPE_LEVEL=level-1-basic RECIPE_TYPE=runner
   ```

2. **Implement the recipe**
   - Add Arazzo workflow definition
   - Include OpenAPI specifications
   - Write examples and documentation
   - Add tests

3. **Test thoroughly**
   ```bash
   cd recipes/runner/level-1-basic/my-workflow
   make test
   make validate
   ```

4. **Submit for review**
   - Ensure all tests pass
   - Update documentation
   - Create pull request

### Recipe Best Practices

- **Self-contained**: Each recipe should be independently runnable
- **Well-documented**: Include clear README with prerequisites and steps
- **Practical**: Focus on real-world use cases and patterns
- **Tested**: Include both mock and real API tests where appropriate
- **Clean**: Follow project formatting and linting standards

## Dependency Groups

The cookbook uses optional dependency groups:

```bash
# API providers
pip install -e ".[stripe]"         # Stripe API integration
pip install -e ".[github]"         # GitHub API integration
pip install -e ".[slack]"          # Slack API integration

# Features
pip install -e ".[auth]"           # OAuth2 and advanced auth
pip install -e ".[monitoring]"     # Observability and metrics
pip install -e ".[testing]"        # Testing utilities

# Meta-groups
pip install -e ".[basic]"          # Basic recipe dependencies
pip install -e ".[intermediate]"   # Intermediate dependencies
pip install -e ".[advanced]"       # Advanced dependencies
pip install -e ".[all]"            # All dependencies
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# API Keys
STRIPE_API_KEY=sk_test_...
GITHUB_TOKEN=ghp_...
SLACK_BOT_TOKEN=xoxb-...

# OpenAI (for Generator)
OPENAI_API_KEY=sk-...

# Configuration
ARAZZO_LOG_LEVEL=INFO
ARAZZO_TIMEOUT=30
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution

- New recipe ideas and implementations
- Improvements to existing recipes
- Documentation enhancements
- Test coverage improvements
- Bug fixes and optimizations

## Resources

### Arazzo Engine
- [GitHub Repository](https://github.com/jentic/arazzo-engine)
- [Runner Documentation](https://github.com/jentic/arazzo-engine/tree/main/runner)
- [Generator Documentation](https://github.com/jentic/arazzo-engine/tree/main/generator)

### Arazzo Specification
- [Official Specification](https://github.com/OAI/Arazzo-Specification)
- [OpenAPI Initiative](https://www.openapis.org/)

### Community
- [Discord](https://discord.gg/TdbWXZsUSm)
- [GitHub Discussions](https://github.com/jentic/arazzo-engine/discussions)
- [Issues](https://github.com/jentic/arazzo-engine/issues)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: Check recipe READMEs and the main Arazzo Engine docs
- **Issues**: [GitHub Issues](https://github.com/jentic/arazzo-engine-cookbook/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jentic/arazzo-engine-cookbook/discussions)
- **Discord**: [Join our community](https://discord.gg/TdbWXZsUSm)

---

*Built with ❤️ by the Arazzo community. Let's orchestrate APIs together!*