.PHONY: lint

lint:
	@echo "Linting backend code..."
	autopep8 --in-place --recursive .
	autoflake --in-place --recursive .
	isort .
	flake8 .
