#!/bin/bash

../KnowledgeGraph &
SERVER_PID=$!

sleep 2

JSON=$(cat <<EOF
{
  "index": "test_generate",
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


# Generate graph at ../../data/test_generate/graph.json
curl -X POST -H "Content-Type: application/json" -d "$JSON" http://localhost:8080/generate

# expected result for the graph generated
expected_output=../../test/expected/test_generate.json
# actual result for the graph generated
output=../../data/test_generate/graph.json

# removing stochastic values from the json files
sed '/"x":/d;/"y":/d;/"size"/d;' "$expected_output" > "tmp_generate_expected.json"
sed '/"x":/d;/"y":/d;/"size"/d;' "$output" > "tmp_generate.json"

# comparing the expected and actual results
if diff -B -Z "tmp_generate.json" "tmp_generate_expected.json"; then
  echo "TestGenerate passed"
  kill $SERVER_PID
  rm -rf ../../data/test_generate
  exit 0
else
  echo "TestGenerate failed"
  kill $SERVER_PID
  rm -rf ../../data/test_generate
  exit 1
fi
