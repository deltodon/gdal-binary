# gdal-binary

This project is still in early development and does not include any useful functionality yet.

Please check back later for updates.

An example project built with [pybind11](https://github.com/pybind/pybind11) and
Meson. Python 3.8+ is required.

## Building from source

To build this project from source, you'll need:

1. Python 3.8+
2. Meson build system
3. A C++ compiler compatible with C++14

### Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:deltodon/gdal-binary.git
   cd gdal-binary
   ```

2. Initialise git submodules
   ```bash
   git submodule update --init --recursive
   ```

3. Install dependencies:
   ```bash
   make .venv
   ```

4. Run build locally:
   ```bash
   make wheel
   ```

## Installation from PyPI

Once the project is published to PyPI, you can install it using pip:

```bash
pip install gdal-binary
```

## Usage

```python
import gdal_binary

gdal_binary.add(1, 2)
```

## Development

For development, you can install the project in editable mode:

```bash
pip install -e .
```

To run tests:

```bash
pytest tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
