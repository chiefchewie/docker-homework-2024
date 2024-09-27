.PHONY: lint

# TODO: Add flake8 linting and validation checks here
lint:
	@echo "Linting backend code..."
	autopep8 --in-place --recursive .
	autoflake --in-place --recursive .
	isort .
	flake8 .
