#!/bin/bash

../KnowledgeGraph &
SERVER_PID=$!

sleep 2

JSON=$(cat <<EOF
{
  "index": "test_get",
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

# generating the graph at ../../data/test_get
curl -X POST -H "Content-Type: application/json" -d "$JSON" http://localhost:8080/generate
# getting the json graph as a response and saving it to tmp_get.json
curl -X POST -H "Content-Type: application/json" -d '{"index": "test_get", "values": []}' http://localhost:8080/get > tmp_get.json
# an empty 'values' list means that we want the whole graph

# removing stochastic values from the output json
sed '/"x":/d;/"y":/d;/"size"/d;' "tmp_get.json" > "output.json" 

expected=../../test/expected/test_get.json

sed '/"x":/d;/"y":/d;/"size"/d;' "$expected" > "expected.json"

if diff -B -Z "expected.json" "output.json"; then
  echo "TestGet passed"
  kill $SERVER_PID
  rm -rf ../../data/test_get
  exit 0
else
  echo "TestGet failed: files are different"
  kill $SERVER_PID
  rm -rf ../../data/test_get
  exit 1
fi
