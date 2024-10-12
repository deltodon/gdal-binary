cmake_minimum_required(VERSION 3.16)
project(GDALPythonWrapper)

# Find Python with required components
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# Print the Python-related variables for debugging
message(STATUS "Python_EXECUTABLE: ${Python_EXECUTABLE}")
message(STATUS "Python_VERSION: ${Python_VERSION}")
message(STATUS "Python_INCLUDE_DIRS: ${Python_INCLUDE_DIRS}")
message(STATUS "Python_LIBRARIES: ${Python_LIBRARIES}")

# Set the correct paths for GDAL Python files
set(GDAL_PYTHON_CSOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/gdal/swig/python")
set(GDAL_PYTHON_PACKAGE_DIR "${CMAKE_CURRENT_BINARY_DIR}/python_package")
set(GDAL_PYTHON_INSTALL_DIR "${Python_SITELIB}")

# Set paths for specific files
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

# Set variables to override GDAL's CMakeLists.txt assumptions
set(GDAL_PYTHON_SETUP_IN ${SETUP_PY_IN})
set(GDAL_PYTHON_README ${README_RST})
set(GDAL_PYTHON_TRIMMED_SYSCONFIG ${TRIMMED_SYSCONFIG_PY})
set(GDAL_PYTHON_INSTALL_CMAKE_IN ${INSTALL_PYTHON_CMAKE_IN})

# Print current working directory and GDAL_PYTHON_CSOURCE_DIR for debugging
message(STATUS "Current working directory: ${CMAKE_CURRENT_SOURCE_DIR}")
message(STATUS "GDAL_PYTHON_CSOURCE_DIR: ${GDAL_PYTHON_CSOURCE_DIR}")

# Include the original CMakeLists.txt from GDAL's SWIG Python directory
include(${CMAKE_CURRENT_SOURCE_DIR}/gdal/swig/python/CMakeLists.txt)

# Ensure the Python package is installed correctly
install(DIRECTORY ${GDAL_PYTHON_PACKAGE_DIR}/
        DESTINATION ${GDAL_PYTHON_INSTALL_DIR}
        COMPONENT pythonbindings)
