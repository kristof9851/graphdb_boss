#!/bin/bash

MONGOD_BINARY="mongod"
MONGODB_TGZ_URL="https://fastdl.mongodb.org/osx/mongodb-macos-x86_64-8.0.5.tgz"
MONGODB_TGZ_FILENAME="mongodb-macos-x86_64-8.0.5.tgz"
MONGODB_EXTRACT_DIR="mongodb-macos-x86_64-8.0.5"
MONGOD_SYMLINK="/usr/local/bin/mongod"

# Check if mongod is already available
if command -v "$MONGOD_BINARY" &> /dev/null; then
  echo "mongod is already available."
  exit 0
fi

echo "mongod not found. Downloading MongoDB..."

# Download the MongoDB tgz file
curl -LO "$MONGODB_TGZ_URL"

if [ $? -ne 0 ]; then
  echo "Failed to download MongoDB."
  exit 1
fi

echo "Extracting MongoDB..."

# Extract the tgz file
tar -xzf "$MONGODB_TGZ_FILENAME"

if [ $? -ne 0 ]; then
  echo "Failed to extract MongoDB."
  rm "$MONGODB_TGZ_FILENAME"
  exit 1
fi

echo "Creating symlink..."

# Create the symlink
sudo ln -sf "$(pwd)/$MONGODB_EXTRACT_DIR/bin/$MONGOD_BINARY" "$MONGOD_SYMLINK"

if [ $? -ne 0 ]; then
  echo "Failed to create symlink. You might need sudo privileges."
  rm "$MONGODB_TGZ_FILENAME"
  rm -rf "$MONGODB_EXTRACT_DIR"
  exit 1
fi

echo "mongod installed successfully."

# Cleanup the tgz file
rm "$MONGODB_TGZ_FILENAME"

exit 0
