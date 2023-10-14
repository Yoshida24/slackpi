.PHONY: run
run:
	@echo "Running..."
	bash scripts/run.sh

.PHONY: setup
setup:
	@echo "Setup..."
	bash scripts/setup.sh

.PHONY: serve
serve:
	@echo "Serve..."
	bash scripts/serve.sh

.PHONY: test
test:
	@echo "Testing..."
	bash scripts/test.sh
