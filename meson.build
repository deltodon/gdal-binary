project('gdal-binary', 'cpp',
  version : '0.2.0.dev2',
  default_options : ['warning_level=3', 'cpp_std=c++14'])

# Build PROJ from source using CMake
proj_build_dir = 'proj_build'
proj_install_dir = 'proj_install'

run_command('mkdir', '-p', proj_build_dir, check: true)

proj_cmake_configure = run_command('cmake',
  '-S', meson.current_source_dir() / 'proj',
  '-B', proj_build_dir,
  '-DCMAKE_INSTALL_PREFIX=' + meson.current_build_dir() / proj_install_dir,
  '-DBUILD_SHARED_LIBS=ON',
  '-DENABLE_CURL=ON',
  '-DBUILD_TESTING=OFF',
  check: true
)

proj_cmake_build = run_command('cmake', '--build', proj_build_dir, '--target', 'install', check: true)

# Set up PROJ dependency
proj_inc = include_directories(proj_install_dir / 'include')
proj_lib_dir = meson.current_build_dir() / proj_install_dir / 'lib'
proj_lib = meson.get_compiler('cpp').find_library('proj', dirs: proj_lib_dir)
proj_dep = declare_dependency(include_directories: proj_inc, dependencies: proj_lib)

# Build GDAL from source using CMake
gdal_build_dir = 'gdal_build'
gdal_install_dir = 'gdal_install'

run_command('mkdir', '-p', gdal_build_dir, check: true)

cmake_configure = run_command('cmake', 
  '-S', meson.current_source_dir() / 'gdal',
  '-B', gdal_build_dir,
  '-DCMAKE_INSTALL_PREFIX=' + meson.current_build_dir() / gdal_install_dir,
  '-DCMAKE_PREFIX_PATH=' + meson.current_build_dir() / proj_install_dir,
  '-DGDAL_USE_PROJ=ON',
  '-DBUILD_PYTHON_BINDINGS=OFF',
  check: true
)

cmake_build = run_command('cmake', '--build', gdal_build_dir, '--target', 'install', check: true)

# Set up GDAL dependency
gdal_inc = include_directories(gdal_install_dir / 'include')
gdal_lib_dir = meson.current_build_dir() / gdal_install_dir / 'lib'
gdal_lib = meson.get_compiler('cpp').find_library('gdal', dirs: gdal_lib_dir)
gdal_dep = declare_dependency(include_directories: gdal_inc, dependencies: [gdal_lib, proj_dep])

# Add Python module
py_mod = import('python')
py = py_mod.find_installation('python3')
pybind11_dep = dependency('pybind11')

# Include the src subdirectory
subdir('src')

# Create a file with the version number
version_file = configure_file(
  input : 'version.py.in',
  output : 'version.py',
  configuration : {'VERSION': meson.project_version()},
  install_dir : py.get_install_dir() / 'gdal_binary'
)

# Install Python package data
py.install_sources(
  ['src/gdal_binary/__init__.py', version_file],
  subdir: 'gdal_binary'
)

# Build GDAL's Python wrapper
gdal_python_build_dir = 'gdal_python_build'
run_command('mkdir', '-p', gdal_python_build_dir, check: true)

cmake_python_configure = run_command('cmake',
  '-S', meson.current_source_dir(),
  '-B', gdal_python_build_dir,
  '-DCMAKE_PREFIX_PATH=' + meson.current_build_dir() / gdal_install_dir,
  '-DCMAKE_MODULE_PATH=' + meson.current_source_dir() / 'gdal/cmake;' + meson.current_source_dir() / 'gdal/cmake/helpers',
  '-DCMAKE_INSTALL_PREFIX=' + meson.current_build_dir() / gdal_python_build_dir,
  '-DSWIG_EXECUTABLE=' + run_command('which', 'swig', check: true).stdout().strip(),
  '-DPython3_EXECUTABLE=' + py.path(),
  '-DGDAL_PYTHON_CSOURCE_DIR=' + meson.current_source_dir() / 'gdal/swig/python',
  check: true
)

cmake_python_build = run_command('cmake', '--build', gdal_python_build_dir, check: true)

# Copy the built Python module to the project's Python package directory
run_command('cp', 
  gdal_python_build_dir / 'osgeo/_gdal.so',
  meson.current_source_dir() / 'src/gdal_binary/',
  check: true)
