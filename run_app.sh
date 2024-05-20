#!/bin/sh

cp .env ./searcher/.env

docker-compose up -d

cd searcher

uvicorn app:app --host 0.0.0.0 --port 8000
