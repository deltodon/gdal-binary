cmake_minimum_required(VERSION 3.12)
project(gdal_binary)

# Set GDAL build options
set(GDAL_BUILD_OPTIONAL_DRIVERS OFF CACHE BOOL "Build optional drivers")
set(GDAL_ENABLE_DRIVER_PDF OFF CACHE BOOL "Enable PDF driver")
set(BUILD_SHARED_LIBS OFF CACHE BOOL "Build static libraries")

# Check if Python3_ROOT_DIR is set (it should be set by the GitHub workflow)
if(DEFINED Python3_ROOT_DIR)
  message(STATUS "Python3_ROOT_DIR is set to ${Python3_ROOT_DIR}")
else()
  message(WARNING "Python3_ROOT_DIR is not set. This might cause issues finding the correct Python installation.")
  # Add a fallback search path for manylinux environments
  set(Python3_ROOT_DIR "/opt/python/cp310-cp310" CACHE PATH "Python3 root directory")
endif()

# Check if Python3_EXECUTABLE is set, if not, try to find it
if(NOT DEFINED Python3_EXECUTABLE)
  if(DEFINED Python3_ROOT_DIR)
    find_program(Python3_EXECUTABLE
      NAMES python3 python
      PATHS "${Python3_ROOT_DIR}/bin"
      NO_DEFAULT_PATH
    )
  endif()
  
  if(NOT Python3_EXECUTABLE)
    find_program(Python3_EXECUTABLE NAMES python3 python)
  endif()

  if(Python3_EXECUTABLE)
    message(STATUS "Found Python3 executable: ${Python3_EXECUTABLE}")
  else()
    message(FATAL_ERROR "Python3_EXECUTABLE is not set and could not be found automatically. Please set it via -DPython3_EXECUTABLE=/path/to/python3 or ensure it's set in the environment.")
  endif()
else()
  message(STATUS "Python3_EXECUTABLE is set to ${Python3_EXECUTABLE}")
endif()

# Get Python version
execute_process(
  COMMAND "${Python3_EXECUTABLE}" -c "import sys; print('{}.{}'.format(sys.version_info[0], sys.version_info[1]))"
  OUTPUT_VARIABLE Python3_VERSION_SHORT
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
message(STATUS "Python3_VERSION_SHORT: ${Python3_VERSION_SHORT}")

if(NOT Python3_VERSION_SHORT)
  message(FATAL_ERROR "Failed to determine Python version from ${Python3_EXECUTABLE}")
endif()

# Set find options to prefer the given Python executable and root dir
set(Python3_FIND_STRATEGY LOCATION)
if(NOT DEFINED Python3_ROOT_DIR)
  get_filename_component(Python3_ROOT_DIR "${Python3_EXECUTABLE}" DIRECTORY)
  get_filename_component(Python3_ROOT_DIR "${Python3_ROOT_DIR}" DIRECTORY)
endif()
message(STATUS "Python3_ROOT_DIR is set to ${Python3_ROOT_DIR}")

# Manually specify include and library directories
set(Python3_INCLUDE_DIR "${Python3_ROOT_DIR}/include/python${Python3_VERSION_SHORT}")
set(Python3_LIBRARY "${Python3_ROOT_DIR}/lib/libpython${Python3_VERSION_SHORT}.so")
message(STATUS "Python3_INCLUDE_DIR: ${Python3_INCLUDE_DIR}")
message(STATUS "Python3_LIBRARY: ${Python3_LIBRARY}")

# Find the exact Python version
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(Python3 ${Python3_VERSION_SHORT} EXACT COMPONENTS Interpreter Development
             HINTS "${Python3_ROOT_DIR}"
             PATHS "${Python3_ROOT_DIR}"
                   "/opt/python/cp${Python3_VERSION_SHORT}-cp${Python3_VERSION_SHORT}"
             PATH_SUFFIXES "lib/python${Python3_VERSION_SHORT}/config-${Python3_VERSION_SHORT}-x86_64-linux-gnu"
                           "lib/python${Python3_VERSION_SHORT}/config"
             NO_DEFAULT_PATH
)

if(NOT Python3_FOUND)
  message(WARNING "Failed to find Python3 using CMake's find_package. Trying pkg-config as fallback.")
  find_package(PkgConfig REQUIRED)
  pkg_check_modules(Python3 REQUIRED python3)
  if(Python3_FOUND)
    set(Python3_INCLUDE_DIRS ${Python3_INCLUDE_DIRS})
    set(Python3_LIBRARIES ${Python3_LIBRARIES})
    set(Python3_VERSION ${Python3_VERSION})
  else()
    message(FATAL_ERROR "Failed to find Python3 using both CMake's find_package and pkg-config.")
  endif()
endif()

message(STATUS "Found Python ${Python3_VERSION} at ${Python3_EXECUTABLE}")
message(STATUS "Python3_INCLUDE_DIRS: ${Python3_INCLUDE_DIRS}")
message(STATUS "Python3_LIBRARIES: ${Python3_LIBRARIES}")

# Additional debug output
message(STATUS "Python3_LIBRARY_DIRS: ${Python3_LIBRARY_DIRS}")
message(STATUS "Python3_RUNTIME_LIBRARY_DIRS: ${Python3_RUNTIME_LIBRARY_DIRS}")
message(STATUS "Python3_SITELIB: ${Python3_SITELIB}")

# Set Python3_DIR if not already set
if(NOT DEFINED Python3_DIR)
  set(Python3_DIR "${Python3_ROOT_DIR}/lib/python${Python3_VERSION_SHORT}/config-${Python3_VERSION_SHORT}-x86_64-linux-gnu")
  message(STATUS "Setting Python3_DIR to ${Python3_DIR}")
endif()

# Set GDAL directory
set(GDAL_DIR ${CMAKE_CURRENT_SOURCE_DIR}/gdal)
message(STATUS "GDAL_DIR is set to ${GDAL_DIR}")

# Check if GDAL directory exists
if(NOT EXISTS ${GDAL_DIR})
  message(FATAL_ERROR "GDAL directory not found at ${GDAL_DIR}")
endif()

# Include GDAL subdirectory
add_subdirectory(${GDAL_DIR} ${CMAKE_BINARY_DIR}/gdal_build)

# List available targets
get_property(targets DIRECTORY ${GDAL_DIR} PROPERTY BUILDSYSTEM_TARGETS)
message(STATUS "Available targets in GDAL_DIR: ${targets}")

# Ensure GDAL target is available
if(NOT TARGET GDAL)
  message(FATAL_ERROR "GDAL target not found. Please check the GDAL subdirectory.")
endif()

# Set installation directories outside of gdal
set(GDAL_INSTALL_DIR ${CMAKE_INSTALL_PREFIX}/gdal_binary)
set(GDAL_LIB_INSTALL_DIR ${GDAL_INSTALL_DIR}/lib)
set(GDAL_DATA_INSTALL_DIR ${GDAL_INSTALL_DIR}/gdal-data)
set(GDAL_PYTHON_INSTALL_DIR ${GDAL_INSTALL_DIR}/python)

# Install GDAL library
install(
    TARGETS GDAL
    LIBRARY DESTINATION ${GDAL_LIB_INSTALL_DIR}
    ARCHIVE DESTINATION ${GDAL_LIB_INSTALL_DIR}
    RUNTIME DESTINATION ${GDAL_LIB_INSTALL_DIR}
)

# Install GDAL data files
install(
    DIRECTORY ${GDAL_DIR}/data/
    DESTINATION ${GDAL_DATA_INSTALL_DIR}
)

# Install Python package
install(
    DIRECTORY ${CMAKE_SOURCE_DIR}/src/gdal_binary
    DESTINATION ${GDAL_PYTHON_INSTALL_DIR}
)

# Set GDAL_DATA environment variable
set(ENV{GDAL_DATA} ${GDAL_DATA_INSTALL_DIR})

# Update PYTHONPATH to include the new GDAL Python package location
set(ENV{PYTHONPATH} "${GDAL_PYTHON_INSTALL_DIR}:$ENV{PYTHONPATH}")

# Additional debugging information
message(STATUS "CMake Version: ${CMAKE_VERSION}")
message(STATUS "CMake System Name: ${CMAKE_SYSTEM_NAME}")
message(STATUS "CMake System Version: ${CMAKE_SYSTEM_VERSION}")
message(STATUS "CMake System Processor: ${CMAKE_SYSTEM_PROCESSOR}")
message(STATUS "CMake C Compiler: ${CMAKE_C_COMPILER}")
message(STATUS "CMake CXX Compiler: ${CMAKE_CXX_COMPILER}")
message(STATUS "CMake Find Root Path: ${CMAKE_FIND_ROOT_PATH}")
message(STATUS "CMake Module Path: ${CMAKE_MODULE_PATH}")
message(STATUS "CMake Prefix Path: ${CMAKE_PREFIX_PATH}")
