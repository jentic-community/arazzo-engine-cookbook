# Terminal colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)
BLUE   := $(shell tput -Txterm setaf 4)
RED    := $(shell tput -Txterm setaf 1)

# Project settings
RECIPE_NAME := multi-step-flow
PYTHON := python3
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

.PHONY: install
install: ## Install recipe dependencies
	@echo "${BLUE}Installing dependencies...${RESET}"
	@if command -v uv > /dev/null 2>&1; then \
	  uv pip install arazzo-runner>=1.0.0 pyyaml>=6.0.0 requests>=2.31.0; \
	  uv pip install pytest>=7.0.0 pytest-cov>=4.1.0; \
	else \
	  $(PYTHON) -m pip install arazzo-runner>=1.0.0 pyyaml>=6.0.0 requests>=2.31.0; \
	  $(PYTHON) -m pip install pytest>=7.0.0 pytest-cov>=4.1.0; \
	fi
	@echo "${GREEN}✓ Dependencies installed${RESET}"

.PHONY: check
check: ## Verify setup
	@echo "${BLUE}Checking setup...${RESET}"
	@$(PYTHON) --version
	@$(PYTHON) -c "import arazzo_runner; print('✓ arazzo-runner installed')"
	@test -f $(ARAZZO_FILE) && echo "✓ Workflow file exists" || echo "✗ Workflow file missing"
	@echo "${GREEN}✓ Setup verified${RESET}"

.PHONY: validate
validate: ## Validate workflow specification
	@echo "${BLUE}Validating workflow...${RESET}"
	@$(PYTHON) -c "import yaml; yaml.safe_load(open('$(ARAZZO_FILE)'))" && echo "${GREEN}✓ Workflow YAML is valid${RESET}"

.PHONY: run
run: ## Execute workflow (use: make run INPUT='{"userId": 2}')
	@echo "${BLUE}Executing workflow with input: $(INPUT)${RESET}"
	@$(PYTHON) -m arazzo_runner execute-workflow $(ARAZZO_FILE) \
	  --workflow-id $(WORKFLOW_ID) \
	  --inputs '$(INPUT)'
	@echo "${GREEN}✓ Workflow execution completed${RESET}"

.PHONY: run-python
run-python: ## Execute workflow using Python script
	@echo "${BLUE}Running Python example...${RESET}"
	@$(PYTHON) examples/basic_example.py
	@echo "${GREEN}✓ Python example completed${RESET}"

.PHONY: run-all-users
run-all-users: ## Execute workflow for multiple users
	@echo "${BLUE}Fetching content for multiple users...${RESET}"
	@for i in 1 2 3; do \
	  echo ""; \
	  echo "${YELLOW}User $$i:${RESET}"; \
	  $(PYTHON) examples/basic_example.py --user-id $$i 2>/dev/null || true; \
	done
	@echo "${GREEN}✓ All users processed${RESET}"

.PHONY: test
test: ## Run workflow tests
	@echo "${BLUE}Running tests...${RESET}"
	@$(PYTHON) -m pytest tests/ -v
	@echo "${GREEN}✓ Tests completed${RESET}"

.PHONY: test-coverage
test-coverage: ## Run tests with coverage
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