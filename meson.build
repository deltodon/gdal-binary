project('gdal-binary', 'cpp',
  version : '0.3.0.dev1',
  default_options : [
    'warning_level=3',
    'cpp_std=c++14'
  ],
  license : 'MIT',
  license_files: [
    'LICENSE',
    'gdal/LICENSE.TXT',
    'proj/COPYING'
  ],
  meson_version : '>=1.6.0'
)

package_dir = 'gdal_binary'

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

# Get Python information
py = import('python').find_installation(pure: false)
python_path = py.full_path()
python_version = py.language_version()
python_include_dir = py.get_path('include')
python_library = py.get_path('stdlib')

cmake_configure = run_command('cmake',
  '-S', 'gdal',
  '-B', gdal_build_dir,
  '-DCMAKE_INSTALL_PREFIX=' + gdal_install_dir,
  '-DCMAKE_PREFIX_PATH=' + proj_install_dir,
  '-DGDAL_USE_PROJ=ON',
  '-DBUILD_PYTHON_BINDINGS=ON',
  '-DCMAKE_BUILD_TYPE=Release',
  '-DGDAL_ENABLE_CONFIG_PACKAGE=ON',
  '-DPYTHON_EXECUTABLE=' + python_path,
  '-DPYTHON_INCLUDE_DIR=' + python_include_dir,
  '-DPYTHON_LIBRARY=' + python_library,
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
pybind11_dep = dependency('pybind11')

# Install osgeo and osgeo_utils from the GDAL site-packages directory
gdal_python_build = gdal_install_dir / 'lib' / 'python3.8' / 'site-packages'
run_command('echo', 'gdal_python_build:', gdal_python_build, check: true)

# Create a file with the version number
version_file = configure_file(
  input : 'version.py.in',
  output : '__init__.py',
  configuration : {'VERSION': meson.project_version()},
  install_dir : py.get_install_dir(pure: false) / package_dir,
  install_tag : 'python'
)

install_subdir(
  gdal_python_build / 'osgeo',
  install_dir : py.get_install_dir(pure: false) / package_dir,
  install_tag : 'python'
)

install_subdir(
  gdal_python_build / 'osgeo_utils',
  install_dir : py.get_install_dir(pure: false) / package_dir,
  install_tag : 'python'
)

# Copy GDAL and PROJ shared libraries
gdal_so_files = run_command('find', gdal_lib_dir, '-name', 'libgdal.so*', check: true).stdout().strip().split('\n')
proj_so_files = run_command('find', proj_lib_dir, '-name', 'libproj.so*', check: true).stdout().strip().split('\n')

if cpp_compiler.get_id() == 'msvc'
  gdal_so_files = run_command('find', gdal_lib_dir, '-name', 'gdal*.dll', check: true).stdout().strip().split('\n')
  proj_so_files = run_command('find', proj_lib_dir, '-name', 'proj*.dll', check: true).stdout().strip().split('\n')
elif host_machine.system() == 'darwin'
  gdal_so_files = run_command('find', gdal_lib_dir, '-name', 'libgdal*.dylib', check: true).stdout().strip().split('\n')
  proj_so_files = run_command('find', proj_lib_dir, '-name', 'libproj*.dylib', check: true).stdout().strip().split('\n')
endif

# Debug output
run_command('echo', 'GDAL shared library files:', gdal_so_files, check: true)
run_command('echo', 'PROJ shared library files:', proj_so_files, check: true)

package_libs_dir = package_dir + '.libs'

# Install shared libraries
install_data(
  gdal_so_files + proj_so_files,
  install_dir: py.get_install_dir(pure: false) / package_libs_dir,
  install_tag : 'python'
)

# Debug output
run_command('echo', 'Python installation directory:', py.get_install_dir(pure: false), check: true)
