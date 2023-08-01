install:
	poetry install
	poetry run pre-commit install
lint:
	poetry run pre-commit run --all-files --hook-stage=manual --show-diff-on-failure
type:
	poetry run mypy .
safety:
	poetry run safety check --full-report
test:
	poetry run pytest
test-cov:
	poetry run coverage report
test-doc:
	poetry run xdoctest
changelog:
	poetry run auto-changelog
build:
	poetry build
publish:
	poetry publish
