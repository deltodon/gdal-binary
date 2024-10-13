project('gdal-binary', 'cpp',
  version : '0.2.0.dev2',
  default_options : ['warning_level=3', 'cpp_std=c++14']
)

# Build PROJ from source using CMake
proj_build_dir = meson.current_build_dir() / 'proj_build'
proj_install_dir = meson.current_build_dir() / 'proj_install'

# No need to create the build directory manually; CMake will handle it.
# run_command('mkdir', '-p', proj_build_dir, check: true)

# Configure and build PROJ
proj_cmake_configure = run_command('cmake',
  '-S', 'proj',
  '-B', proj_build_dir,
  '-DCMAKE_INSTALL_PREFIX=' + proj_install_dir,
  '-DBUILD_SHARED_LIBS=ON',
  '-DENABLE_CURL=ON',
  '-DBUILD_TESTING=OFF',
  '-DINSTALL_CMAKE_CONFIG_MODULE=ON',
  check: true
)

proj_cmake_build = run_command('cmake', '--build', proj_build_dir, '--target', 'install', check: true)

# Debug output for PROJ build
# run_command('echo', 'PROJ build completed. Checking installation...', check: true)
# run_command('ls', '-R', proj_install_dir, check: true)

# Set up PROJ dependency
proj_inc = include_directories(proj_install_dir / 'include')
proj_lib_dir = proj_install_dir / 'lib'

# Debug output for PROJ library path
run_command('echo', 'PROJ library directory:', proj_lib_dir, check: true)
run_command('ls', '-l', proj_lib_dir, check: true)

cpp_compiler = meson.get_compiler('cpp')

proj_lib = cpp_compiler.find_library('proj', dirs: [proj_lib_dir])
# proj_dep = declare_dependency(include_directories: proj_inc, dependencies: proj_lib)
proj_dep = declare_dependency(include_directories: proj_inc, link_with: proj_lib)

# Build GDAL from source using CMake
gdal_build_dir = meson.current_build_dir() / 'gdal_build'
gdal_install_dir = meson.current_build_dir() / 'gdal_install'

# No need to create the build directory manually; CMake will handle it.
# run_command('mkdir', '-p', gdal_build_dir, check: true)

cmake_configure = run_command('cmake',
  '-S', 'gdal',
  '-B', gdal_build_dir,
  '-DCMAKE_INSTALL_PREFIX=' + gdal_install_dir,
  '-DCMAKE_PREFIX_PATH=' + proj_install_dir,
  '-DGDAL_USE_PROJ=ON',
  '-DBUILD_PYTHON_BINDINGS=OFF',
  '-DGDAL_ENABLE_CONFIG_PACKAGE=ON',
  check: true
)

cmake_build = run_command('cmake', '--build', gdal_build_dir, '--target', 'install', check: true)

# Debug output for GDAL build
run_command('echo', 'GDAL build completed. Checking installation...', check: true)
run_command('ls', '-R', gdal_install_dir, check: true)

# Set up GDAL dependency
gdal_inc = include_directories(gdal_install_dir / 'include')
gdal_lib_dir = gdal_install_dir / 'lib'
gdal_lib = cpp_compiler.find_library('gdal', dirs: [gdal_lib_dir])
gdal_dep = declare_dependency(include_directories: gdal_inc, link_with: gdal_lib, dependencies: proj_dep)

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
gdal_python_build_dir = meson.current_build_dir() / 'gdal_python_build'

# Old Build GDAL's Python wrapper
# gdal_python_build_dir = 'build'
# run_command('mkdir', '-p', gdal_python_build_dir, check: true)

cmake_python_configure = run_command('cmake',
  '-S', '.',
  '-B', gdal_python_build_dir,
  '-DCMAKE_PREFIX_PATH=' + gdal_install_dir + ';' + proj_install_dir,
  '-DCMAKE_MODULE_PATH=' + 'gdal/cmake;gdal/cmake/helpers',
  '-DCMAKE_INSTALL_PREFIX=' + gdal_python_build_dir,
  '-DSWIG_EXECUTABLE=' + run_command('which', 'swig', check: true).stdout().strip(),
  '-DGDAL_PYTHON_CSOURCE_DIR=' + 'gdal/swig/python',
  '-DPROJ_DIR=' + proj_install_dir / 'lib' / 'cmake' / 'proj',
  '-DGDAL_DIR=' + gdal_install_dir / 'lib' / 'cmake' / 'gdal',
  check: true
)

# Debug output for CMake configuration
run_command('echo', 'CMake configuration for GDAL Python wrapper completed. Checking build directory...', check: true)
run_command('ls', '-R', gdal_python_build_dir, check: true)

cmake_python_build = rrun_command('cmake', '--build', gdal_python_build_dir, check: true)

# Debug output for CMake build
run_command('echo', 'CMake build for GDAL Python wrapper completed. Checking build directory...', check: true)
run_command('ls', '-R', gdal_python_build_dir, check: true)

# Old: Copy the built Python module to the project's Python package directory
# run_command('cp', 
#   gdal_python_build_dir / 'osgeo/_gdal.so',
#   'src/gdal_binary/',
#   check: true)

# Install the built Python module
py.install_sources(
  [gdal_python_build_dir / 'osgeo' / '_gdal.so'],
  subdir: 'gdal_binary'
)

# Final debug output
run_command('echo', 'Build process completed. Checking final directory structure...', check: true)
run_command('ls', '-R', '.', check: true)
run_command('echo', 'Checking src/gdal_binary directory...', check: true)
run_command('ls', '-R', 'src/gdal_binary', check: true)
