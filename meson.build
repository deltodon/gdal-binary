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
run_command('echo', 'PROJ build completed. Checking installation...', check: true)
run_command('ls', '-R', proj_install_dir, check: true)

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

# Copy GDAL Python source files
gdal_python_src = meson.source_root() / 'gdal/swig/python'
install_subdir(gdal_python_src, install_dir : py.get_install_dir() / 'gdal_binary')

# Install Python package data
py.install_sources(
  ['gdal_binary/__init__.py', version_file],
  subdir: 'gdal_binary'
)

# Copy GDAL and PROJ shared libraries
gdal_so = gdal_lib_dir / 'libgdal.so'
proj_so = proj_lib_dir / 'libproj.so'

if cpp_compiler.get_id() == 'msvc'
  gdal_so = gdal_lib_dir / 'gdal.dll'
  proj_so = proj_lib_dir / 'proj.dll'
elif host_machine.system() == 'darwin'
  gdal_so = gdal_lib_dir / 'libgdal.dylib'
  proj_so = proj_lib_dir / 'libproj.dylib'
endif

install_data(
  [gdal_so, proj_so],
  install_dir: py.get_install_dir() / 'gdal_binary'
)

# Create a custom target to build the wheel
custom_target('build_wheel',
  output: 'wheel',
  command: [
    py.path(),
    '-m',
    'build',
    '--wheel',
    '--no-isolation',
    '--outdir',
    meson.current_build_dir() / 'dist'
  ],
  depends: [version_file],
  build_by_default: true
)
