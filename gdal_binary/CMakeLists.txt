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

# Add target for GDAL Python wrapper
add_custom_target(gdal_binary ALL
    COMMAND ${CMAKE_COMMAND} -E echo "Building GDAL Python wrapper"
    COMMAND ${CMAKE_COMMAND}
        -S "${CMAKE_CURRENT_SOURCE_DIR}"
        -B "${CMAKE_CURRENT_BINARY_DIR}/build"
        "-DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_BINARY_DIR}/build"
        "-DSWIG_EXECUTABLE=${SWIG_EXECUTABLE}"
        "-DGDAL_PYTHON_CSOURCE_DIR=${CMAKE_CURRENT_SOURCE_DIR}/gdal/swig/python"
        "-DPROJ_DIR=${PROJ_DIR}"
        "-DGDAL_DIR=${GDAL_DIR}"
        "-DPROJ_INCLUDE_DIRS=${PROJ_INCLUDE_DIRS}"
        "-DPROJ_LIBRARIES=${PROJ_LIBRARIES}"
        "-DGDAL_INCLUDE_DIRS=${GDAL_INCLUDE_DIRS}"
        "-DGDAL_LIBRARIES=${GDAL_LIBRARIES}"
        "-DPython_EXECUTABLE=${Python_EXECUTABLE}"
        "-DPython_INCLUDE_DIRS=${Python_INCLUDE_DIRS}"
        "-DPython_LIBRARIES=${Python_LIBRARIES}"
    COMMAND ${CMAKE_COMMAND} --build "${CMAKE_CURRENT_BINARY_DIR}/build"
    COMMAND ${CMAKE_COMMAND} -E copy
        "${CMAKE_CURRENT_BINARY_DIR}/build/osgeo/_gdal.so"
        "${CMAKE_CURRENT_SOURCE_DIR}/gdal_binary/"
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
    COMMENT "Building GDAL Python wrapper"
)

# Add a custom command to print the contents of the build directory after the build
add_custom_command(
    TARGET gdal_binary
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E echo "Contents of build directory:"
    COMMAND ${CMAKE_COMMAND} -E ls -R ${CMAKE_CURRENT_BINARY_DIR}/build
)
