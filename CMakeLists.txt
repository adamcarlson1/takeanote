cmake_minimum_required(VERSION 3.10)
project(TakeANoteDependencies)

# Find Python3 interpreter (adjust COMPONENTS as needed)
find_package(Python3 COMPONENTS Interpreter REQUIRED)

# Define a custom target to install Python dependencies
add_custom_target(install-deps ALL
  COMMAND ${Python3_EXECUTABLE} -m pip install --upgrade pip
  COMMAND ${Python3_EXECUTABLE} -m pip install -r ${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt
  COMMENT "Installing Python dependencies from requirements.txt"
)
