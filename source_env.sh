#!/bin/bash

export $(cat .env | xargs)
source activate $VENV
