.DEFAULT_GOAL := help

###### Development

test: test-lint test-unit test-format

test-lint: ## Run code linting tests
	pylint --errors-only --ignore=templates ./slackcli ./tests

test-unit:
	python -m unittest discover tests

test-format: ## Check formatting
	black --check --diff .

format: ## Format all code
	black ./slackcli ./tests

###### Packaging

package: ## Build source distribution package
	python setup.py sdist

pypi: package ## Upload package to pypi
	twine upload --skip-existing dist/slack-cli-*.tar.gz

###### Additional commands

ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/\n               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
