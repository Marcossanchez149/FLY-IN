PYTHON = python3
MAIN_FILE = fly_in.py
EXAMPLE = maps/easy/01_linear_path.txt

.PHONY: install run debug clean lint lint-strict

install:
	pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN_FILE) $(EXAMPLE)

debug:
	$(PYTHON) -m pdb $(MAIN_FILE) $(EXAMPLE)

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	python3 -m flake8
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3 -m flake8
	python3 -m mypy . --strict