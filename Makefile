.PHONY: all
all: help

.venv:
	@echo "Installing project dependencies.."
	@pdm install -v

clean:
	@echo "Removing .venv"
	@rm -rf .venv

help:
	@echo "Available make targets:"
	@echo " make help         - Print help"
	@echo " make .venv        - Instal project dependencies"
	@echo " make clean        - Remove all build output"
	@echo ""
