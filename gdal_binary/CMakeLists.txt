cmake_minimum_required(VERSION 3.16)
project(GDALPythonWrapper)

# Find Python
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# Find SWIG
find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

# Find PROJ
find_package(PROJ REQUIRED)

# Find GDAL
find_package(GDAL REQUIRED)

# Set up SWIG
set(CMAKE_SWIG_FLAGS "")
set_property(SOURCE gdal.i PROPERTY CPLUSPLUS ON)
set_property(SOURCE gdal.i PROPERTY SWIG_MODULE_NAME gdal)

# Include directories
include_directories(${GDAL_INCLUDE_DIRS} ${PROJ_INCLUDE_DIRS})

# Build the GDAL Python wrapper
swig_add_library(gdal
    TYPE SHARED
    LANGUAGE python
    SOURCES gdal.i)

# Link libraries
target_link_libraries(gdal ${PYTHON_LIBRARIES} ${GDAL_LIBRARIES} ${PROJ_LIBRARIES})

# Set output name
set_target_properties(gdal PROPERTIES OUTPUT_NAME _gdal)

# Install the Python module
install(TARGETS gdal DESTINATION ${Python_SITEARCH})
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/gdal.py DESTINATION ${Python_SITEARCH})
