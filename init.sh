#!/bin/sh

cp .env ./searcher/.env

docker-compose up -d &&
  echo "Docker containers started successfully" || {
  echo "Failed to start Docker containers"; exit 1; }

(cd ./graph && ./KnowledgeGraph &) &&
  echo "C++ server started successfully" || {
  echo "Failed to start C++ server"; exit 1; }

(cd ./searcher && uvicorn app:app --host 0.0.0.0 --port 8000) &&
  echo "Uvicorn server started successfully" || {
  echo "Failed to start Uvicorn server"; exit 1; }
