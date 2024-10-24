.PHONY: all
all: help

.venv:
	@echo "Installing project dependencies.."
	@pdm install -G:all --no-self -v

clean:
	@echo "Removing .venv"
	@rm -rf .venv

wheel:
	@echo "Runing cibuildwheel for linux.."
	@sudo rm -rf build
	@mkdir -p build
	@CIBW_CONTAINER_ENGINE="docker;create_args: -v=$(shell pwd)/build:/build" pdm run cibuildwheel --output-dir wheelhouse --platform linux .


help:
	@echo "Available make targets:"
	@echo " make help         - Print help"
	@echo " make .venv        - Instal project dependencies"
	@echo " make clean        - Remove all build output"
	@echo " make wheel        - Run cibuildwheel for linux"
	@echo ""
