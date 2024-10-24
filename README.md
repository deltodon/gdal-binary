# gdal-binary

GDAL binary wheels with precompiled binaries for various platforms.

This project packages GDAL Python bindings along with precompiled GDAL and PROJ libraries, making it easier to install and use GDAL in Python projects across different operating systems.

## Features

- Includes GDAL Python bindings
- Precompiled GDAL and PROJ libraries
- Supports multiple platforms (Linux, macOS, Windows)
- Built using Meson and cibuildwheel

## Requirements

- Python 3.8+

## Installation

Once the project is published to PyPI, you can install it using pip:

```bash
pip install gdal-binary
```

## Usage

After installation, you can use GDAL in your Python projects like this:

```python
from osgeo import gdal

# Your GDAL code here
```

## Building from source

To build this project from source, you'll need:

1. Python 3.8+
2. Meson build system
3. A C++ compiler compatible with C++14
4. CMake (for building GDAL and PROJ)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/deltodon/gdal-binary.git
   cd gdal-binary
   ```

2. Initialize git submodules:
   ```bash
   git submodule update --init --recursive
   ```

3. Install dependencies:
   ```bash
   pip install meson-python pybind11 ninja
   ```

4. Build the project:
   ```bash
   meson setup builddir
   meson compile -C builddir
   ```

5. Install the built package:
   ```bash
   pip install .
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

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

This project uses the following open-source libraries:

- [GDAL](https://github.com/OSGeo/gdal)
- [PROJ](https://github.com/OSGeo/PROJ)

We are grateful to the maintainers and contributors of these projects for their valuable work.
