# Terminal colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)
BLUE   := $(shell tput -Txterm setaf 4)
RED    := $(shell tput -Txterm setaf 1)

# Project settings
PYTHON_VERSION := 3.11
VENV_NAME := .venv
PROJECT_NAME := arazzo-engine-cookbook
REPO_ROOT := $(shell pwd)
PYTHON := $(REPO_ROOT)/$(VENV_NAME)/bin/python
UV := $(shell which uv)

# Recipe settings
RECIPE_TYPES := runner generator
RECIPE_LEVELS := level-1-basic level-2-intermediate level-3-advanced
RECIPE_TARGET ?= simple-workflow
RECIPE_LEVEL ?= level-1-basic
RECIPE_TYPE ?= runner
RECIPE_PATH := recipes/$(RECIPE_TYPE)/$(RECIPE_LEVEL)/$(RECIPE_TARGET)

# Test settings
PYTEST_ARGS ?= -v
COVERAGE_THRESHOLD := 85

help: ## Show this help message
	@echo ''
	@echo '${YELLOW}Arazzo Engine Cookbook - Development Guide${RESET}'
	@echo ''
	@echo '${YELLOW}Quick Start:${RESET}'
	@echo '  Setup:        ${GREEN}make setup${RESET}              - Complete development environment'
	@echo '  Recipe:       ${GREEN}make recipe RECIPE_TARGET=simple-workflow${RESET} - Work with specific recipe'
	@echo '  Activate:     ${GREEN}source .venv/bin/activate${RESET} - Activate environment'
	@echo ''
	@echo '${YELLOW}Recipe Management:${RESET}'
	@echo '  List:         ${GREEN}make list-recipes${RESET}       - Show all available recipes'
	@echo '  Validate:     ${GREEN}make validate-recipe${RESET}    - Validate recipe structure'
	@echo '  Test Recipe:  ${GREEN}make test-recipe${RESET}        - Test specific recipe'
	@echo '  New Recipe:   ${GREEN}make new-recipe RECIPE_TARGET=my-recipe RECIPE_LEVEL=level-1-basic${RESET}'
	@echo ''
	@echo '${YELLOW}Arazzo Runner Commands:${RESET}'
	@echo '  Execute:      ${GREEN}make execute${RESET}            - Execute Arazzo workflow'
	@echo '  Validate:     ${GREEN}make validate-workflow${RESET}  - Validate Arazzo spec'
	@echo '  Test:         ${GREEN}make test-workflow${RESET}      - Test workflow execution'
	@echo ''
	@echo '${YELLOW}Development:${RESET}'
	@echo '  Format:       ${GREEN}make format${RESET}             - Format all code'
	@echo '  Lint:         ${GREEN}make lint${RESET}               - Run linters'
	@echo '  Test:         ${GREEN}make test${RESET}               - Run all tests'
	@echo '  Clean:        ${GREEN}make clean${RESET}              - Clean build artifacts'
	@echo ''
	@echo '${YELLOW}Available Targets:${RESET}'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${YELLOW}%-15s${GREEN}%s${RESET}\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ''

# Environment setup
.PHONY: check-uv
check-uv: ## Check if uv is installed
	@if ! command -v uv > /dev/null 2>&1; then \
	  echo "${RED}Error: uv is not installed. Please install it first:${RESET}"; \
	  echo "curl -LsSf https://astral.sh/uv/install.sh | sh"; \
	  exit 1; \
	fi
	@echo "${GREEN}✓ uv is installed${RESET}"

.PHONY: env
env: check-uv ## Create virtual environment using uv
	@echo "${BLUE}Creating virtual environment with Python $(PYTHON_VERSION)...${RESET}"
	$(UV) venv --python $(PYTHON_VERSION)
	@echo "${GREEN}Virtual environment created. Activate it with:${RESET}"
	@echo "source $(VENV_NAME)/bin/activate"

.PHONY: install-core
install-core: ## Install core Arazzo dependencies
	@echo "${BLUE}Installing core Arazzo dependencies...${RESET}"
	@if [ ! -f "$(PYTHON)" ]; then \
	  echo "${YELLOW}Virtual environment not found. Creating it first...${RESET}"; \
	  make env; \
	fi
	$(UV) pip install -e "." --python $(REPO_ROOT)/$(VENV_NAME)/bin/python
	@echo "${GREEN}Core dependencies installed successfully${RESET}"

.PHONY: install-dev
install-dev: ## Install development dependencies
	@echo "${BLUE}Installing development dependencies...${RESET}"
	$(UV) pip install -e ".[dev]" --python $(REPO_ROOT)/$(VENV_NAME)/bin/python
	@echo "${GREEN}Development dependencies installed successfully${RESET}"

.PHONY: install-basic
install-basic: ## Install basic recipe dependencies
	@echo "${BLUE}Installing basic recipe dependencies...${RESET}"
	$(UV) pip install -e ".[basic]" --python $(REPO_ROOT)/$(VENV_NAME)/bin/python
	@echo "${GREEN}Basic dependencies installed successfully${RESET}"

.PHONY: install-intermediate
install-intermediate: ## Install intermediate recipe dependencies
	@echo "${BLUE}Installing intermediate recipe dependencies...${RESET}"
	$(UV) pip install -e ".[intermediate]" --python $(REPO_ROOT)/$(VENV_NAME)/bin/python
	@echo "${GREEN}Intermediate dependencies installed successfully${RESET}"

.PHONY: install-advanced
install-advanced: ## Install advanced recipe dependencies
	@echo "${BLUE}Installing advanced recipe dependencies...${RESET}"
	$(UV) pip install -e ".[advanced]" --python $(REPO_ROOT)/$(VENV_NAME)/bin/python
	@echo "${GREEN}Advanced dependencies installed successfully${RESET}"

.PHONY: install-all
install-all: ## Install all dependencies
	@echo "${BLUE}Installing all dependencies...${RESET}"
	$(UV) pip install -e ".[all]" --python $(REPO_ROOT)/$(VENV_NAME)/bin/python
	@echo "${GREEN}All dependencies installed successfully${RESET}"

.PHONY: setup
setup: ## Create environment and install development dependencies
	@echo "${BLUE}Setting up complete development environment...${RESET}"
	make env
	make install-dev
	make install-basic
	@echo ""
	@echo "${GREEN}Setup complete! Development environment ready.${RESET}"
	@echo "${YELLOW}To activate the environment, run:${RESET}"
	@echo "  ${GREEN}source .venv/bin/activate${RESET}"
	@echo ""
	@echo "${YELLOW}To work with a specific recipe:${RESET}"
	@echo "  ${GREEN}make recipe RECIPE_TARGET=simple-workflow${RESET}"

.PHONY: check-env
check-env: ## Check if virtual environment is active and working
	@echo "${BLUE}Checking environment...${RESET}"
	@if [ ! -f "$(PYTHON)" ]; then \
	  echo "${RED}Virtual environment not found at $(PYTHON)${RESET}"; \
	  echo "Run 'make setup' first"; \
	  exit 1; \
	fi
	@echo "Python: $(PYTHON)"
	@$(PYTHON) --version
	@$(PYTHON) -c "import sys; print(f'Python executable: {sys.executable}')"
	@if $(PYTHON) -c "import arazzo_runner" 2>/dev/null; then \
	  echo "${GREEN}✓ Arazzo Runner is installed${RESET}"; \
	  $(PYTHON) -c "import arazzo_runner; print(f'Version: {arazzo_runner.__version__}' if hasattr(arazzo_runner, '__version__') else 'Version: unknown')"; \
	else \
	  echo "${YELLOW}⚠ Arazzo Runner not found - run 'make install-core' first${RESET}"; \
	fi
	@echo "${GREEN}Environment check complete${RESET}"

# Recipe management
.PHONY: list-recipes
list-recipes: ## List all available recipes
	@echo "${BLUE}Available Recipes:${RESET}"
	@echo ""
	@for recipe_type in $(RECIPE_TYPES); do \
	  echo "${YELLOW}$$recipe_type recipes:${RESET}"; \
	  for level in $(RECIPE_LEVELS); do \
	    if [ -d "recipes/$$recipe_type/$$level" ]; then \
	      echo "  ${YELLOW}$$level:${RESET}"; \
	      for recipe in recipes/$$recipe_type/$$level/*/; do \
	        if [ -d "$$recipe" ]; then \
	          recipe_name=$$(basename "$$recipe"); \
	          if [ -f "$$recipe/README.md" ]; then \
	            description=$$(head -n 5 "$$recipe/README.md" | grep -E "^#|description" | head -n 1 | sed 's/^#*[[:space:]]*//'); \
	            echo "    ${GREEN}$$recipe_name${RESET} - $$description"; \
	          else \
	            echo "    ${GREEN}$$recipe_name${RESET}"; \
	          fi; \
	        fi; \
	      done; \
	    fi; \
	  done; \
	  echo ""; \
	done

.PHONY: recipe
recipe: ## Work with a specific recipe (usage: make recipe RECIPE_TARGET=simple-workflow)
	@if [ ! -d "$(RECIPE_PATH)" ]; then \
	  echo "${RED}Recipe '$(RECIPE_TARGET)' not found in '$(RECIPE_TYPE)/$(RECIPE_LEVEL)'${RESET}"; \
	  echo "Available recipes:"; \
	  make list-recipes; \
	  exit 1; \
	fi
	@echo "${BLUE}Working with recipe: $(RECIPE_TARGET)${RESET}"
	@echo "Recipe path: $(RECIPE_PATH)"
	@echo ""
	@echo "${YELLOW}Recipe commands:${RESET}"
	@echo "  ${GREEN}cd $(RECIPE_PATH)${RESET}"
	@echo "  ${GREEN}make setup-recipe${RESET}   - Install recipe dependencies"
	@echo "  ${GREEN}make run${RESET}            - Execute workflow"
	@echo "  ${GREEN}make test${RESET}           - Run tests"

.PHONY: validate-recipe
validate-recipe: ## Validate recipe structure
	@if [ ! -d "$(RECIPE_PATH)" ]; then \
	  echo "${RED}Recipe '$(RECIPE_TARGET)' not found${RESET}"; \
	  exit 1; \
	fi
	@echo "${BLUE}Validating recipe: $(RECIPE_TARGET)${RESET}"
	@error_count=0; \
	if [ "$(RECIPE_TYPE)" = "runner" ]; then \
	  for required_file in README.md pyproject.toml arazzo/workflow.arazzo.yaml; do \
	    if [ ! -f "$(RECIPE_PATH)/$$required_file" ]; then \
	      echo "${RED}✗ Missing required file: $$required_file${RESET}"; \
	      error_count=$$((error_count + 1)); \
	    else \
	      echo "${GREEN}✓ Found: $$required_file${RESET}"; \
	    fi; \
	  done; \
	else \
	  for required_file in README.md; do \
	    if [ ! -f "$(RECIPE_PATH)/$required_file" ]; then \
	      echo "${RED}✗ Missing required file: $required_file${RESET}"; \
	      error_count=$((error_count + 1)); \
	    else \
	      echo "${GREEN}✓ Found: $required_file${RESET}"; \
	    fi; \
	  done; \
	fi; \
	if [ $error_count -eq 0 ]; then \
	  echo "${GREEN}✓ Recipe structure is valid${RESET}"; \
	else \
	  echo "${RED}✗ Recipe validation failed with $error_count errors${RESET}"; \
	  exit 1; \
	fi

.PHONY: new-recipe
new-recipe: ## Create a new recipe (usage: make new-recipe RECIPE_TARGET=my-recipe RECIPE_LEVEL=level-1-basic RECIPE_TYPE=runner)
	@if [ -d "$(RECIPE_PATH)" ]; then \
	  echo "${RED}Recipe '$(RECIPE_TARGET)' already exists${RESET}"; \
	  exit 1; \
	fi
	@echo "${BLUE}Creating new recipe: $(RECIPE_TARGET)${RESET}"
	@mkdir -p "$(RECIPE_PATH)"
	@if [ "$(RECIPE_TYPE)" = "runner" ]; then \
	  mkdir -p "$(RECIPE_PATH)/arazzo"; \
	  mkdir -p "$(RECIPE_PATH)/openapi"; \
	  mkdir -p "$(RECIPE_PATH)/examples"; \
	  mkdir -p "$(RECIPE_PATH)/tests"; \
	  echo "# $(RECIPE_TARGET)" > "$(RECIPE_PATH)/README.md"; \
	  echo "" >> "$(RECIPE_PATH)/README.md"; \
	  echo "Description of your recipe goes here." >> "$(RECIPE_PATH)/README.md"; \
	  echo "arazzo: \"1.0.0\"" > "$(RECIPE_PATH)/arazzo/workflow.arazzo.yaml"; \
	  echo "info:" >> "$(RECIPE_PATH)/arazzo/workflow.arazzo.yaml"; \
	  echo "  title: $(RECIPE_TARGET)" >> "$(RECIPE_PATH)/arazzo/workflow.arazzo.yaml"; \
	  echo "  version: 1.0.0" >> "$(RECIPE_PATH)/arazzo/workflow.arazzo.yaml"; \
	else \
	  mkdir -p "$(RECIPE_PATH)"; \
	  echo "# $(RECIPE_TARGET) (Generator Recipe)" > "$(RECIPE_PATH)/README.md"; \
	  echo "" >> "$(RECIPE_PATH)/README.md"; \
	  echo "Coming soon. This is a placeholder for generator recipes." >> "$(RECIPE_PATH)/README.md"; \
	fi
	@echo "${GREEN}✓ Recipe structure created at $(RECIPE_PATH)${RESET}"
	@echo "Edit the files to implement your recipe."

# Arazzo Runner commands
.PHONY: check-recipe-context
check-recipe-context: ## Check if we're in a valid recipe context
	@if [ ! -f "arazzo/workflow.arazzo.yaml" ]; then \
	  echo "${RED}Error: Not in a runner recipe directory.${RESET}"; \
	  echo "Usage: cd recipes/runner/level-1-basic/simple-workflow && make execute"; \
	  echo "   or: make execute RECIPE_TARGET=simple-workflow RECIPE_LEVEL=level-1-basic"; \
	  exit 1; \
	fi

.PHONY: execute
execute: ## Execute Arazzo workflow in current recipe
	@if [ -f "arazzo/workflow.arazzo.yaml" ]; then \
	  echo "${BLUE}Executing Arazzo workflow in current directory...${RESET}"; \
	  $(PYTHON) -m arazzo_runner execute arazzo/workflow.arazzo.yaml; \
	else \
	  if [ -d "$(RECIPE_PATH)" ] && [ -f "$(RECIPE_PATH)/arazzo/workflow.arazzo.yaml" ]; then \
	    echo "${BLUE}Executing Arazzo workflow in $(RECIPE_PATH)...${RESET}"; \
	    cd "$(RECIPE_PATH)" && $(PYTHON) -m arazzo_runner execute arazzo/workflow.arazzo.yaml; \
	  else \
	    echo "${RED}No workflow found. Check recipe context.${RESET}"; \
	    exit 1; \
	  fi; \
	fi
	@echo "${GREEN}✓ Workflow execution completed${RESET}"

.PHONY: validate-workflow
validate-workflow: ## Validate Arazzo workflow specification
	@if [ -f "arazzo/workflow.arazzo.yaml" ]; then \
	  echo "${BLUE}Validating Arazzo workflow in current directory...${RESET}"; \
	  $(PYTHON) -m arazzo_runner validate arazzo/workflow.arazzo.yaml; \
	else \
	  if [ -d "$(RECIPE_PATH)" ] && [ -f "$(RECIPE_PATH)/arazzo/workflow.arazzo.yaml" ]; then \
	    echo "${BLUE}Validating Arazzo workflow in $(RECIPE_PATH)...${RESET}"; \
	    cd "$(RECIPE_PATH)" && $(PYTHON) -m arazzo_runner validate arazzo/workflow.arazzo.yaml; \
	  else \
	    echo "${RED}No workflow found. Check recipe context.${RESET}"; \
	    exit 1; \
	  fi; \
	fi
	@echo "${GREEN}✓ Workflow validation completed${RESET}"

.PHONY: test-workflow
test-workflow: ## Test workflow execution
	@if [ -f "tests/test_workflow.py" ]; then \
	  echo "${BLUE}Testing workflow in current directory...${RESET}"; \
	  $(PYTHON) -m pytest tests/test_workflow.py $(PYTEST_ARGS); \
	else \
	  if [ -d "$(RECIPE_PATH)" ] && [ -f "$(RECIPE_PATH)/tests/test_workflow.py" ]; then \
	    echo "${BLUE}Testing workflow in $(RECIPE_PATH)...${RESET}"; \
	    cd "$(RECIPE_PATH)" && $(PYTHON) -m pytest tests/test_workflow.py $(PYTEST_ARGS); \
	  else \
	    echo "${YELLOW}No workflow tests found${RESET}"; \
	  fi; \
	fi

.PHONY: test-recipe
test-recipe: ## Test specific recipe
	@if [ ! -d "$(RECIPE_PATH)" ]; then \
	  echo "${RED}Recipe '$(RECIPE_TARGET)' not found${RESET}"; \
	  exit 1; \
	fi
	@echo "${BLUE}Testing recipe: $(RECIPE_TARGET)${RESET}"
	@cd "$(RECIPE_PATH)" && \
	if [ -f "tests/test_workflow.py" ]; then \
	  echo "Running workflow tests..."; \
	  $(PYTHON) -m pytest tests/ $(PYTEST_ARGS); \
	else \
	  echo "${YELLOW}No tests found for this recipe${RESET}"; \
	fi

# Development commands
.PHONY: format
format: ## Format all code with Ruff and Black
	@echo "${BLUE}Formatting code...${RESET}"
	$(PYTHON) -m ruff check --fix recipes/
	$(PYTHON) -m ruff format recipes/
	$(PYTHON) -m black recipes/
	$(PYTHON) -m isort recipes/
	@echo "${GREEN}✓ Code formatting completed${RESET}"

.PHONY: lint
lint: ## Run linters
	@echo "${BLUE}Running linters...${RESET}"
	$(PYTHON) -m ruff check recipes/
	$(PYTHON) -m ruff format --check recipes/
	$(PYTHON) -m black --check recipes/
	$(PYTHON) -m mypy recipes/ --ignore-missing-imports
	@echo "${GREEN}✓ Linting completed${RESET}"

.PHONY: test
test: ## Run all tests
	@echo "${BLUE}Running tests...${RESET}"
	$(PYTHON) -m pytest recipes/ $(PYTEST_ARGS) \
	  --cov=recipes \
	  --cov-report=term-missing \
	  --cov-fail-under=$(COVERAGE_THRESHOLD)
	@echo "${GREEN}✓ All tests completed${RESET}"

.PHONY: test-fast
test-fast: ## Run fast tests only
	@echo "${BLUE}Running fast tests...${RESET}"
	$(PYTHON) -m pytest recipes/ $(PYTEST_ARGS) -m "not slow and not integration"
	@echo "${GREEN}✓ Fast tests completed${RESET}"

.PHONY: test-integration
test-integration: ## Run integration tests
	@echo "${BLUE}Running integration tests...${RESET}"
	$(PYTHON) -m pytest recipes/ $(PYTEST_ARGS) -m "integration"
	@echo "${GREEN}✓ Integration tests completed${RESET}"

# Utility commands
.PHONY: clean
clean: ## Clean build artifacts and cache
	@echo "${BLUE}Cleaning build artifacts and cache...${RESET}"
	rm -rf build/ dist/ *.egg-info .coverage htmlcov/
	rm -rf $(VENV_NAME) .mypy_cache .pytest_cache .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	# Clean recipe-specific artifacts
	find recipes/ -type d -name "logs" -exec rm -rf {} +
	find recipes/ -type f -name "*.log" -delete
	@echo "${GREEN}✓ Cleaned all build artifacts and cache${RESET}"

.PHONY: update
update: ## Update all dependencies
	@echo "${BLUE}Updating dependencies...${RESET}"
	$(UV) pip install --upgrade -e ".[dev]" --python $(REPO_ROOT)/$(VENV_NAME)/bin/python
	@echo "${GREEN}✓ Dependencies updated${RESET}"

.PHONY: validate-all
validate-all: ## Validate all recipes
	@echo "${BLUE}Validating all recipes...${RESET}"
	@error_count=0; \
	for recipe_type in $(RECIPE_TYPES); do \
	  for level in $(RECIPE_LEVELS); do \
	    if [ -d "recipes/$recipe_type/$level" ]; then \
	      for recipe in recipes/$recipe_type/$level/*/; do \
	        if [ -d "$recipe" ]; then \
	          recipe_name=$(basename "$recipe"); \
	          echo "Validating $recipe_type/$level/$recipe_name..."; \
	          if ! RECIPE_TARGET=$recipe_name RECIPE_LEVEL=$level RECIPE_TYPE=$recipe_type make validate-recipe >/dev/null 2>&1; then \
	            echo "${RED}✗ $recipe_type/$level/$recipe_name failed validation${RESET}"; \
	            error_count=$((error_count + 1)); \
	          else \
	            echo "${GREEN}✓ $recipe_type/$level/$recipe_name${RESET}"; \
	          fi; \
	        fi; \
	      done; \
	    fi; \
	  done; \
	done; \
	if [ $error_count -eq 0 ]; then \
	  echo "${GREEN}✓ All recipes validated successfully${RESET}"; \
	else \
	  echo "${RED}✗ $error_count recipes failed validation${RESET}"; \
	  exit 1; \
	fi

.PHONY: pre-commit
pre-commit: format lint test validate-all ## Run all checks before committing
	@echo "${GREEN}✓ All pre-commit checks passed${RESET}"

.PHONY: structure
structure: ## Show project structure
	@echo "${YELLOW}Arazzo Engine Cookbook Structure:${RESET}"
	@echo "${BLUE}"
	@if command -v tree > /dev/null; then \
		tree -a -I '.git|.venv|__pycache__|*.pyc|*.pyo|*.pyd|.pytest_cache|.ruff_cache|.coverage|htmlcov'; \
	else \
		find . -not -path '*/\.*' -not -path '*.pyc' -not -path '*/__pycache__/*' \
			-not -path './.venv/*' -not -path './build/*' -not -path './dist/*' \
			-not -path './*.egg-info/*' \
			| sort | \
			sed -e "s/[^-][^\/]*\// │   /g" -e "s/├── /│── /" -e "s/└── /└── /"; \
	fi
	@echo "${RESET}"

# Quick start commands
.PHONY: quick-start
quick-start: ## Quick start with simple-workflow recipe
	@echo "${BLUE}Quick start with simple-workflow recipe...${RESET}"
	@if [ ! -d ".venv" ]; then \
	  make setup; \
	fi
	@make recipe RECIPE_TARGET=simple-workflow RECIPE_LEVEL=level-1-basic RECIPE_TYPE=runner
	@echo ""
	@echo "${GREEN}✓ Quick start completed!${RESET}"
	@echo "${YELLOW}Next steps:${RESET}"
	@echo "  1. ${GREEN}cd recipes/runner/level-1-basic/simple-workflow${RESET}"
	@echo "  2. Review the README.md"
	@echo "  3. ${GREEN}make run${RESET}"

.PHONY: setup-env-all
setup-env-all: ## Create .env files for all recipes
	@echo "${BLUE}Setting up environment files for all recipes...${RESET}"
	@if [ ! -f ".env" ]; then \
		echo "Creating root .env file..."; \
		cp .env.example .env; \
	fi
	@for recipe_type in $(RECIPE_TYPES); do \
		for level in $(RECIPE_LEVELS); do \
			if [ -d "recipes/$recipe_type/$level" ]; then \
				for recipe in recipes/$recipe_type/$level/*/; do \
					if [ -d "$recipe" ] && [ -f "$recipe/.env.example" ]; then \
						recipe_name=$(basename "$recipe"); \
						if [ ! -f "$recipe/.env" ]; then \
							echo "Creating .env for $recipe_type/$level/$recipe_name..."; \
							cp "$recipe/.env.example" "$recipe/.env"; \
						fi; \
					fi; \
				done; \
			fi; \
		done; \
	done
	@echo "${GREEN}✓ Environment files created${RESET}"
	@echo "${YELLOW}Please edit .env files with your actual credentials${RESET}"

.PHONY: check-env-all
check-env-all: ## Check environment setup for all recipes
	@echo "${BLUE}Checking environment for all recipes...${RESET}"
	@error_count=0; \
	for recipe_type in $(RECIPE_TYPES); do \
		for level in $(RECIPE_LEVELS); do \
			if [ -d "recipes/$recipe_type/$level" ]; then \
				for recipe in recipes/$recipe_type/$level/*/; do \
					if [ -d "$recipe" ]; then \
						recipe_name=$(basename "$recipe"); \
						echo "Checking $recipe_type/$level/$recipe_name..."; \
						if [ -f "$recipe/.env" ]; then \
							echo "  ✓ .env exists"; \
						else \
							echo "  ✗ .env missing"; \
							error_count=$((error_count + 1)); \
						fi; \
					fi; \
				done; \
			fi; \
		done; \
	done; \
	if [ $error_count -eq 0 ]; then \
		echo "${GREEN}✓ All recipes have environment files${RESET}"; \
	else \
		echo "${YELLOW}⚠ $error_count recipes missing .env files${RESET}"; \
		echo "Run 'make setup-env-all' to create them"; \
	fi

.DEFAULT_GOAL := help