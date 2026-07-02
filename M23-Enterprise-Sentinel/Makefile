.PHONY: help syntax test compose-up compose-down compose-config

PYTHON ?= python3
PYTHONPYCACHEPREFIX ?= /private/tmp/enterprise-sentinel-pycache

help:
	@echo "Enterprise Sentinel targets:"
	@echo "  make syntax         Compile Python files without writing cache into the repo"
	@echo "  make test           Run pytest tests when pytest is installed"
	@echo "  make compose-config Validate docker compose configuration"
	@echo "  make compose-up     Start the full target stack"
	@echo "  make compose-down   Stop the full target stack"

syntax:
	PYTHONPYCACHEPREFIX=$(PYTHONPYCACHEPREFIX) $(PYTHON) -m compileall -q .

test:
	PYTHONPYCACHEPREFIX=$(PYTHONPYCACHEPREFIX) $(PYTHON) -m pytest -q tests

compose-config:
	docker compose config

compose-up:
	docker compose up -d

compose-down:
	docker compose down

