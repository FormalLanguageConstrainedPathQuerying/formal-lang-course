.PHONY: lint lint-fix venv install format rye

PYTHON = python3
VENV_DIR = venv
VENV_PYTHON = $(VENV_DIR)/bin/python
VENV_PIP = $(VENV_DIR)/bin/pip
SOURCE_DIR = .

lint:
	ruff check $(SOURCE_DIR)

lint-fix:
	ruff check --fix $(SOURCE_DIR)

install:
	pip3 install -r requirements.txt

format:
	$(VENV_PYTHON) -m ruff format $(SOURCE_DIR)

venv:
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Virtual environment $(VENV_DIR) already exists"; \
	else \
		echo "Creating virtual environment with $(PYTHON)..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
		echo "Venv created in $(VENV_DIR)"; \
		echo "To activate run: source $(VENV_DIR)/bin/activate"; \
	fi

rye:
	rye fmt --check
	rye fmt