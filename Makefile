.PHONY: all clean wheel debug help

all: help

DOCKER_IMG="quay.io/pypa/musllinux_1_2_x86_64:2024.10.01-1"
DOCKER_CFG="docker;create_args: -v=$(shell pwd)/../build:/build"
PYBIN="/opt/python/cp38-cp38/bin"
AFTER_BUILD="python {project}/wheel/add_top_level.py {wheel} {project}/wheel/top_level.txt"

.venv:
	@echo "Installing project dependencies.."
	@pdm install -G:all --no-self -v

clean:
	@echo "Cleaning up build artifacts.."
	@rm -rf .venv wheelhouse build

wheel:
	@echo "Running cibuildwheel for linux.."
	@sudo rm -rf ../build
	@mkdir -p ../build
	@CIBW_CONTAINER_ENGINE=$(DOCKER_CFG) pdm run cibuildwheel --output-dir wheelhouse --platform linux .
	
debug:
	@echo "Starting debug session in Docker container.."
	@docker run --rm -ti -v "$(shell pwd)":/project -v=$(shell pwd)/../build:/build --env PYBIN=$(PYBIN) $(DOCKER_IMG) /bin/bash

build-local:
	@echo "Building package locally.."
	@pip install meson-python ninja
	@meson setup build
	@meson compile -C build
	@meson install -C build

help:
	@echo "Available make targets:"
	@echo " make help         - Print help"
	@echo " make .venv        - Install project dependencies"
	@echo " make clean        - Remove all build artifacts"
	@echo " make wheel        - Run cibuildwheel for linux"
	@echo " make debug        - Start a debug session in Docker container"
	@echo " make build-local  - Build package locally"
	@echo ""
