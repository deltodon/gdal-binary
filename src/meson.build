python_sources = [
  'gdal_binary/__init__.py',
]

py.install_sources(
  python_sources,
  subdir: 'gdal_binary'
)

cpp_sources = [
  'main.cpp',
  # Add other C++ source files here
]

gdal_binary_lib = shared_library('gdal_binary',
  cpp_sources,
  dependencies: [gdal_dep, pybind11_dep],
  install: true,
  install_dir: py.get_install_dir() / 'gdal_binary'
)

# Create a Python extension module
py.extension_module('_core',
  cpp_sources,
  dependencies: [gdal_dep, pybind11_dep],
  install: true,
  subdir: 'gdal_binary'
)

# Install the version.py file
py.install_sources(
  '../version.py',
  subdir: 'gdal_binary'
)