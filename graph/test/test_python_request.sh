#!/bin/bash

../build/KnowledgeGraph &
SERVER_PID=$!

sleep 2

test_file=../../searcher/tests/files/Ricardo_Meruane-Noctulo.pdf

echo "first request"
curl -X POST -F "file=@$test_file" http://localhost:8000/load-file

echo "second request"
curl -X POST -H "Content-Type: application/json" -d '{"index": "noctulo", "values": [1]}' http://localhost:8000/get-graph > "graph1.json"

echo "third request"
curl -X POST -H "Content-Type: application/json" -d '{"index": "noctulo", "values": [2]}' http://localhost:8000/get-graph > "graph2.json"

cat "graph1.json" | jq .
cat "graph2.json" | jq .

rm "graph1.json"
rm "graph2.json"

curl -X POST "http://localhost:8000/delete-index" -H "Content-Type: application/json" -d '{"request": "noctulo"}'
