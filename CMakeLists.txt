cmake_minimum_required(VERSION 3.16)
project(GDALPythonWrapper)

# Set default values for Python-related variables if not already set
if(NOT DEFINED Python_EXECUTABLE)
    set(Python_EXECUTABLE $ENV{PYTHON})
endif()

if(NOT DEFINED Python_VERSION)
    execute_process(
        COMMAND ${Python_EXECUTABLE} -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        OUTPUT_VARIABLE Python_VERSION
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
endif()

if(NOT DEFINED Python_INCLUDE_DIR)
    execute_process(
        COMMAND ${Python_EXECUTABLE} -c "import sysconfig; print(sysconfig.get_path('include'))"
        OUTPUT_VARIABLE Python_INCLUDE_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
endif()

if(NOT DEFINED Python_LIBRARY)
    execute_process(
        COMMAND ${Python_EXECUTABLE} -c "import sysconfig; import os; print(os.path.join(sysconfig.get_config_var('LIBDIR'), sysconfig.get_config_var('LDLIBRARY')))"
        OUTPUT_VARIABLE Python_LIBRARY
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
endif()

# Print the Python-related variables for debugging
message(STATUS "Python_EXECUTABLE: ${Python_EXECUTABLE}")
message(STATUS "Python_VERSION: ${Python_VERSION}")
message(STATUS "Python_INCLUDE_DIR: ${Python_INCLUDE_DIR}")
message(STATUS "Python_LIBRARY: ${Python_LIBRARY}")

# Include the original CMakeLists.txt from GDAL's SWIG Python directory
include(${CMAKE_CURRENT_SOURCE_DIR}/gdal/swig/python/CMakeLists.txt)