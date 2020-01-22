.DEFAULT_GOAL := help
.PHONY: build

###### Development

test-format: ## Check formatting
	black --check --diff .

format: ## Format all code
	black .

###### Packaging

package: ## Build source distribution package
	python setup.py sdist

pypi: build ## Upload package to pypi
	twine upload --skip-existing dist/slack-cli-*.tar.gz

###### Additional commands

ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/\n               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
