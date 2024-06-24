cmake_minimum_required(VERSION 3.11)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
cmake_policy(SET CMP0135 NEW)
project(KnowledgeGraph LANGUAGES CXX)

include(FetchContent)
FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz)
FetchContent_MakeAvailable(json)

message(STATUS "CMAKE_SOURCE_DIR: ${CMAKE_SOURCE_DIR}")
set(DATA_DIR "${CMAKE_SOURCE_DIR}/data")
add_definitions(-DDATA_DIR="${DATA_DIR}")

set(SRCS
  main.cpp
  src/adjacency_list.cpp
  src/json_defs.cpp
  src/fruchterman_reingold.cpp
  src/layout.cpp
  src/knowledge_graph.cpp
)
add_executable(KnowledgeGraph ${SRCS})

target_link_libraries(KnowledgeGraph PRIVATE nlohmann_json::nlohmann_json)
target_compile_options(KnowledgeGraph PRIVATE -Wall -O3 -std=c++17)
target_include_directories(KnowledgeGraph PRIVATE ${CMAKE_SOURCE_DIR}/include)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")                                     
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")                            
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -g")                                
endif()

add_custom_target(run
  COMMAND KnowledgeGraph
  DEPENDS KnowledgeGraph
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)

enable_testing()
add_subdirectory(test)
