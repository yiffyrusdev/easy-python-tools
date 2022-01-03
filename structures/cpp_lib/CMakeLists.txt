cmake_minimum_required(VERSION 3.20)
project(cpp_lib)

find_package(PythonLibs 3.10 REQUIRED)
find_package(Boost COMPONENTS python REQUIRED)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_SHARED_MODULE_PREFIX "")
set(CMAKE_Cxx_ARCHIVE_CREATE "<CMAKE_AR> qc <TARGET> <LINK_FLAGS> <OBJECTS>")
set(CMAKE_Cxx_ARCHIVE_FINISH "<CMAKE_RANLIB> <TARGET>")
set(CMAKE_SOURCE_DIR ${CMAKE_SOURCE_DIR}/src)

include_directories(PRIVATE ${PYTHON_INCLUDE_DIRS})
link_libraries(${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

#primitives
file( GLOB PRIMITIVES_SOURCES ${CMAKE_SOURCE_DIR}/primitives/*.cpp )
file( GLOB PRIMITIVES_HEADERS ${CMAKE_SOURCE_DIR}/primitives/*.h )
add_library(primitives_lib SHARED ${PRIMITIVES_SOURCES} ${PRIMITIVES_HEADERS} )

add_library(primitives MODULE ${CMAKE_SOURCE_DIR}/primitives_wrapper.cpp)
target_link_libraries(primitives primitives_lib)
#/primitives

#trees
file( GLOB TREES_SOURCES ${CMAKE_SOURCE_DIR}/trees/*.cpp )
file( GLOB TREES_HEADERS ${CMAKE_SOURCE_DIR}/trees/*.h )
add_library(trees_lib SHARED ${TREES_SOURCES} ${TREES_HEADERS} )

add_library(trees MODULE ${CMAKE_SOURCE_DIR}/trees_wrapper.cpp)
target_link_libraries(trees trees_lib)
#/trees