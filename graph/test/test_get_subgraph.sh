#!/bin/bash

../KnowledgeGraph &
SERVER_PID=$!

sleep 2

JSON=$(cat <<EOF
{
  "index": "test_get_subgraph",
  "triplet_lists": [
    {
      "id": 1,
      "triplets": [
        {"entity1": "A", "relation": "B", "entity2": "C"},
        {"entity1": "C", "relation": "D", "entity2": "E"}
      ]
    },
    {
      "id": 2,
      "triplets": [
        {"entity1": "A", "relation": "B", "entity2": "E"}
      ]
    }
  ]
}
EOF
)

curl -X POST -H "Content-Type: application/json" -d "$JSON" http://localhost:8080/generate

# getting subgraph where the edges id is 2
curl -X POST -H "Content-Type: application/json" -d '{"index": "test_get_subgraph", "values": [2]}' http://localhost:8080/get > tmp_subgraph.json

sed '/"x":/d;/"y":/d;/"size"/d;' "tmp_subgraph.json" > "output.json"

expected_output=../../test/expected/test_get_subgraph.json
sed '/"x":/d;/"y":/d;/"size"/d;' "$expected_output" > "expected_output.json"

if diff -B -Z "expected_output.json" "output.json"; then
  echo "TestGet passed"
  kill $SERVER_PID
  rm -rf ../../data/test_get_subgraph
  exit 0
else
  echo "TestGet failed: files are different"
  kill $SERVER_PID
  rm -rf ../../data/test_get_subgraph
  exit 1
fi
