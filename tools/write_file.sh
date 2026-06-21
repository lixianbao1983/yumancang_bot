#!/bin/bash

FILE=$1

if [ -z "$FILE" ]; then
  echo "Usage: write_file.sh path"
  exit 1
fi

echo "🧠 Writing safely to $FILE"

cat > "$FILE"
