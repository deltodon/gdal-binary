cmake_minimum_required(VERSION 3.12)
project(gdal_binary)

# Set GDAL build options (customize as needed)
set(GDAL_BUILD_OPTIONAL_DRIVERS OFF CACHE BOOL "Build optional drivers")
set(GDAL_ENABLE_DRIVER_PDF OFF CACHE BOOL "Enable PDF driver")

# Include GDAL subdirectory
add_subdirectory(external/gdal gdal_build)

# Install GDAL libraries to a known location
install(
  DIRECTORY ${CMAKE_BINARY_DIR}/gdal_build/
  DESTINATION gdal_install
  FILES_MATCHING PATTERN "*.so" PATTERN "*.dll" PATTERN "*.dylib"
)
