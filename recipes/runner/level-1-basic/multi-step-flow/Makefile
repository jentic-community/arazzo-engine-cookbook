# Terminal colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)
BLUE   := $(shell tput -Txterm setaf 4)
RED    := $(shell tput -Txterm setaf 1)

# Project settings
RECIPE_NAME := multi-step-flow

# Detect Python from virtual environment or fall back to system Python
# First, try to find the root venv (4 levels up from recipe directory)
REPO_ROOT := $(shell cd ../../../.. && pwd)
VENV_PYTHON := $(REPO_ROOT)/.venv/bin/python

# Check if venv Python exists, otherwise fall back to system Python
ifeq ($(shell test -f $(VENV_PYTHON) && echo yes),yes)
    PYTHON := $(VENV_PYTHON)
    $(info Using virtual environment Python: $(PYTHON))
else
    PYTHON := python3
    $(warning Virtual environment not found at $(VENV_PYTHON), using system Python)
    $(warning Run 'make setup' from the repository root first)
endif

ARAZZO_FILE := arazzo/workflow.arazzo.yaml
WORKFLOW_ID := getUserContent
INPUT ?= {"userId": 1}

help: ## Show this help message
	@echo ''
	@echo '${YELLOW}Multi-Step Flow Recipe${RESET}'
	@echo ''
	@echo '${YELLOW}Quick Start:${RESET}'
	@echo '  ${GREEN}make install${RESET}        - Install dependencies'
	@echo '  ${GREEN}make run${RESET}            - Execute workflow'
	@echo '  ${GREEN}make test${RESET}           - Run tests'
	@echo ''
	@echo '${YELLOW}Available Commands:${RESET}'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${YELLOW}%-15s${GREEN}%s${RESET}\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ''

.PHONY: check-venv
check-venv: ## Check if virtual environment is available
	@if [ ! -f "$(VENV_PYTHON)" ]; then \
	  echo "${RED}Error: Virtual environment not found${RESET}"; \
	  echo "Expected location: $(VENV_PYTHON)"; \
	  echo ""; \
	  echo "${YELLOW}Please run from the repository root:${RESET}"; \
	  echo "  ${GREEN}cd $(REPO_ROOT)${RESET}"; \
	  echo "  ${GREEN}make setup${RESET}"; \
	  echo ""; \
	  exit 1; \
	fi
	@echo "${GREEN}✓ Virtual environment found${RESET}"

.PHONY: check
check: check-venv ## Verify setup
	@echo "${BLUE}Checking setup...${RESET}"
	@echo "Python: $(PYTHON)"
	@$(PYTHON) --version
	@$(PYTHON) -c "import arazzo_runner; print('✓ arazzo-runner installed')" || \
	  (echo "${RED}✗ arazzo-runner not found - run 'make install'${RESET}" && exit 1)
	@test -f $(ARAZZO_FILE) && echo "✓ Workflow file exists" || echo "✗ Workflow file missing"
	@echo "${GREEN}✓ Setup verified${RESET}"

.PHONY: validate
validate: check-venv ## Validate workflow specification
	@echo "${BLUE}Validating workflow...${RESET}"
	@$(PYTHON) -c "import yaml; yaml.safe_load(open('$(ARAZZO_FILE)'))" && echo "${GREEN}✓ Workflow YAML is valid${RESET}"

.PHONY: run
run: check-venv ## Execute workflow (use: make run INPUT='{"userId": 2}')
	@echo "${BLUE}Executing workflow with input: $(INPUT)${RESET}"
	@$(PYTHON) -m arazzo_runner execute-workflow $(ARAZZO_FILE) \
	  --workflow-id $(WORKFLOW_ID) \
	  --inputs '$(INPUT)'
	@echo "${GREEN}✓ Workflow execution completed${RESET}"

.PHONY: run-python
run-python: check-venv ## Execute workflow using Python script
	@echo "${BLUE}Running Python example...${RESET}"
	@$(PYTHON) examples/basic_example.py
	@echo "${GREEN}✓ Python example completed${RESET}"

.PHONY: run-all-users
run-all-users: check-venv ## Execute workflow for multiple users
	@echo "${BLUE}Fetching content for multiple users...${RESET}"
	@for i in 1 2 3; do \
	  echo ""; \
	  echo "${YELLOW}User $$i:${RESET}"; \
	  $(PYTHON) examples/basic_example.py --user-id $$i 2>/dev/null || true; \
	done
	@echo "${GREEN}✓ All users processed${RESET}"

.PHONY: test
test: check-venv ## Run workflow tests
	@echo "${BLUE}Running tests...${RESET}"
	@$(PYTHON) -m pytest tests/ -v
	@echo "${GREEN}✓ Tests completed${RESET}"

.PHONY: test-coverage
test-coverage: check-venv ## Run tests with coverage
	@echo "${BLUE}Running tests with coverage...${RESET}"
	@$(PYTHON) -m pytest tests/ -v --cov=. --cov-report=term-missing
	@echo "${GREEN}✓ Tests with coverage completed${RESET}"

.PHONY: clean
clean: ## Clean generated files
	@echo "${BLUE}Cleaning...${RESET}"
	@rm -rf __pycache__ .pytest_cache .coverage htmlcov
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "${GREEN}✓ Cleaned${RESET}"

.PHONY: show-workflow
show-workflow: ## Display workflow definition
	@echo "${YELLOW}Workflow Definition:${RESET}"
	@cat $(ARAZZO_FILE)

.PHONY: show-openapi
show-openapi: ## Display OpenAPI specification
	@echo "${YELLOW}OpenAPI Specification:${RESET}"
	@cat openapi/jsonplaceholder.openapi.yaml

.PHONY: explain
explain: ## Explain workflow steps
	@echo "${YELLOW}Workflow Steps:${RESET}"
	@echo ""
	@echo "${BLUE}Step 1: fetchUser${RESET}"
	@echo "  - Fetches user information by ID"
	@echo "  - Input: userId from workflow input"
	@echo "  - Output: userId, username, name, email"
	@echo ""
	@echo "${BLUE}Step 2: fetchPosts${RESET}"
	@echo "  - Fetches all posts by the user"
	@echo "  - Input: userId from Step 1 output"
	@echo "  - Output: posts array, postCount, firstPostId, firstPostTitle"
	@echo ""
	@echo "${BLUE}Step 3: fetchComments${RESET}"
	@echo "  - Fetches comments for the first post"
	@echo "  - Input: firstPostId from Step 2 output"
	@echo "  - Output: comments array, commentCount, firstCommentEmail"
	@echo ""
	@echo "${YELLOW}Data Flow:${RESET}"
	@echo "  workflow input → Step 1 → Step 2 → Step 3 → workflow output"

.DEFAULT_GOAL := help