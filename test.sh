#!/bin/bash

# Variables
MONGO_HOST="localhost"
MONGO_PORT="27017"
DB_NAME="test"
COLLECTION_NAME="test"
DOCUMENT='{"name": "test", "value": 123}'

# Insert document into MongoDB
mongosh <<EOF
use $DB_NAME
db.$COLLECTION_NAME.insert($DOCUMENT)
EOF

echo "Document inserted into $DB_NAME.$COLLECTION_NAME"
