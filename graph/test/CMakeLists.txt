add_test(NAME TestGenerate COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/test_generate.sh)
add_test(NAME TestGenerateEmpty COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/test_generate_empty.sh)

add_test(NAME TestGet COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/test_get.sh)
add_test(NAME TestGetInvalid COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/test_get_invalid.sh)
add_test(NAME TestGetSubgraph COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/test_get_subgraph.sh)

