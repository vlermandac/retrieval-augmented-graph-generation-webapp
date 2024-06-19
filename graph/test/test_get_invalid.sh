#!/bin/bash

../KnowledgeGraph &
SERVER_PID=$!

sleep 2

RESPONSE=$(curl -X POST -H "Content-Type: application/json" -d '{"index": "fake_index", "values": []}' http://localhost:8080/get)

echo $RESPONSE

[[ "$RESPONSE" =~ error ]] && echo "TestGetInvalid passed" && kill $SERVER_PID && exit 0

echo "TestGet failed" && kill $SERVER_PID && exit 1
