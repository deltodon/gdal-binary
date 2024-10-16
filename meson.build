project('gdal-binary', 'cpp',
  version : '0.2.0.dev2',
  default_options : ['warning_level=3', 'cpp_std=c++14']
)

# Build PROJ from source using CMake
proj_build_dir = meson.current_build_dir() / 'proj_build'
proj_install_dir = meson.current_build_dir() / 'proj_install'

# Configure and build PROJ
proj_cmake_configure = run_command('cmake',
  '-S', 'proj',
  '-B', proj_build_dir,
  '-DCMAKE_INSTALL_PREFIX=' + proj_install_dir,
  '-DBUILD_SHARED_LIBS=ON',
  '-DENABLE_CURL=ON',
  '-DBUILD_TESTING=OFF',
  '-DCMAKE_BUILD_TYPE=Release',
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
proj_dep = declare_dependency(include_directories: proj_inc, dependencies: proj_lib)

# Build GDAL from source using CMake
gdal_build_dir = meson.current_build_dir() / 'gdal_build'
gdal_install_dir = meson.current_build_dir() / 'gdal_install'

cmake_configure = run_command('cmake',
  '-S', 'gdal',
  '-B', gdal_build_dir,
  '-DCMAKE_INSTALL_PREFIX=' + gdal_install_dir,
  '-DCMAKE_PREFIX_PATH=' + proj_install_dir,
  '-DGDAL_USE_PROJ=ON',
  '-DBUILD_PYTHON_BINDINGS=OFF',
  '-DCMAKE_BUILD_TYPE=Release',
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
gdal_dep = declare_dependency(include_directories: gdal_inc, dependencies: [gdal_lib, proj_dep])

# Add Python module
py_mod = import('python')
py = py_mod.find_installation('python3')
pybind11_dep = dependency('pybind11')

# Create a file with the version number
version_file = configure_file(
  input : 'version.py.in',
  output : 'version.py',
  configuration : {'VERSION': meson.project_version()},
  install_dir : py.get_install_dir() / 'gdal_binary'
)

# Install Python package data
py.install_sources(
  ['gdal_binary/__init__.py', version_file],
  subdir: 'gdal_binary'
)

# Build GDAL's Python wrapper using the new CMake project
# gdal_binary_src_dir = meson.current_source_dir() / 'gdal_binary'
gdal_binary_build_dir = meson.current_build_dir() / 'gdal_binary_build'

# Find SWIG executable
swig_executable = run_command('which', 'swig', check: true).stdout().strip()

# Configure GDAL Python wrapper build
cmake_python_configure = run_command([
  'cmake',
  '-S', 'gdal_binary',
  '-B', gdal_binary_build_dir,
  '-DCMAKE_INSTALL_PREFIX=' + gdal_binary_build_dir,
  '-DSWIG_EXECUTABLE=' + swig_executable,
  '-DGDAL_PYTHON_CSOURCE_DIR=' + 'gdal/swig/python',
  '-DPROJ_DIR=' + (proj_install_dir / 'lib' / 'cmake' / 'proj'),
  '-DGDAL_DIR=' + (gdal_install_dir / 'lib' / 'cmake' / 'gdal'),
  '-DCMAKE_BUILD_TYPE=Release',
  # '-DPython_EXECUTABLE=' + py.path(),
  # '-DPython_INCLUDE_DIRS=' + py.get_variable('INCLUDEPY'),
  # '-DPython_LIBRARIES=' + py.get_variable('LIBDIR'),
], check: true)

# Debug output for CMake configuration
run_command('echo', 'CMake configuration for GDAL Python wrapper completed. Checking build directory...', check: true)
run_command('ls', '-R', gdal_binary_build_dir, check: true)

cmake_python_build = run_command('cmake', '--build', gdal_binary_build_dir, check: true)

# Debug output for CMake build
run_command('echo', 'CMake build for GDAL Python wrapper completed. Checking build directory...', check: true)
run_command('ls', '-R', gdal_binary_build_dir, check: true)

# Copy the built _gdal.so file to the correct location
run_command('cp',
  gdal_binary_build_dir / '_gdal.so',
  meson.current_source_dir() / 'gdal_binary/',
  check: true
)

# Install the built Python module
py.install_sources(
  [gdal_binary_build_dir / 'gdal.py', gdal_binary_build_dir / '_gdal.so'],
  subdir: 'gdal_binary'
)

# Add a custom target to print the contents of the build directory
run_target('print_build_contents',
  command : ['sh', '-c', 'echo "Contents of build directory:" && ls -R ' + gdal_binary_build_dir]
)

# Final debug output
run_command('echo', 'Build process completed. Checking final directory structure...', check: true)
run_command('ls', '-R', '.', check: true)
run_command('echo', 'Checking gdal_binary directory...', check: true)
run_command('ls', '-R', 'gdal_binary', check: true)
