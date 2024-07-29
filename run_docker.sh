#!/bin/bash

docker-compose -f docker-compose.local.yml up --build -d
docker-compose logs -f
