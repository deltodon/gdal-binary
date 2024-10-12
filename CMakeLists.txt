cmake_minimum_required(VERSION 3.16)
project(GDALPythonWrapper)

# Find Python with required components
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# Find SWIG
find_package(SWIG REQUIRED)

# Print debug information
message(STATUS "Python_EXECUTABLE: ${Python_EXECUTABLE}")
message(STATUS "Python_VERSION: ${Python_VERSION}")
message(STATUS "Python_INCLUDE_DIRS: ${Python_INCLUDE_DIRS}")
message(STATUS "Python_LIBRARIES: ${Python_LIBRARIES}")
message(STATUS "SWIG_EXECUTABLE: ${SWIG_EXECUTABLE}")

# Set GDAL-specific variables
set(BUILD_PYTHON_BINDINGS ON CACHE BOOL "Build Python bindings")
set(GDAL_PYTHON_CSOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/gdal/swig/python")
set(GDAL_PYTHON_PACKAGE_DIR "${CMAKE_CURRENT_BINARY_DIR}/python_package")
set(GDAL_PYTHON_INSTALL_DIR "${Python_SITELIB}")

# Set the correct paths for GDAL Python files
set(SETUP_PY_IN "${GDAL_PYTHON_CSOURCE_DIR}/setup.py.in")
set(README_RST "${GDAL_PYTHON_CSOURCE_DIR}/README.rst")
set(TRIMMED_SYSCONFIG_PY "${GDAL_PYTHON_CSOURCE_DIR}/trimmedsysconfig.py")
set(INSTALL_PYTHON_CMAKE_IN "${GDAL_PYTHON_CSOURCE_DIR}/install_python.cmake.in")

# Ensure these files exist and print their paths
foreach(file ${SETUP_PY_IN} ${README_RST} ${TRIMMED_SYSCONFIG_PY} ${INSTALL_PYTHON_CMAKE_IN})
    if(NOT EXISTS ${file})
        message(FATAL_ERROR "Required file not found: ${file}")
    else()
        message(STATUS "Found file: ${file}")
    endif()
endforeach()

# Find PROJ
set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/proj)
set(PROJ_DIR ${CMAKE_CURRENT_SOURCE_DIR}/proj)
set(PROJ_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/proj)
set(PROJ_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/proj/include)
set(PROJ_LIBRARY_DIR ${CMAKE_CURRENT_SOURCE_DIR}/proj/lib)

# Add PROJ's cmake directory to CMAKE_MODULE_PATH
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/proj/cmake")

# Set PROJ_DATA environment variable
set(ENV{PROJ_DATA} "${CMAKE_CURRENT_SOURCE_DIR}/proj/data")

find_package(PROJ REQUIRED)

if(PROJ_FOUND)
    message(STATUS "PROJ found:")
    message(STATUS "  PROJ_VERSION: ${PROJ_VERSION}")
    message(STATUS "  PROJ_INCLUDE_DIRS: ${PROJ_INCLUDE_DIRS}")
    message(STATUS "  PROJ_LIBRARIES: ${PROJ_LIBRARIES}")
else()
    message(FATAL_ERROR "PROJ not found. Please check your PROJ installation.")
endif()

# Include GDAL's CMakeLists.txt
add_subdirectory(gdal)

# Ensure the Python package is installed correctly
install(DIRECTORY ${GDAL_PYTHON_PACKAGE_DIR}/
        DESTINATION ${GDAL_PYTHON_INSTALL_DIR}
        COMPONENT pythonbindings)

# Add error checking
if(NOT TARGET GDAL)
    message(FATAL_ERROR "GDAL target not created. Check GDAL build configuration.")
endif()

# Print final configuration for debugging
message(STATUS "BUILD_PYTHON_BINDINGS: ${BUILD_PYTHON_BINDINGS}")
message(STATUS "GDAL_PYTHON_CSOURCE_DIR: ${GDAL_PYTHON_CSOURCE_DIR}")
message(STATUS "GDAL_PYTHON_PACKAGE_DIR: ${GDAL_PYTHON_PACKAGE_DIR}")
message(STATUS "GDAL_PYTHON_INSTALL_DIR: ${GDAL_PYTHON_INSTALL_DIR}")
