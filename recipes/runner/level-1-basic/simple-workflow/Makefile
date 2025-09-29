# Terminal colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)
BLUE   := $(shell tput -Txterm setaf 4)
RED    := $(shell tput -Txterm setaf 1)

# Project settings
RECIPE_NAME := simple-workflow
PYTHON := python3
ARAZZO_FILE := arazzo/workflow.arazzo.yaml
WORKFLOW_ID := getUserInfo
INPUT ?= {"userId": 1}

help: ## Show this help message
	@echo ''
	@echo '${YELLOW}Simple Workflow Recipe${RESET}'
	@echo ''
	@echo '${YELLOW}Quick Start:${RESET}'
	@echo '  ${GREEN}make setup-recipe${RESET}        - Install dependencies'
	@echo '  ${GREEN}make run${RESET}            - Execute workflow'
	@echo '  ${GREEN}make test${RESET}           - Run tests'
	@echo ''
	@echo '${YELLOW}Available Commands:${RESET}'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${YELLOW}%-15s${GREEN}%s${RESET}\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ''


.PHONY: setup-recipe
setup-recipe: ## Install recipe dependencies
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
	@$(PYTHON) -m arazzo_runner validate $(ARAZZO_FILE)
	@echo "${GREEN}✓ Workflow is valid${RESET}"

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
run-all-users: ## Execute workflow for all users (1-10)
	@echo "${BLUE}Fetching all users...${RESET}"
	@for i in 1 2 3 4 5 6 7 8 9 10; do \
	  echo ""; \
	  echo "${YELLOW}User $$i:${RESET}"; \
	  $(PYTHON) -m arazzo_runner execute $(ARAZZO_FILE) \
	    --workflow $(WORKFLOW_ID) \
	    --input "{\"userId\": $$i}" 2>/dev/null | \
	    $(PYTHON) -c "import sys, json; data=json.load(sys.stdin); user=data['outputs']['user']; print(f\"  Name: {user['name']}\n  Email: {user['email']}\n  Username: {user['username']}\")"; \
	done
	@echo "${GREEN}✓ All users fetched${RESET}"

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

.DEFAULT_GOAL := help