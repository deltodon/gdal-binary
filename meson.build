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

# Get the correct site-packages directory
site_packages_dir = py.get_path('purelib')

# Create a file with the version number
version_file = configure_file(
  input : 'version.py.in',
  output : 'version.py',
  configuration : {'VERSION': meson.project_version()},
  install_dir : site_packages_dir / 'gdal_binary',
  install_tag : 'python'
)

# Copy GDAL Python source files
gdal_python_src = meson.project_source_root() / 'gdal/swig/python'
install_subdir(
  gdal_python_src,
  install_dir : site_packages_dir / 'gdal_binary',
  install_tag : 'python'
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

# Debug output for shared library paths
run_command('echo', 'GDAL shared library path:', gdal_so, check: true)
run_command('echo', 'PROJ shared library path:', proj_so, check: true)

# Install shared libraries with explicit 'runtime' tag
install_data(
  [gdal_so, proj_so],
  install_dir: site_packages_dir / 'gdal_binary',
  install_tag : 'runtime'
)

# Debug output for installation
run_command('echo', 'Python install dir:', py.get_install_dir(), check: true)
run_command('echo', 'Python full path:', py.full_path(), check: true)
run_command('echo', 'Meson build dir:', meson.current_build_dir(), check: true)
run_command('echo', 'site-packages dir:', site_packages_dir, check: true)

# Additional debug output
run_command('echo', 'Checking installed files:', check: true)
run_command('ls', '-R', site_packages_dir, check: true)

# Create a custom target to ensure shared libraries are copied
custom_target('copy_shared_libs',
  output : ['libgdal.so', 'libproj.so'],
  command : ['cp', gdal_so, proj_so, '@OUTDIR@'],
  install : true,
  install_dir : site_packages_dir / 'gdal_binary',
  install_tag : 'runtime'
)

# Additional debug output for shared library installation
run_command('echo', 'Shared library installation paths:', check: true)
run_command('echo', 'GDAL:', site_packages_dir / 'gdal_binary' / 'libgdal.so', check: true)
run_command('echo', 'PROJ:', site_packages_dir / 'gdal_binary' / 'libproj.so', check: true)
