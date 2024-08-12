#!/bin/bash

docker-compose -f docker-compose.yml up --build -d
docker-compose logs -f
