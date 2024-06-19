#!/bin/bash

../KnowledgeGraph &
SERVER_PID=$!

sleep 2


# CONTENT TYPE VERIFICATION
RES=$(curl -X POST -H "Content-Type: plain/text" -d \
  '{"index": "test_generate_empty", "triplet_lists": []}' http://localhost:8080/generate)
# Incorrect content type should return an error
[[ $RES != *"415"* ]] && echo "TestGenerateEmpty failed" && kill $SERVER_PID && exit 1


# GENERATE EMPTY GRAPH
RES=$(curl -X POST -H "Content-Type: application/json" \
  -d '{"index": "test_generate_empty", "triplet_lists": []}' http://localhost:8080/generate)
# No directory nor files should be created
[[ -d ../../data/test_generate_empty ]] && \
  echo "TestGenerateEmpty failed" && \
  kill $SERVER_PID && \
  rm -rf ../../data/test_generate_empty && \
  exit 1
# Response should be an error
[[ "$RES" =~ error ]] && echo "TestGenerateEmpty passed" && kill $SERVER_PID && exit 0


exit 1
