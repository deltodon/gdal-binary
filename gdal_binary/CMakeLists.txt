# Print debug information at the start
message(STATUS "gdal_binary CMakeLists.txt: Starting configuration")
message(STATUS "Initial PROJ_INCLUDE_DIRS: ${PROJ_INCLUDE_DIRS}")
message(STATUS "Initial GDAL_INCLUDE_DIRS: ${GDAL_INCLUDE_DIRS}")
message(STATUS "Initial PROJ_LIBRARIES: ${PROJ_LIBRARIES}")
message(STATUS "Initial GDAL_LIBRARIES: ${GDAL_LIBRARIES}")

# Find Python (this is still needed as it's specific to this subproject)
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# Find SWIG (this is still needed as it's specific to this subproject)
find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

# Print Python and SWIG information
message(STATUS "Python_EXECUTABLE: ${Python_EXECUTABLE}")
message(STATUS "Python_VERSION: ${Python_VERSION}")
message(STATUS "Python_INCLUDE_DIRS: ${Python_INCLUDE_DIRS}")
message(STATUS "Python_LIBRARIES: ${Python_LIBRARIES}")
message(STATUS "SWIG_EXECUTABLE: ${SWIG_EXECUTABLE}")

# Set up SWIG
set(CMAKE_SWIG_FLAGS "")
set_property(SOURCE gdal.i PROPERTY CPLUSPLUS ON)
set_property(SOURCE gdal.i PROPERTY SWIG_MODULE_NAME gdal)

# Check if gdal.i exists
if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/gdal.i")
    message(FATAL_ERROR "gdal.i not found in ${CMAKE_CURRENT_SOURCE_DIR}")
else
    message(STATUS "gdal.i found in ${CMAKE_CURRENT_SOURCE_DIR}")
endif()

# Include directories (GDAL_INCLUDE_DIRS and PROJ_INCLUDE_DIRS should be available from parent scope)
include_directories(${GDAL_INCLUDE_DIRS} ${PROJ_INCLUDE_DIRS})

# Build the GDAL Python wrapper
swig_add_library(gdal
    TYPE SHARED
    LANGUAGE python
    SOURCES gdal.i)

# Link libraries (GDAL_LIBRARIES and PROJ_LIBRARIES should be available from parent scope)
target_link_libraries(gdal ${PYTHON_LIBRARIES} ${GDAL_LIBRARIES} ${PROJ_LIBRARIES})

# Set output name
set_target_properties(gdal PROPERTIES OUTPUT_NAME _gdal)

# Install the Python module
install(TARGETS gdal DESTINATION ${Python_SITEARCH})
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/gdal.py DESTINATION ${Python_SITEARCH})

# Print final debug information
message(STATUS "gdal_binary CMakeLists.txt: Configuration complete")
message(STATUS "Final PROJ_INCLUDE_DIRS: ${PROJ_INCLUDE_DIRS}")
message(STATUS "Final GDAL_INCLUDE_DIRS: ${GDAL_INCLUDE_DIRS}")
message(STATUS "Final PROJ_LIBRARIES: ${PROJ_LIBRARIES}")
message(STATUS "Final GDAL_LIBRARIES: ${GDAL_LIBRARIES}")
message(STATUS "Python_SITEARCH: ${Python_SITEARCH}")
